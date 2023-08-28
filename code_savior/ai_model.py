from typing import List

import openai

from code_savior.config import get_config_values
from code_savior.config import ai_logger

class CommitDocAI:
    def __init__(self):
        self.config_values = get_config_values()
        self.get_config()

        openai.api_key = self.config_values['CS_OPENAI_API_KEY']
       

    def get_config(self):
        # 获取配置，例如语言、是否使用emoji等
        self.commit_max_length = self.config_values['CS_MAX_LENGTH']
        self.commit_n_generate = self.config_values['CS_MAX_ITERATION']
        self.commit_language = self.config_values['CS_LANGUAGE']
        self.commit_response_type = self.config_values['CS_RESPONSE_TYPE']

        self.language_mapping = {
            "en": "English",
            "zh": "Chinese",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "pt": "Portuguese",
            "it": "Italian",
            "nl": "Dutch",
            "sv": "Swedish",
            "el": "Greek",
            "hi": "Hindi",
            # ... 其他语言
        }
        

    def _generate_commit_message_prompt(self, parsed_data) -> str:
        # 用特定语言回答
        language = self.language_mapping.get(self.commit_language, "Unknown Language")
        
        file_changes = ""
        for file_data in parsed_data["file_metadata"]:
            old_path = file_data["old_path"]
            new_path = file_data["new_path"]
            is_new = file_data["is_new_file"]
            is_deleted = file_data["is_deleted_file"]
            old_index = file_data["old_index"]
            new_index = file_data["new_index"]
            file_mode = file_data["file_mode"]
            


            if old_path != new_path:
                file_changes += f"The file path changed from '{old_path}' to '{new_path}'.\n"
            elif is_new:
                file_changes += f"A new file '{new_path}' was added.\n"
            elif is_deleted:
                file_changes += f"The file '{old_path}' was deleted.\n"
            
            changes = parsed_data["changes"].get(new_path, [])
            for change in changes:
                file_changes += f"Change context: {change['info']}\n"
                for line in change['lines']:
                    file_changes += f"{line}\n"
                file_changes += "\n"

        prompt_template = f"In {language}, please summarize the following changes:\n{file_changes}"
        return prompt_template

    def split_diff(self, diff, max_change_length):
        # 拆分diff以适应最大长度
        pass

    def delay(self, ms):
        # 延迟函数
        pass

    def generate_commit_messages_by_diff(self, parsed_data) -> List[str]:
        # 主要的函数，根据diff生成commit消息
        commit_prompt = self._generate_commit_message_prompt(parsed_data)
        
        kwargs = {
            "model": self.config_values['CS_OPENAI_MODEL'],
            "max_tokens": self.config_values['CS_OPENAI_MAX_TOKEN'],
            "temperature": 0,
            "messages": [
                {
                    "role": "user", 
                    "content": commit_prompt
                }
            ],
        }

        commit_messages = []

        for _ in range(self.config_values['CS_MAX_ITERATION']):
            response = openai.ChatCompletion.create(**kwargs)
            # print(f"{response}\n\n")
            # response格式详情见：https://platform.openai.com/docs/guides/gpt/chat-completions-response-format
            message = response.choices[0].message['content']
            commit_messages.append(message)

        return commit_messages
