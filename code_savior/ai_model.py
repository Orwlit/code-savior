from typing import Tuple

from langchain.chat_models import ChatOpenAI

from config import CS_OPENAI_API_KEY, CS_OPENAI_MODEL, CS_OPENAI_BASE_PATH, CS_OPENAI_MAX_TOKEN, CS_TIMEOUT
from config import CS_MAX_LENGTH, CS_LANGUAGE, CS_N_GENERATE, CS_RESPONSE_TYPE
from config import CS_PROXY, CS_TIMEOUT

from config import ai_logger

class CommitDocAI:
    def __init__(self):
        self.get_config()

        self.llm = ChatOpenAI(
            temperature=0,                                                                         
            model_name=CS_OPENAI_MODEL, 
            openai_api_key=CS_OPENAI_API_KEY,
            openai_api_base=CS_OPENAI_BASE_PATH,
            max_tokens=CS_OPENAI_MAX_TOKEN,
            request_timeout=CS_TIMEOUT,
            openai_proxy=CS_PROXY, # TODO: 不知道这样对不对，langchain说默认值为None
        )
        

    def get_config(self):
        # 获取配置，例如语言、是否使用emoji等
        self.commit_max_length = CS_MAX_LENGTH
        self.commit_n_generate = CS_N_GENERATE
        self.commit_language = CS_LANGUAGE
        self.commit_response_type = CS_RESPONSE_TYPE
        

    def get_translation(self, input:str) -> str:
        # 根据配置获取相应的翻译
        output = input
        return output

    def generate_commit_message_chat_completion_prompt(self, diff):
        # 生成commit消息的prompt
        pass

    def get_messages_promises_by_changes_in_file(self, file_diff, separator, max_change_length):
        # 根据文件的变化获取消息
        pass

    def split_diff(self, diff, max_change_length):
        # 拆分diff以适应最大长度
        pass

    def get_commit_msgs_promises_from_file_diffs(self, diff, max_diff_length):
        # 从文件的diffs中获取commit消息
        pass

    def delay(self, ms):
        # 延迟函数
        pass

    def generate_commit_message_by_diff(self, diff):
        # 主要的函数，根据diff生成commit消息
        pass

# 使用示例
ai_model = None  # 这应该是一个预先训练好的AI模型
commit_doc_ai = CommitDocAI(ai_model)
diff = "..."  # 这是从git diff获取的内容
commit_message = commit_doc_ai.generate_commit_message_by_diff(diff)
print(commit_message)
