import fs from 'fs';
import qrcodeTerminal from 'qrcode-terminal';
import { Client, NoAuth, MessageMedia } from 'whatsapp-web.js';
import yargs from 'yargs/yargs';
import { hideBin } from 'yargs/helpers';
import axios from 'axios';
import { decode } from 'entities';

const parsedArgv = yargs(hideBin(process.argv))
    .scriptName('whatsapp-cli')
    .usage('Usage: $0 [options]')
    .option('save', {
        alias: 's',
        type: 'boolean',
        description: 'Save QR code to file instead of printing it',
    })
    .option('file', {
        alias: 'f',
        type: 'string',
        description: 'QR code file path',
        default: 'qr_code.png',
    })
    .help('h')
    .alias('h', 'help')
    .argv;

const argv = parsedArgv as { [x: string]: unknown; save: boolean | undefined; file: string; _: (string | number)[]; $0: string; };

const client = new Client({
    authStrategy: new NoAuth(),
    puppeteer: {
        headless: false,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            process.platform !== 'win32' ? '--single-process' : '',
            '--disable-gpu',
        ].filter(arg => arg.length > 0),
    },
});

client.on('qr', (qr) => {
    if (argv.save) {
        const qrcode = require('qrcode');
        const filePath = argv.file;

        qrcode.toFile(filePath, qr, { type: 'png' }, (err: Error | null) => {
            if (err) {
                console.error('Failed to save QR code to file:', err);
            } else {
                console.log(`QR code saved to ${filePath}. Scan it with your phone.`);
            }
        });
    } else {
        qrcodeTerminal.generate(qr, { small: true });
    }
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.on('message', async (msg) => {
    if (msg.body === '!ping') {
        msg.reply('pong');
    }

    if (msg.hasMedia) {
        const attachmentData = await msg.downloadMedia();

        // Save the attachment
        if (attachmentData) {
            const filename = `./media/${attachmentData.filename}`;
            fs.writeFile(filename, attachmentData.data, { encoding: 'base64' }, (err) => {
                if (err) {
                    console.error('Failed to save attachment:', err);
                } else {
                    console.log(`Attachment saved to ${filename}`);
                }
            });
        }
    }
});

interface Trivia {
    message: string;
    correctAnswer: string;
}

interface TriviaResult {
    question: string;
    correct_answer: string;
    incorrect_answers: string[];
}


async function fetchTriviaQuestion(): Promise<Trivia | null> {
    try {
        const response = await axios.get('https://opentdb.com/api.php?amount=1&type=multiple');
        const result: TriviaResult = response.data.results[0];

        const question = decode(result.question);
        const correctAnswer = decode(result.correct_answer);
        const incorrectAnswers = result.incorrect_answers.map((answer: string) => decode(answer));

        const options = [correctAnswer, ...incorrectAnswers];
        const message = `Trivia Question: ${question}\n\nOptions:\n${options.map((option, index) => `${index + 1}. ${option}`).join('\n')}`;

        return { message, correctAnswer };
    } catch (error) {
        console.error('Failed to fetch trivia question:', error);
        return null;
    }
}

// Modify the 'client.on('message', ...)' event listener to send a trivia question when '!trivia' is sent
client.on('message', async (msg) => {
    if (msg.hasMedia) {
        try {
            const attachmentData = await msg.downloadMedia();

            // Save the attachment
            if (attachmentData) {
                const filename = `./media/${attachmentData.filename}`;
                await fs.promises.writeFile(filename, attachmentData.data, { encoding: 'base64' });
                console.log(`Attachment saved to ${filename}`);
            }
        } catch (err) {
            console.error('Failed to save attachment:', err);
        }
    }

    if (msg.body === '!ping') {
        msg.reply('pong');
    }

    console.log('Received message:', msg.body);
    if (msg.body === '!trivia') {
        console.log('Sending trivia question...');
        const trivia = await fetchTriviaQuestion();
        if (trivia) {
            msg.reply(trivia.message);
        } else {
            msg.reply('Failed to fetch a trivia question. Please try again.');
        }
    }
});

client.initialize();
