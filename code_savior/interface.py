# from prompt_toolkit.shortcuts import confirm
# from rich import print as rprint

# class GitInterface:

#     def __init__(self):
#         pass

#     def ask_for_confirmation(self, commit_message: str) -> bool:
#         """
#         Display the generated commit message and ask the user for confirmation.

#         Args:
#         - commit_message (str): The generated commit message.

#         Returns:
#         - bool: True if the user confirms, False otherwise.
#         """
#         rprint(f"[bold blue]自动生成的提交信息:[/bold blue] {commit_message}")
#         return confirm("您同意此次提交信息吗?")

#     def git_commit(self, commit_message: str) -> None:
#         """
#         Simulate a git commit operation with the provided message.

#         Args:
#         - commit_message (str): Commit message to use.
#         """
#         # 这里是模拟的git提交操作。实际上您可以调用git命令或使用其他方法进行提交。
#         rprint("[bold green]Committing with message:[/bold green]", commit_message)

import os
import inquirer
from rich import print

from code_savior.config import exclude_files
from code_savior.utils.git_utils import git_commit

class GitInterface:
    def __init__(self):
        pass

    def _confirm_commit_message(self, commit_message):
        """
        Display the generated commit message and ask the user for confirmation.

        Args:
        - commit_message (str): The generated commit message.

        Returns:
        - bool: True if the user confirms, False otherwise.
        """

        # 获取终端的宽度
        terminal_width = os.get_terminal_size().columns
        # Determine the length of the longest line in the commit message
        max_line_length = max(len(line) for line in commit_message.split('\n')) + 4  # Adding 4 for the extra spaces and quotes

        # 如果max_line_length比终端的宽度还大，就使用终端的宽度
        max_line_length = min(max_line_length, terminal_width)
        
        print(f"[cyan]{'-' * max_line_length}[/cyan]")
        for line in commit_message.split('\n'):
            print(f"[yellow] {line} [/yellow]")
        print(f"[cyan]{'-' * max_line_length}[/cyan]")
        print()

        questions = [
            inquirer.List('confirmation',
                          message="Do you agree with this commit message?",
                          choices=['Yes', 'No'],
                          ),
        ]

        answers = inquirer.prompt(questions)
        return answers['confirmation'] == 'Yes'
    
    def ask_and_execute(self, commit_message) -> None:
        if self._confirm_commit_message(commit_message=commit_message):
            print("[green]Committing with the generated message...[/green]")
            git_commit(commit_message=commit_message, exclude_files=exclude_files)
        else:
            print("[red]User declined the generated commit message.[/red]")
