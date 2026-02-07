import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from "dotenv";
import path from "path";
import fs from "fs";

// El .env se carga en el punto de entrada (index.ts)

const apiKey = process.env.GOOGLE_API_KEY;

if (!apiKey || apiKey === "AIza...") {
    console.warn("⚠️ Advertencia: GOOGLE_API_KEY no detectada o es un placeholder.");
}

const genAI = new GoogleGenerativeAI(apiKey || "");

export class AIService {
    private model: any;

    constructor(modelName: string = "gemini-1.5-flash-latest") {
        this.model = genAI.getGenerativeModel({ model: modelName });
    }

    /**
     * Genera una respuesta basada en un prompt simple
     */
    async generateResponse(prompt: string): Promise<string> {
        try {
            if (!apiKey || apiKey === "AIza...") {
                throw new Error("GOOGLE_API_KEY no válida. Por favor, configura la llave real en el archivo .env.");
            }

            const result = await this.model.generateContent(prompt);
            const response = await result.response;
            return response.text();
        } catch (error) {
            console.error("Error en AIService.generateResponse:", error);
            throw error;
        }
    }

    /**
     * Prueba de conexión rápida
     */
    async checkHealth(): Promise<boolean> {
        try {
            const result = await this.model.generateContent("Di 'OK' para confirmar conexión.");
            const text = result.response.text();
            return text.includes("OK");
        } catch (error: any) {
            console.error("Fallo de salud en AIService:", error.message || error);
            return false;
        }
    }
}
