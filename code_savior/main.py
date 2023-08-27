from code_savior.utils.git_utils import get_git_diff_cached_output
from code_savior.utils.git_utils import GitDiffProcessor
from code_savior.ai_model import CommitDocAI
from code_savior.interface import GitInterface
from code_savior.config import logger


if __name__ == "__main__":
    # try:
    # 获得"git dif --cached"的内容
    diff_content = get_git_diff_cached_output()

    # 将 "git dif" 的信息分类装载到 parsed_data
    git_processor = GitDiffProcessor(diff_content)
    parsed_data = git_processor.process_diff()
    
    llm = CommitDocAI()
    commit_message = llm.generate_commit_message_by_diff(parsed_data=parsed_data)


    # interface = GitInterface()
    # commit_msg = "Update the README.md with new installation instructions"
    # if interface.confirm_commit_message(commit_message):
    #     print("Committing with the generated message...")
    #     # Add your git commit logic here
    # else:
    #     print("User declined the generated commit message.")

    interface = GitInterface()
    interface.ask_and_execute(commit_message=commit_message)


    # except ValueError as ve:
    #     logger.error(f"Value error occurred: {ve}")
    #     print(f"Error: {ve}")
    # except RuntimeError as re:
    #     logger.error(f"Runtime error occurred: {re}")
    #     print(f"Error: {re}")
    # except Exception as e:
    #     logger.error(f"Unexpected error occurred: {e}")
    #     print(f"An unexpected error occurred. Please check the logs for more details.")



