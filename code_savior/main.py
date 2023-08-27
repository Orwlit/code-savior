from code_savior.utils.git_utils import get_git_diff_cached_output, git_commit
from code_savior.utils.git_utils import GitDiffProcessor
from code_savior.ai_model import CommitDocAI
from code_savior.interface import GitInterface
from code_savior.config import configure_from_args
from code_savior.config import logger

def main():
    # try:

    # 处理命令行参数并配置参数
    configure_from_args()

    # 获得"git dif --cached"的内容
    diff_content = get_git_diff_cached_output()

    # 将 "git dif" 的信息分类装载到 parsed_data
    git_processor = GitDiffProcessor(diff_content)
    parsed_data = git_processor.process_diff()
    
    llm = CommitDocAI()
    commit_messages = llm.generate_commit_messages_by_diff(parsed_data=parsed_data)

    interface = GitInterface()
    interface.ask_and_execute(commit_messages=commit_messages)


if __name__ == "__main__":
    main()
