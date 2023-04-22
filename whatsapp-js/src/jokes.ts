import axios from 'axios';

export async function fetchRandomJoke(): Promise<string | null> {
    try {
        const response = await axios.get('https://official-joke-api.appspot.com/jokes/random');
        const joke = response.data;

        return `${joke.setup}\n\n${joke.punchline}`;
    } catch (error) {
        console.error('Erreur lors de la récupération d\'une blague:', error);
        return null;
    }
}