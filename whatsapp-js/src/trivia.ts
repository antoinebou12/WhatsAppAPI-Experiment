import axios from 'axios';
import { decode } from 'entities';

interface Trivia {
    title: string;
    question: string;
    options: Array<string>;
    correctAnswer: string;
    message: string;
}

interface TriviaResult {
    question: string;
    correct_answer: string;
    incorrect_answers: string[];
}


async function fetchTriviaQuestion(
    token: string | null = null,
): Promise<Trivia | null> {
    try {
        if (!token) {
            const tokenRequest = await axios.get('https://opentdb.com/api_token.php?command=request');
            token = tokenRequest.data.token;
        }
        const response = await axios.get('https://opentdb.com/api.php?amount=1&type=multiple&token=' + token);
        const result: TriviaResult = response.data.results[0];

        const question = decode(result.question);
        const correctAnswer = decode(result.correct_answer);
        const incorrectAnswers = result.incorrect_answers.map((answer: string) => decode(answer));

        const options = [correctAnswer, ...incorrectAnswers];
        const title = 'Trivia Question';
        const message = `Trivia Question: ${question}\n\nOptions:\n${options.map((option, index) => `${index + 1}. ${option}`).join('\n')}`;

        return { title, question, options, correctAnswer, message };
    } catch (error) {
        console.error('Failed to fetch trivia question:', error);
        return null;
    }
}


export { Trivia, fetchTriviaQuestion };