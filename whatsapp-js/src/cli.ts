import fs from 'fs';
import qrcodeTerminal from 'qrcode-terminal';
import { Client, NoAuth, MessageMedia, Buttons } from 'whatsapp-web.js';
import yargs from 'yargs/yargs';
import { hideBin } from 'yargs/helpers';
import axios from 'axios';
import { decode } from 'entities';
import { fetchTriviaQuestion, Trivia } from './trivia';
import { fetchRandomJoke } from './jokes';
import winston from 'winston';
import { generateResponse } from './openai';
import { fetchWordDefinition } from './word';
import { title } from 'process';

// Créer le logger avec winston
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.printf(({ timestamp, level, message }) => {
            return `[${timestamp}] ${level}: ${message}`;
        })
    ),
    transports: [
        new winston.transports.File({ filename: 'logs.log' }),
    ],
});

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
    .options('headless', {
        alias: 'v',
        type: 'boolean',
        description: 'Run headless',
        default: true,
    })
    .options('help', {
        alias: 'h',
        type: 'boolean',
        description: 'Show help',
    })
    .help('h')
    .alias('h', 'help')
    .argv;

const argv = parsedArgv as { [x: string]: unknown; save: boolean | undefined; file: string; _: (string | number)[]; $0: string; headless: boolean | undefined; help: boolean | undefined; };

const client = new Client({
    authStrategy: new NoAuth(),
    puppeteer: {
        headless: argv.headless,
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
                logger.error('Failed to save QR code to file:' + err, err);
            } else {
                logger.info(`QR code saved to ${filePath}. Scan it with your phone.`);
            }
        });
    } else {
        qrcodeTerminal.generate(qr, { small: true });
    }
});

client.on('ready', () => {
    logger.info('Client is ready!');
});

let currentTrivia: Trivia | null = null;

client.on('message_create', async (msg) => {
    console.log('Received message:' + msg.body);
    logger.info('Received message:' + msg.body);
});

client.on('message', async (msg) => {
    console.log('Received message:' + msg.body);
    logger.info('Received message:' + msg.body);
    logger.debug('Message:' + msg);
    if (msg.hasMedia) {
        try {
            const attachmentData = await msg.downloadMedia();

            // Save the attachment
            if (attachmentData) {
                if (attachmentData.mimetype === 'image/jpeg') {
                    const fileName = `./attachments/${msg.id}.jpg`;
                    fs.writeFileSync(fileName, attachmentData.data, 'base64');
                    logger.info(`Saved attachment to ${fileName}`);
                }
                if (attachmentData.mimetype === 'image/png') {
                    const fileName = `./attachments/${msg.id}.png`;
                    fs.writeFileSync(fileName, attachmentData.data, 'base64');
                    logger.info(`Saved attachment to ${fileName}`);
                }
                if (attachmentData.mimetype === 'video/mp4') {
                    const fileName = `./attachments/${msg.id}.mp4`;
                    fs.writeFileSync(fileName, attachmentData.data, 'base64');
                    logger.info(`Saved attachment to ${fileName}`);
                }
                if (attachmentData.mimetype === 'audio/mp3') {
                    const fileName = `./attachments/${msg.id}.mp3`;
                    fs.writeFileSync(fileName, attachmentData.data, 'base64');
                    logger.info(`Saved attachment to ${fileName}`);
                }
                if (attachmentData.mimetype === 'application/pdf') {
                    const fileName = `./attachments/${msg.id}.pdf`;
                    fs.writeFileSync(fileName, attachmentData.data, 'base64');
                    logger.info(`Saved attachment to ${fileName}`);
                }
                if (attachmentData.mimetype === 'application/zip') {
                    const fileName = `./attachments/${msg.id}.zip`;
                    fs.writeFileSync(fileName, attachmentData.data, 'base64');
                    logger.info(`Saved attachment to ${fileName}`);
                }
            }
        } catch (err) {
            logger.error('Failed to save attachment:' + err);
        }
    }

    if (msg.body.startsWith('!askai')) {
        const prompt = msg.body.slice(6).trim();
        const response = await generateResponse(prompt);
        msg.reply(response);
    }

    if (msg.body.startsWith('!word')) {
        const word = msg.body.slice(6).trim();
        const definition = await fetchWordDefinition(word);
        if (definition) {
            msg.reply(definition);
        } else {
            msg.reply('Failed to fetch definition. Please try again.');
        }
    }

    if (msg.body === '!help') {
        msg.reply('Available Commands: !ping, !joke, !trivia, !answer');
    }

    if (msg.body === '!ping') {
        msg.reply('pong');
    }

    if (msg.body === '!joke') {
        const joke = await fetchRandomJoke();
        if (joke) {
            msg.reply(joke);
        } else {
            msg.reply('Failed to fetch a joke. Please try again.');
        }
    }

    if (msg.body === '!trivia') {
        console.log('Sending trivia question...');
        logger.info('Sending trivia question...');
        const trivia = await fetchTriviaQuestion();
        if (trivia) {
            currentTrivia = trivia;
            let button = new Buttons(trivia.message,
                [
                    { id: '1', body: trivia.options[0] },
                    { id: '2', body: trivia.options[1] },
                    { id: '3', body: trivia.options[2] },
                    { id: '4', body: trivia.options[3] },
                ],
                trivia.title,
                'Select an option to answer the question',
                );
            msg.reply(button);
        } else {
            msg.reply('Failed to fetch a trivia question. Please try again.');
        }
    }

    if (currentTrivia && currentTrivia.options.some(option => msg.body.includes(option))) {
        const answerNumber = parseInt(msg.body.split(' ')[1], 10) - 1;
        const userAnswer = currentTrivia.options[answerNumber];

        // Check if the user's answer matches the correct answer (case insensitive)
        if (userAnswer && userAnswer.trim().toLowerCase() === currentTrivia.correctAnswer.toLowerCase()) {
            msg.reply('Congratulations! You answered correctly.');
            currentTrivia = null; // Reset the trivia question
        } else {
            msg.reply('Incorrect answer. Please try again.');
        }
    }
});

client.initialize();
