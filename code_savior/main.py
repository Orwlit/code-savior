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

    interface = GitInterface()
    commit_msg = "🐛 修复(code.py)：在除法函数中添加对除数为0的判断，避免出现除数为0的错误"
    if interface.ask_for_confirmation(commit_msg):
        interface.git_commit(commit_msg)
    else:
        print("提交已取消。")

    # except ValueError as ve:
    #     logger.error(f"Value error occurred: {ve}")
    #     print(f"Error: {ve}")
    # except RuntimeError as re:
    #     logger.error(f"Runtime error occurred: {re}")
    #     print(f"Error: {re}")
    # except Exception as e:
    #     logger.error(f"Unexpected error occurred: {e}")
    #     print(f"An unexpected error occurred. Please check the logs for more details.")



