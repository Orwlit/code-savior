from typing import Tuple, List

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
        self.commit_n_generate = self.config_values['CS_N_GENERATE']
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
        

    def get_translation(self, input:str) -> str:
        # 根据配置获取相应的翻译
        output = input
        return output

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
                file_changes += f"For the file '{old_path}', index changed from {old_index} to {new_index}:\n"
            else:
                file_changes += f"For the file '{old_path}' (index {old_index}) changed to '{new_path}' (index {new_index}):\n"
            
            if is_new:
                file_changes += "This is a new file.\n"
            elif is_deleted:
                file_changes += "This file was deleted.\n"
            if file_mode:
                file_changes += f"File mode: {file_mode}\n"
            
            changes = parsed_data["changes"].get(new_path, [])
            for change in changes:
                file_changes += f"Change context: {change['info']}\n"
                for line in change['lines']:
                    file_changes += f"{line}\n"
                file_changes += "\n"

        prompt_template = f"In {language}, please summarize the following changes:\n{file_changes}"
        return prompt_template

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

        for _ in range(self.config_values['CS_N_GENERATE']):
            response = openai.ChatCompletion.create(**kwargs)
            # print(f"{response}\n\n")
            # response格式详情见：https://platform.openai.com/docs/guides/gpt/chat-completions-response-format
            message = response.choices[0].message['content']
            commit_messages.append(message)

        return commit_messages
