import { apiUrl } from "./config";

export interface Question {
    id: string;
    text: string;
    options: string[];
    correctAnswer: number; // index
    explanation?: string;
    subject?: "Physics" | "Chemistry" | "Mathematics" | string;
    difficulty?: "Easy" | "Medium" | "Hard" | string;
}

export async function fetchQuestions(subject: string, difficulty: string, count: number, examType?: string): Promise<Question[]> {
    try {
        const response = await fetch(apiUrl("/generate-questions"), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ subject, difficulty, count, exam_type: examType })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Failed to fetch questions from backend:", error);
        // Fallback to mock data if backend is offline (for demo purposes)
        console.warn("Falling back to mock data...");
        await new Promise(resolve => setTimeout(resolve, 1000));
        return Array.from({ length: count }).map((_, i) => ({
            id: `${i}`,
            text: `[FALLBACK] Sample ${difficulty} question for ${subject} #${i + 1}. (Backend unavailable)`,
            options: ["Option A", "Option B", "Option C", "Option D"],
            correctAnswer: Math.floor(Math.random() * 4),
            explanation: "This is a fallback question because the backend could not be reached."
        }));
    }
}
