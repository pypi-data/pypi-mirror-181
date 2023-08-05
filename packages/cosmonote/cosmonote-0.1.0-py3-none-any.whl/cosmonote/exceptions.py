from json import JSONDecodeError

from click import ClickException
from requests import Response
from rich.console import Console


class ApiError(ClickException):
    def __init__(self, response: Response):
        self.response = response
        self.data = self.parse_response(response)
        self.console = Console()
        super().__init__(self.build_message())

    def parse_response(self, response: Response) -> dict[str, str]:
        try:
            data = response.json()
        except JSONDecodeError:
            data = {}
        if response.status_code == 401:
            data = {"code": "UNAUTHORIZED", "message": "Unauthorized."}
        if response.status_code == 404:
            data = {"code": "NOTFOUND", "message": "Not found."}
        return data

    def build_message(self):
        return self.data["message"] if self.data else ""

    def show(self):
        if self.data.get("code"):
            handler = getattr(self, "_" + self.data["code"].lower(), None)
            if handler:
                return handler()
        self.console.print(f"[bold red]Error:[/bold red] {str(self)}")

    def _email_unregistered(self):
        self.console.print(
            "The provided [red]email[/red] has [red]not yet been registered[/red] with the OpenPGP key servers."
        )
        self.console.print(
            "Please visit [cyan]https://keys.openpgp.org[/cyan] for information on registering your email and"
            " public key."
        )


class RegistrationError(ApiError):
    def _duplicate_email(self):
        self.console.print("The provided [red]email[/red] has [red]already been registered[/red].")
        self.console.print(
            "If you [cyan]have[/cyan] the associated private key installed on your machine, you should be able to"
            " access Himitsu straight away."
        )
        self.console.print(
            "If you [cyan]do not have[/cyan] the associated private key installed on your machine, please transfer"
            " the private key to your current machine."
        )

    def _duplicate_public_key(self):
        self.console.print(
            "The [red]public key[/red] associated with the provided email has [red]already has been registered[/red]."
        )
        self.console.print("If you believe this is a [cyan]mistake[/cyan], please contact support.")
