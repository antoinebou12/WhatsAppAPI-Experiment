import { Configuration, OpenAIApi } from 'openai';
import { config } from 'dotenv';

// Load environment variables from the .env file
config();

// Initialize OpenAI API client
const openai = new OpenAIApi(new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
}));

/**
 * Generate a response using OpenAI API.
 *
 * @param prompt The input prompt for the AI.
 * @returns A promise that resolves to the generated response.
 */
export async function generateResponse(prompt: string): Promise<string> {
    try {
        let message = '';
        const response = await openai.createCompletion({
            model: 'gpt3',
            prompt: prompt,
        });
        if (!response.data.choices || !response.data.choices[0]) {
            throw new Error('Invalid response from OpenAI API');
        } else {
            let message = response.data.choices[0].text;
            console.log('Response from OpenAI API:', response.data.choices[0].text);
        }
        return message;
    } catch (error) {
        console.error('Failed to generate response using OpenAI API:', error);
        return 'Sorry, I am unable to generate a response at this moment.';
    }
}