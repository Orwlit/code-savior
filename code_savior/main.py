from code_savior.utils.git_utils import get_git_diff_cached_output
from code_savior.utils.git_utils import GitDiffProcessor

from code_savior.ai_model import CommitDocAI

from code_savior.config import logger
logger.info("This is an info message from main.py.")

if __name__ == "__main__":
    try:
        # 获得"git dif --cached"的内容
        diff_content = get_git_diff_cached_output()

        # 将 "git dif" 的信息分类装载到 parsed_data
        git_processor = GitDiffProcessor(diff_content)
        parsed_data = git_processor.process_diff()
        
        ai = CommitDocAI()
        ai.generate_commit_message_by_diff(parsed_data=parsed_data)

    except ValueError as ve:
        logger.error(f"Value error occurred: {ve}")
        print(f"Error: {ve}")
    except RuntimeError as re:
        logger.error(f"Runtime error occurred: {re}")
        print(f"Error: {re}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        print(f"An unexpected error occurred. Please check the logs for more details.")



