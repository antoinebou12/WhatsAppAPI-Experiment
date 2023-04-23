import axios from 'axios';

/**
 * Fetches the definition of a word from the Oxford Dictionary API.
 *
 * @param word The word to fetch the definition for.
 * @returns A promise that resolves to the definition of the word, or null if the word is not found.
 */
export async function fetchWordDefinition(word: string): Promise<string | null> {
    const appId = process.env.OXFORD_APP_ID;
    const appKey = process.env.OXFORD_APP_KEY;
    const apiUrl = `https://od-api.oxforddictionaries.com/api/v2/entries/en-us/${word}`;

    try {
        const response = await axios.get(apiUrl, {
            headers: {
                'app_id': appId,
                'app_key': appKey,
            },
        });

        const definition = response.data.results[0].lexicalEntries[0].entries[0].senses[0].definitions[0];
        return definition;
    } catch (error) {
        let errorVar = error as Error & { response?: { status: number } };
        if (errorVar.response?.status === 404) {
            console.error(`Word "${word}" not found.`);
        } else {
            console.error(`Failed to fetch definition for word "${word}":`, error);
        }
        return null;
    }
}