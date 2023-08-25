from utils.git_utils import get_git_diff_cached_output
from utils.git_utils import GitDiffProcessor
import logging

# 设置日志
logging.basicConfig(level=logging.WARNING)
git_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # 获得"git dif --cached"的内容
        diff_content = get_git_diff_cached_output()

        # 将 "git dif" 的信息分类装载到 parsed_data
        git_processor = GitDiffProcessor(diff_content)
        parsed_data = git_processor.process_diff()

    except ValueError as ve:
        git_logger.error(f"Value error occurred: {ve}")
        print(f"Error: {ve}")
    except RuntimeError as re:
        git_logger.error(f"Runtime error occurred: {re}")
        print(f"Error: {re}")
    except Exception as e:
        git_logger.error(f"Unexpected error occurred: {e}")
        print(f"An unexpected error occurred. Please check the logs for more details.")
