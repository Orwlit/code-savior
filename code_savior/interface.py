from prompt_toolkit.shortcuts import confirm
from rich import print as rprint

class GitInterface:

    def __init__(self):
        pass

    def ask_for_confirmation(self, commit_message: str) -> bool:
        """
        Display the generated commit message and ask the user for confirmation.

        Args:
        - commit_message (str): The generated commit message.

        Returns:
        - bool: True if the user confirms, False otherwise.
        """
        rprint(f"[bold blue]自动生成的提交信息:[/bold blue] {commit_message}")
        return confirm("您同意此次提交信息吗?")

    def git_commit(self, commit_message: str) -> None:
        """
        Simulate a git commit operation with the provided message.

        Args:
        - commit_message (str): Commit message to use.
        """
        # 这里是模拟的git提交操作。实际上您可以调用git命令或使用其他方法进行提交。
        rprint("[bold green]Committing with message:[/bold green]", commit_message)
