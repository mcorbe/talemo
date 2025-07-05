import sys
from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    help = "Starts a lightweight web server for AI service development."

    default_port = "8001"  # Different port than the main server

    def on_bind(self, server_port):
        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"

        if self._raw_ipv6:
            addr = f"[{self.addr}]"
        elif self.addr == "0":
            addr = "0.0.0.0"
        else:
            addr = self.addr

        from django.conf import settings
        from django.utils.timezone import now

        now_str = now().strftime("%B %d, %Y - %X")
        version = self.get_version()
        print(
            f"{now_str}\n"
            f"Django version {version}, using settings {settings.SETTINGS_MODULE!r}\n"
            f"Starting AI service development server at {self.protocol}://{addr}:{server_port}/\n"
            f"This server only includes AI-specific dependencies.\n"
            f"Quit the server with {quit_command}.",
            file=self.stdout,
        )