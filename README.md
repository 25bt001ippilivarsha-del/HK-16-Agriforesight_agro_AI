# 🌾 Agro AI - Post-Harvest Loss Reduction & Crop Planning Intelligence System

An AI-powered farming assistant that helps farmers reduce post-harvest losses by up to 40% through real-time climate analysis, smart storage recommendations, and market intelligence.

## 🎯 Problem Statement

India loses approximately **₹92,000 crore** worth of food grains annually due to post-harvest losses. Small and marginal farmers suffer the most due to:
- Lack of proper storage facilities
- No access to real-time market prices
- Limited knowledge of optimal selling windows
- Language barriers in accessing agricultural information

## 💡 Our Solution

Agro AI provides an intelligent, multilingual platform that:
- **Predicts spoilage risk** based on real-time weather and storage conditions
- **Recommends optimal crops** based on soil, season, and market demand
- **Tracks market prices** and suggests the best time and place to sell
- **Speaks the farmer's language** with support for 10 Indian languages
- **Offers 24/7 AI assistance** via voice or text in local languages

## ✨ Key Features

### 1. Dashboard
- Real-time weather monitoring with GPS integration
- Live spoilage risk assessment
- AI-powered crop recommendations
- Best market identification
- Climate signal analysis

### 2. Spoilage Risk Prediction
- Crop-specific shelf life calculation
- Temperature and humidity impact analysis
- Storage optimization recommendations
- Sell-by date predictions
- Logistics timing suggestions

### 3. Smart Crop Planning
- Season-aware crop recommendations (Kharif, Rabi, Zaid)
- Soil type matching
- Crop rotation planning with nitrogen tracking
- Soil regeneration strategies
- Risk-adjusted planning horizons

### 4. Market Intelligence
- Real-time price tracking for multiple crops
- 4-week price forecasting
- Local vs nearby market comparison
- Transport cost optimization
- Optimal selling window recommendations

### 5. AI Farming Assistant
- Natural language chat in 10 languages
- Voice input support
- Quick question buttons for common queries
- Context-aware responses with local data
- Offline fallback responses

### 6. Manual Location Search
- Search any city, village, or district by name
- Auto-complete suggestions with geocoding
- Switch between GPS and manual location
- Works even without GPS access

## 🌐 Supported Languages

| Language | Script | Code |
|----------|--------|------|
| English | Latin | en |
| Hindi | हिंदी | hi |
| Bengali | বাংলা | bn |
| Tamil | தமிழ் | ta |
| Telugu | తెలుగు | te |
| Marathi | मराठी | mr |
| Gujarati | ગુજરાતી | gu |
| Kannada | ಕನ್ನಡ | kn |
| Punjabi | ਪੰਜਾਬੀ | pa |
| Odia | ଓଡ଼ିଆ | or |

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python + Flask** | Backend server (primary) |
| **Google Gemini AI** | Natural language understanding & responses |
| **Open-Meteo API** | Real-time weather data |
| **OpenStreetMap Nominatim** | Geolocation, geocoding & reverse geocoding |
| **Web Speech API** | Voice input in regional languages |
| **Chart.js** | Interactive data visualizations |
| **HTML/CSS/JavaScript** | Frontend application |
| **Node.js** | Alternative backend server |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher (recommended)
- OR Node.js v16 or higher
- Google Gemini API Key

### Setup Steps (Python - Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agro-ai.git
   cd agro-ai
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variable and start server**
   ```bash
   # Linux/Mac
   GEMINI_API_KEY=your_api_key_here python app.py
   
   # Windows PowerShell
   $env:GEMINI_API_KEY="your_api_key_here"; python app.py
   ```

4. **Open in browser**
   Navigate to `http://localhost:3000`

### Alternative Setup (Node.js)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agro-ai.git
   cd agro-ai
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set environment variable and start server**
   ```bash
   # Linux/Mac
   GEMINI_API_KEY=your_api_key_here node server.js
   
   # Windows PowerShell
   $env:GEMINI_API_KEY="your_api_key_here"; node server.js
   ```

4. **Open in browser**
   Navigate to `http://localhost:3000`

## 🚀 Usage

### Getting Started
1. Allow location access when prompted for accurate local data
2. Select your preferred language from the dropdown
3. Navigate through Dashboard, Spoilage, Planning, and Market tabs
4. Use the Help button (bottom right) for AI assistance

### Spoilage Prediction
1. Go to **Spoilage Risk** tab
2. Select your crop type
3. Enter harvest date and storage conditions
4. Adjust temperature and humidity sliders
5. Click **Analyze Spoilage Risk**

### Crop Planning
1. Go to **Crop Planning** tab
2. Enter farm area and select irrigation type
3. Choose soil type and risk preference
4. Click **Generate Crop Plan**

### Market Analysis
1. Go to **Market Insights** tab
2. View price trends on the chart
3. Enter crop quantity and transport costs
4. Click **Calculate Best Market**

## 📊 Expected Impact

| Metric | Target |
|--------|--------|
| Post-Harvest Loss Reduction | **40%** |
| Farmer Profit Increase | **25%** |
| Languages Supported | **10+** |
| AI Availability | **24/7** |

## 📁 Project Structure

```
agro-ai/
├── index.html          # Main application HTML
├── app.py              # Python Flask backend (primary)
├── server.js           # Node.js backend (alternative)
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies
├── css/
│   └── style.css       # Application styles
├── js/
│   ├── main.js         # Main application logic
│   ├── ai.js           # AI logic & translations
│   └── services/
│       └── locationService.js  # Location & weather services
└── README.md           # This file
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | AI chatbot (requires `prompt` in body) |
| `/api/geocode?q=` | GET | Search location by name |
| `/api/reverse-geocode?lat=&lon=` | GET | Get location name from coordinates |
| `/api/weather?lat=&lon=` | GET | Get weather data for location |
| `/api/health` | GET | Server health check |

## 🔒 Privacy & Security

- Location data is only used for weather and market calculations
- No personal farming data is stored on servers
- All API communications are encrypted
- Voice input is processed locally when possible

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

Built with ❤️ for Indian farmers

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- Open-Meteo for free weather data
- OpenStreetMap for geolocation services
- All the farmers who inspired this project

---

**Made for Hackathon 2026** 🏆

*Empowering farmers with AI-driven decisions to reduce post-harvest losses and maximize profits.*
