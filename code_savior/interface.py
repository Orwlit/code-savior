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
from typing import List

from code_savior.config import exclude_files
from code_savior.utils.git_utils import git_commit

class GitInterface:
    def __init__(self):
        pass

    def _confirm_commit_message(self, commit_messages): # TODO: 能让用户选择一个信息去提交
        """
        Display the generated commit message and ask the user for confirmation.

        Args:
        - commit_message (str): The generated commit message.

        Returns:
        - bool: True if the user confirms, False otherwise.
        """

        # 获取终端的宽度
        terminal_width = os.get_terminal_size().columns
        # 找到commit_messages中所有元素最长的那一行的长度
        max_line_length = 0
        for message in commit_messages:
            max_line_length = max(len(line) for line in message.split('\n')) + 4  # Adding 4 for the extra spaces and quotes

        # 如果max_line_length比终端的宽度还大，就使用终端的宽度
        max_line_length = min(max_line_length, terminal_width)
        
        for message in commit_messages:
            print(f"[cyan]{'-' * max_line_length}[/cyan]")
            for line in message.split('\n'):
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
    
    def ask_and_execute(self, commit_messages:List[str]) -> None:

        if self._confirm_commit_message(commit_messages=commit_messages):
            print("[green]Committing with the generated message...[/green]")
            git_commit(commit_message=commit_messages[0], exclude_files=exclude_files) # TODO: 用户选择一个最好的，这里取了第一个
        else:
            print("[red]User declined the generated commit message.[/red]")

    def choose_best_message(self, commit_messages:List[str]) -> str: # TODO: 能让用户选择一个信息去提交
        pass
    