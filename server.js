const http = require("http");
const fs = require("fs");
const path = require("path");
const { URL } = require("url");

const PORT = Number(process.env.PORT || 3000);
const HOST = "0.0.0.0";
const ROOT = __dirname;
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "";
const GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash"];

const MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon"
};

function sendJson(res, status, payload) {
    res.writeHead(status, {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store"
    });
    res.end(JSON.stringify(payload));
}

function readBody(req) {
    return new Promise((resolve, reject) => {
        let body = "";
        req.on("data", (chunk) => {
            body += chunk;
            if (body.length > 2 * 1024 * 1024) {
                reject(new Error("Request body too large"));
                req.destroy();
            }
        });
        req.on("end", () => resolve(body));
        req.on("error", reject);
    });
}

async function generateGeminiReply(prompt) {
    for (const model of GEMINI_MODELS) {
        const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${GEMINI_API_KEY}`;
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    contents: [{ role: "user", parts: [{ text: prompt }] }]
                })
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`${model} ${response.status}: ${text}`);
            }

            const json = await response.json();
            const reply = json?.candidates?.[0]?.content?.parts?.map((part) => part.text).join("\n")?.trim();
            if (reply) return reply;
        } catch (error) {
            console.warn("Gemini call failed:", error.message);
        }
    }

    throw new Error("Gemini request failed for all configured models");
}

function getSafePath(urlPath) {
    const decoded = decodeURIComponent(urlPath);
    const cleanPath = decoded === "/" ? "/index.html" : decoded;
    const normalized = path.normalize(cleanPath).replace(/^(\.\.[/\\])+/, "");
    return path.join(ROOT, normalized);
}

const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);

    if (req.method === "POST" && url.pathname === "/api/chat") {
        try {
            if (!GEMINI_API_KEY) {
                return sendJson(res, 500, { error: "GEMINI_API_KEY not configured on server" });
            }

            const rawBody = await readBody(req);
            const body = rawBody ? JSON.parse(rawBody) : {};
            const prompt = String(body.prompt || "").trim();
            if (!prompt) {
                return sendJson(res, 400, { error: "prompt is required" });
            }

            const reply = await generateGeminiReply(prompt);
            return sendJson(res, 200, { reply });
        } catch (error) {
            return sendJson(res, 500, { error: `Chat request failed: ${error.message}` });
        }
    }

    if (!["GET", "HEAD"].includes(req.method)) {
        res.writeHead(405, { "Content-Type": "text/plain; charset=utf-8" });
        res.end("Method Not Allowed");
        return;
    }

    const filePath = getSafePath(url.pathname);
    if (!filePath.startsWith(ROOT)) {
        res.writeHead(403, { "Content-Type": "text/plain; charset=utf-8" });
        res.end("Forbidden");
        return;
    }

    fs.stat(filePath, (err, stat) => {
        if (err || !stat.isFile()) {
            res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
            res.end("Not Found");
            return;
        }

        const ext = path.extname(filePath).toLowerCase();
        const mime = MIME_TYPES[ext] || "application/octet-stream";
        res.writeHead(200, { "Content-Type": mime });

        if (req.method === "HEAD") {
            res.end();
            return;
        }

        const stream = fs.createReadStream(filePath);
        stream.on("error", () => {
            res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
            res.end("Server Error");
        });
        stream.pipe(res);
    });
});

server.listen(PORT, HOST, () => {
    console.log(`Agro server running at http://localhost:${PORT}`);
});
