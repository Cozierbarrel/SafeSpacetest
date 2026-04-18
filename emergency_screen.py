"""
Tela de Emergência do SafeSpace.
Simula uma ligação para o contato de emergência cadastrado pelo usuário.
"""

import asyncio
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container


class EmergencyScreen(Screen):
    """
    Tela de emergência. Exibe o número do contato de emergência cadastrado
    e simula uma chamada com contagem regressiva de 3 segundos antes de
    retornar automaticamente ao menu principal.
    """

    CSS = """
    EmergencyScreen {
        align: center middle;
        background: $background;
    }

    #emergency-container {
        width: 52;
        height: auto;
        padding: 3 4;
        border: double $error;
        background: $surface;
        align: center middle;
    }

    #emergency-icon {
        text-align: center;
        margin-bottom: 1;
    }

    #emergency-title {
        text-align: center;
        color: $error;
        text-style: bold;
        margin-bottom: 2;
    }

    #call-status {
        text-align: center;
        color: $warning;
        text-style: bold;
        margin-bottom: 1;
    }

    #countdown {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    #no-contact {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    #btn-cancel {
        width: 100%;
        background: $surface-darken-1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Voltar"),
    ]

    def __init__(self):
        """Inicializa a tela de emergência."""
        super().__init__()
        self._seconds_remaining = 3
        self._has_contact = False

    def compose(self) -> ComposeResult:
        """Compõe os widgets da tela de emergência."""
        user = getattr(self.app, "current_user", {})
        contact = user.get("emergency_contact") if user else None
        self._has_contact = bool(contact)

        with Container(id="emergency-container"):
            yield Static("🚨", id="emergency-icon")
            yield Static("EMERGÊNCIA", id="emergency-title")

            if contact:
                yield Static(f"📞  Ligando para {contact}", id="call-status")
                yield Static(f"Retornando ao menu em {self._seconds_remaining}s...", id="countdown")
            else:
                yield Static(
                    "⚠ Nenhum contato de emergência cadastrado.\n\n"
                    "Você pode adicionar um contato no seu perfil.",
                    id="no-contact",
                )

            yield Button("Cancelar / Voltar", id="btn-cancel")

    def on_mount(self) -> None:
        """
        Executado quando a tela é montada. Inicia a contagem regressiva
        apenas se houver um contato de emergência cadastrado.
        """
        if self._has_contact:
            self.set_interval(1.0, self._tick_countdown)

    def _tick_countdown(self) -> None:
        """
        Reduz em 1 segundo o contador de retorno automático.
        Quando chegar a 0, volta automaticamente ao menu principal.
        Verifica se a tela ainda está montada antes de atualizar widgets.
        """
        self._seconds_remaining -= 1

        try:
            countdown_widget = self.query_one("#countdown", Static)
        except Exception:
            # Tela já foi desmontada, ignora o tick
            return

        if self._seconds_remaining > 0:
            countdown_widget.update(f"Retornando ao menu em {self._seconds_remaining}s...")
        else:
            countdown_widget.update("Retornando ao menu...")
            self.action_go_back()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Trata o clique no botão de cancelar, voltando ao menu.
        """
        if event.button.id == "btn-cancel":
            self.action_go_back()

    def action_go_back(self) -> None:
        """Volta para o menu principal."""
        self.app.pop_screen()
