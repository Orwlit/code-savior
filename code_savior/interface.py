from prompt_toolkit.shortcuts import radiolist_dialog
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

class GitInterface:

    def __init__(self):
        self.console = Console()

    def display_header(self):
        self.console.print(Panel("[bold blue]open-commit[/bold blue]"))
        self.console.print("◇  1 staged files:")
        self.console.print("  code.py")
        self.console.print("◇  📝 Commit message generated")

    def ask_for_confirmation(self, commit_message):
        """
        Display the generated commit message and ask the user for confirmation.

        Args:
        - commit_message (str): The generated commit message.

        Returns:
        - bool: True if the user confirms, False otherwise.
        """
        self.display_header()
        self.console.print(Panel(Text(f"Commit message:\n——————————————————\n{commit_message}\n——————————————————", style="bold green")))

        result = radiolist_dialog(
            title="Confirm the commit message?",
            values=[
                ("yes", "● Yes"),
                ("no", "○ No")
            ]).run()

        return result == "yes"

    def git_commit(self, commit_message):
        # 这里添加git提交的逻辑
        self.console.print(f"Committing with message: {commit_message}")
