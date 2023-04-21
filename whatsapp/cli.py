import httpx
import requests
import typer
import os
from rich.console import Console
from whatsapp_client import API as API

import logging
logging.basicConfig(filename='whatsapp_client.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

app = typer.Typer()
console = Console()

class WhatsAppClient:
    """
    WhatsApp Client
    """
    def __init__(self, id_instance: str, api_token_instance: str):
        self.greenAPI = API.GreenApi(id_instance, api_token_instance)
        self.opentdb_token = None

    def send_message(self, recipient_number: str, message: str):
        result = self.greenAPI.sending.sendMessage(chatId=f'{recipient_number}@c.us', message=message)
        result = self.greenAPI.sending.sendMessage(chatId=f'{recipient_number}@c.us', message=message)
        console.print(f"Send result: [bold]{result.data}[/bold]")

    def send_file(self, recipient_number: str, file_path: str):
        result = self.greenAPI.sending.sendFile(chatId=f'{recipient_number}@c.us', urlFile=file_path)
    console.print(f"Send result: [bold]{result.data}[/bold]")
        result = self.greenAPI.sending.sendFile(chatId=f'{recipient_number}@c.us', urlFile=file_path)
        console.print(f"Send result: [bold]{result.data}[/bold]")

    def send_button(self, recipient_number: str, message: str, buttons: list):
        result = self.greenAPI.sending.sendButtons(chatId=f'{recipient_number}@c.us', message=message, buttons=buttons ,footer="Powered by Love Bots")
        console.print(f"Send result: [bold]{result.data}[/bold]")

    def on_event(self, type_webhook, body):
            if type_webhook == "incomingMessageReceived":
                client.process_received_message(body)
                notification_id = body["notificationId"]  # Replace this with the actual field name for the notification ID in the webhook data
                self.greenAPI.deleteNotification(notification_id)

    def receive_notification(self):
        self.greenAPI.webhooks.startReceivingNotifications(self.on_event)

    def process_received_message(self, body):
        if "triva" in body["messageData"]["text"].lower():
            recipient_number = body["senderData"]["id"]
            self.send_trivia_question(recipient_number)
        elif "answer" in body["messageData"]["text"].lower():
            recipient_number = body["senderData"]["id"]
            selected_option = body["messageData"]["text"].split()[-1]
            self.send_correct_answer(recipient_number, selected_option)

    def send_trivia_question(self, recipient_number: str):
        with httpx.Client() as client:
            token = client.get("https://opentdb.com/api_token.php?command=request")
            self.opentdb_token = token.json()["token"]
            print(self.opentdb_token)
            response = client.get(f"https://opentdb.com/api.php?amount=1&type=multiple&token={self.opentdb_token}")

        if response.status_code != 200:
            console.print("Failed to fetch trivia question.", style="bold red")
            return

        data = response.json()
        print(data)
        question = data["results"][0]["question"]
        correct_answer = data["results"][0]["correct_answer"]
        incorrect_answers = data["results"][0]["incorrect_answers"]

        message = f"Trivia Question: {question}\n\nOptions:\n1. {correct_answer}\n"
        for idx, incorrect_answer in enumerate(incorrect_answers, start=2):
            message += f"{idx}. {incorrect_answer}\n"

        self.send_button(recipient_number, message, [
            {"buttonId": "1", "buttonText": "Answer 1"},
            {"buttonId": "2", "buttonText": "Answer 2"},
            {"buttonId": "3", "buttonText": "Answer 3"},
            {"buttonId": "4", "buttonText": "Answer 4"},
        ])

        logger.info(f"Sent trivia question to {recipient_number}: {question}")


    def send_correct_answer(self, recipient_number: str, selected_option: str):
        # Fetch a trivia question again (assuming the same question is fetched)
        with httpx.Client() as client:
            response = client.get("https://opentdb.com/api.php?amount=1&type=multiple&token={self.opentdb_token}")

        if response.status_code != 200:
            console.print("Failed to fetch trivia question.", style="bold red")
            return

        data = response.json()
        correct_answer = data["results"][0]["correct_answer"]
        incorrect_answers = data["results"][0]["incorrect_answers"]

        all_answers = [correct_answer] + incorrect_answers
        correct_option = "1"

        if selected_option == correct_option:
            message = "Congratulations! Your answer is correct."
        else:
            message = f"Sorry, the correct answer is option {correct_option}: {correct_answer}"
        self.send_message(recipient_number, message)

    def openai_answer(self, recipient_number: str, question: str):
        response = requests.post(
            "https://api.openai.com/v1/engines/davinci/completions",
            json={
                "prompt": f"Q: {question}\nA:",
                "temperature": 0.9,
                "max_tokens": 150,
                "top_p": 1,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.6,
                "stop": ["\n", "Q:"]
            },
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
            }
        )
        if response.status_code != 200:
            console.print("Failed to fetch answer.", style="bold red")
            return

        data = response.json()
        answer = data["choices"][0]["text"]

        self.send_message(recipient_number, answer)


client = None

@app.callback(
    help="Setup the WhatsApp client"
)
def setup():
    global client
    id_instance = os.getenv('ID_INSTANCE')
    api_token_instance = os.getenv('API_TOKEN_INSTANCE')
    if id_instance is None or api_token_instance is None:
        console.print("Please set ID_INSTANCE and API_TOKEN_INSTANCE environment variables.", style="bold red")
        raise typer.Exit(code=1)
    client = WhatsAppClient(id_instance, api_token_instance)

@app.command(
    help="Send a message to a WhatsApp number"
)
def send_message(recipient_number: str, message: str):
    """Send a message to a WhatsApp number"""
    if client is None:
        console.print("Please run the setup() function first.", style="bold red")
        raise typer.Exit(code=1)
    client.send_message(recipient_number, message)

@app.command(
    help="Send a file to a WhatsApp number"
)
def send_file(recipient_number: str, file_path: str):
    """Send a file to a WhatsApp number"""
    if client is None:
        console.print("Please run the setup() function first.", style="bold red")
        raise typer.Exit(code=1)
    client.send_file(recipient_number, file_path)

@app.command(
    help="Send a file to a WhatsApp number"
)
def send_trivia(recipient_number: str):
    """Send a trivia question to a WhatsApp number"""
    if client is None:
        console.print("Please run the setup() function first.", style="bold red")
        raise typer.Exit(code=1)
    client.send_trivia_question(recipient_number)

@app.command(
    help="Receive notifications from WhatsApp"
)
def receive_notifications():
    """Receive notifications from WhatsApp"""
    if client is None:
        console.print("Please run the setup() function first.", style="bold red")
        raise typer.Exit(code=1)
    client.receive_notification(client.process_received_message)

@app.command(
    help="Send a message and check for notifications"
)
def send_and_check_notifications(recipient_number: str, message: str):
    """Send a message and check for notifications"""
    if client is None:
        console.print("Please run the setup() function first.", style="bold red")
        raise typer.Exit(code=1)

    client.send_message(recipient_number, message)
    client.receive_notification(client.process_received_message)

@app.command(
    help="Send a message and check for notifications"
)
def send_and_check_notifications_trivia(recipient_number: str):
    """Send a trivia question and check for notifications"""
    if client is None:
        console.print("Please run the setup() function first.", style="bold red")
        raise typer.Exit(code=1)

    client.send_trivia_question(recipient_number)
    client.receive_notification(client.process_received_message)

if __name__ == "__main__":
    app()