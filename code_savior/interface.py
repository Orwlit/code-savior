import inquirer
from rich import print
from typing import List

from code_savior.utils.git_utils import git_commit

class GitInterface:
    def __init__(self):
        pass

    def choose_and_confirm_message(self, commit_messages: List[str]) -> str:
        """
        Let the user choose the best commit message from the list and confirm the choice.

        Args:
        - commit_messages (List[str]): List of generated commit messages.

        Returns:
        - str: The commit message chosen by the user or None if the user chooses "No".
        """
        # 添加"No"选项到commit_messages列表的末尾
        options = commit_messages + ["No, I don't want to commit with these messages."]

        questions = [
            inquirer.List('chosen_message',
                        message="Please choose the best commit message or decline the commit:",
                        choices=options,
                        ),
        ]

        answers = inquirer.prompt(questions)
        chosen_message = answers['chosen_message']

        # 如果用户选择"No"，则返回None
        if chosen_message == "No, I don't want to commit with these messages.":
            return None

        return chosen_message

    def ask_and_execute(self, commit_messages: List[str]) -> None:
        """
        Display the generated commit messages, let the user choose the best one, and execute the commit.

        Args:
        - commit_messages (List[str]): List of generated commit messages.
        """
        chosen_message = self.choose_and_confirm_message(commit_messages)

        if chosen_message:
            print("[green]Committing with the chosen message...[/green]")
            git_commit(commit_message=chosen_message)
        else:
            print("[red]User declined the generated commit messages.[/red]")
    