import requests
import typer
import os
from rich.console import Console
from whatsapp_client import API as API

app = typer.Typer()
console = Console()

class WhatsAppClient:
    def __init__(self, id_instance: str, api_token_instance: str):
        self.greenAPI = API.GreenApi(id_instance, api_token_instance)

    def send_message(self, recipient_number: str, message: str):
        result = self.greenAPI.sending.sendMessage(recipient_number, message)
        console.print(f"Send result: [bold]{result.data}[/bold]")

    def send_file(self, recipient_number: str, file_path: str):
        result = self.greenAPI.sending.sendFile(recipient_number, file_path)
        console.print(f"Send result: [bold]{result.data}[/bold]")

    def send_trivia_question(self, recipient_number: str):
        response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        if response.status_code != 200:
            console.print("Failed to fetch trivia question.", style="bold red")
            return

        data = response.json()
        question = data["results"][0]["question"]
        correct_answer = data["results"][0]["correct_answer"]
        incorrect_answers = data["results"][0]["incorrect_answers"]

        message = f"Trivia Question: {question}\n\nOptions:\n1. {correct_answer}\n"
        for idx, incorrect_answer in enumerate(incorrect_answers, start=2):
            message += f"{idx}. {incorrect_answer}\n"

        self.send_message(recipient_number, message)

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

if __name__ == "__main__":
    app()