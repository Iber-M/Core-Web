import dotenv from 'dotenv';
import path from 'path';
dotenv.config();

import express from 'express';
import cors from 'cors';
import { AIService } from './services/AIService';

const app = express();
const port = process.env.PORT || 3005;

app.use(cors());
app.use(express.json());

const aiService = new AIService();

/**
 * Endpoint de prueba: Confirma si el cerebro está activo
 */
app.get('/api/ai/health', async (req, res) => {
    try {
        const isHealthy = await aiService.checkHealth();
        if (isHealthy) {
            res.json({
                status: 'active',
                message: '🧠 El cerebro de Core-Web está en línea.',
                engine: 'Google Gemini 1.5'
            });
        } else {
            res.status(503).json({
                status: 'degraded',
                message: 'Conexión con la IA fallida. Revisa la GOOGLE_API_KEY.'
            });
        }
    } catch (error: any) {
        res.status(500).json({
            status: 'error',
            message: error.message
        });
    }
});

/**
 * Endpoint para interacciones (POST)
 */
app.post('/api/ai/prompt', async (req, res) => {
    const { prompt } = req.body;

    if (!prompt) {
        return res.status(400).json({ error: 'Se requiere un prompt válido.' });
    }

    try {
        const response = await aiService.generateResponse(prompt);
        res.json({ success: true, response });
    } catch (error: any) {
        console.error('API Error:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(port, () => {
    console.log(`\n🚀 Backend de Core-Web activo`);
    console.log(`📍 URL: http://localhost:${port}`);
    console.log(`📡 Health Check: http://localhost:${port}/api/ai/health\n`);
});
