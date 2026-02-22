"""
Agro AI - Python Backend Server
Post-Harvest Loss Reduction & Crop Planning Intelligence System
"""

import os
import json
import mimetypes
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import requests

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Configuration
PORT = int(os.environ.get('PORT', 3000))
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_MODELS = ['gemini-2.5-flash', 'gemini-2.0-flash']

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Root directory
ROOT = Path(__file__).parent


def generate_gemini_reply(prompt: str) -> str:
    """
    Generate a reply using Google Gemini AI.
    Tries multiple models in case one fails.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured on server")
    
    last_error = None
    
    for model in GEMINI_MODELS:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        try:
            response = requests.post(
                endpoint,
                params={'key': GEMINI_API_KEY},
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{'role': 'user', 'parts': [{'text': prompt}]}]
                },
                timeout=30
            )
            
            if not response.ok:
                raise Exception(f"{model} {response.status_code}: {response.text}")
            
            data = response.json()
            candidates = data.get('candidates', [])
            
            if candidates:
                parts = candidates[0].get('content', {}).get('parts', [])
                reply = '\n'.join(part.get('text', '') for part in parts).strip()
                if reply:
                    return reply
                    
        except Exception as e:
            print(f"Gemini call failed for {model}: {e}")
            last_error = e
            continue
    
    raise Exception(f"Gemini request failed for all configured models: {last_error}")


def geocode_location(query: str) -> dict:
    """
    Convert a location name/address to coordinates using Nominatim.
    Returns location data including lat, lon, state, district.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'limit': 5,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'AgroAI/1.0 (Agricultural Planning App)',
            'Accept-Language': 'en'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if not response.ok:
            raise Exception(f"Nominatim status {response.status_code}")
        
        results = response.json()
        
        if not results:
            return {'error': 'Location not found', 'suggestions': []}
        
        # Process results
        locations = []
        for result in results:
            address = result.get('address', {})
            locations.append({
                'lat': float(result.get('lat', 0)),
                'lon': float(result.get('lon', 0)),
                'display_name': result.get('display_name', ''),
                'state': address.get('state') or address.get('region') or address.get('country', ''),
                'district': (address.get('city') or address.get('town') or 
                           address.get('village') or address.get('county') or 'Unknown'),
                'country': address.get('country', '')
            })
        
        return {
            'success': True,
            'results': locations,
            'count': len(locations)
        }
        
    except Exception as e:
        print(f"Geocoding error: {e}")
        return {'error': str(e), 'suggestions': []}


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle AI chat requests."""
    try:
        if not GEMINI_API_KEY:
            return jsonify({'error': 'GEMINI_API_KEY not configured on server'}), 500
        
        data = request.get_json() or {}
        prompt = str(data.get('prompt', '')).strip()
        
        if not prompt:
            return jsonify({'error': 'prompt is required'}), 400
        
        reply = generate_gemini_reply(prompt)
        return jsonify({'reply': reply})
        
    except Exception as e:
        return jsonify({'error': f'Chat request failed: {str(e)}'}), 500


@app.route('/api/geocode', methods=['GET'])
def geocode():
    """
    Geocode a location query to coordinates.
    Query param: q (location name or address)
    """
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Query too short'}), 400
        
        result = geocode_location(query)
        
        if 'error' in result and result['error'] != 'Location not found':
            return jsonify(result), 500
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reverse-geocode', methods=['GET'])
def reverse_geocode():
    """
    Reverse geocode coordinates to location name.
    Query params: lat, lon
    """
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not lat or not lon:
            return jsonify({'error': 'lat and lon parameters are required'}), 400
        
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return jsonify({'error': 'Invalid coordinates'}), 400
        
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'zoom': 10,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'AgroAI/1.0 (Agricultural Planning App)',
            'Accept-Language': 'en'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if not response.ok:
            return jsonify({'error': f'Nominatim status {response.status_code}'}), 500
        
        data = response.json()
        address = data.get('address', {})
        
        return jsonify({
            'success': True,
            'lat': lat,
            'lon': lon,
            'display_name': data.get('display_name', ''),
            'state': address.get('state') or address.get('region') or address.get('country', ''),
            'district': (address.get('city') or address.get('town') or 
                        address.get('village') or address.get('county') or 'Unknown')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather', methods=['GET'])
def weather():
    """
    Get weather data for coordinates.
    Query params: lat, lon
    """
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not lat or not lon:
            return jsonify({'error': 'lat and lon parameters are required'}), 400
        
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return jsonify({'error': 'Invalid coordinates'}), 400
        
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,rain,wind_speed_10m,weather_code',
            'forecast_days': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if not response.ok:
            return jsonify({'error': f'Weather API status {response.status_code}'}), 500
        
        data = response.json()
        current = data.get('current', {})
        
        if not current:
            return jsonify({'error': 'Missing weather data'}), 500
        
        # Map weather codes to conditions
        weather_code = current.get('weather_code', 0)
        condition = map_weather_code(weather_code)
        
        return jsonify({
            'success': True,
            'temp': round(current.get('temperature_2m', 0)),
            'humidity': round(current.get('relative_humidity_2m', 0)),
            'rainfall': current.get('rain', 0),
            'windSpeed': round(current.get('wind_speed_10m', 0)),
            'weatherCode': weather_code,
            'condition': condition
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def map_weather_code(code: int) -> str:
    """Map Open-Meteo weather codes to human-readable conditions."""
    weather_map = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        77: 'Snow grains',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with hail',
        99: 'Thunderstorm with heavy hail'
    }
    return weather_map.get(code, 'Unknown')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'gemini_configured': bool(GEMINI_API_KEY),
        'models': GEMINI_MODELS
    })


# Serve static files
@app.route('/')
def index():
    """Serve the main HTML file."""
    return send_file(ROOT / 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, images)."""
    file_path = ROOT / filename
    
    if not file_path.exists() or not file_path.is_file():
        return "Not Found", 404
    
    # Ensure the file is within the root directory (security check)
    try:
        file_path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        return "Forbidden", 403
    
    return send_file(file_path)


if __name__ == '__main__':
    print(f"🌾 Agro AI Python Server")
    print(f"📍 Running at http://localhost:{PORT}")
    print(f"🤖 Gemini API: {'Configured' if GEMINI_API_KEY else 'NOT CONFIGURED'}")
    print(f"🔧 Models: {', '.join(GEMINI_MODELS)}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
