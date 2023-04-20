from whatsapp_api_client_python import API as API
import typer
import os
from rich.console import Console

app = typer.Typer()
console = Console()

greenAPI = None

@app.callback()
def setup():
    global greenAPI
    id_instance = os.getenv('ID_INSTANCE')
    api_token_instance = os.getenv('API_TOKEN_INSTANCE')
    if id_instance is None or api_token_instance is None:
        console.print("Please set ID_INSTANCE and API_TOKEN_INSTANCE environment variables.", style="bold red")
        raise typer.Exit(code=1)
    greenAPI = API.GreenApi(id_instance, api_token_instance)

@app.command()
def send_message(recipient_number: str, message: str):
    result = greenAPI.sending.sendMessage(recipient_number, message)
    console.print(f"Send result: [bold]{result.data}[/bold]")

if __name__ == "__main__":
    app()
