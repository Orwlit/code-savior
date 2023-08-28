from typing import List

import openai

from code_savior.config import get_config_values
from code_savior.config import ai_logger

class CommitDocAI:
    def __init__(self):
        self.config_values = get_config_values()
        self.get_config()

        openai.api_key  = self.config_values['CS_OPENAI_API_KEY']
        openai.api_base = self.config_values['CS_OPENAI_BASE_PATH']
        openai.proxy    = self.config_values['CS_PROXY']

    def get_config(self):
        # 获取配置，例如语言、是否使用emoji等
        self.commit_max_length      = self.config_values['CS_MAX_LENGTH']
        self.commit_max_iteration   = self.config_values['CS_MAX_ITERATION']
        self.commit_language        = self.config_values['CS_LANGUAGE']
        self.commit_response_type   = self.config_values['CS_RESPONSE_TYPE']

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
        # Initial prompt setup
        prompt_template = "You are to act as the author of a commit message in git. Here are the changes:\n"

        # Use specific language for the answer
        language = self.language_mapping.get(self.commit_language, "Unknown Language")

        # Iterate through file metadata to generate the file changes description
        for file_data in parsed_data["file_metadata"]:
            old_path = file_data["old_path"]
            new_path = file_data["new_path"]
            is_new = file_data["is_new_file"]
            is_deleted = file_data["is_deleted_file"]

            # Describe the type of change for each file
            if old_path != new_path:
                prompt_template += f"In file: '{new_path}' (changed from '{old_path}'), the modifications are:\n"
            elif is_new:
                prompt_template += f"In file: '{new_path}' (new file), the modifications are:\n"
            elif is_deleted:
                prompt_template += f"In file: '{old_path}' (deleted)\n"
                continue
            else:
                prompt_template += f"In file: '{new_path}', the modifications are:\n"

            # Describe the specific changes in each file
            changes = parsed_data["changes"].get(new_path, [])
            for i, change in enumerate(changes):
                prompt_template += f"Change {i+1}:\n"
                for line in change['lines']:
                    prompt_template += f"{line}\n"
                prompt_template += "\n"

        # Instructions for the model
        prompt_instructions = f"Based on the above changes, please answer in {language} and generate a git commit message. Summarize the purpose and main modifications concisely. For example: 'improve the clarity of the prompt, removes commented out code'.\n"

        # Format for the answer
        prompt_format = "Answer format (markdown format):\n"
        prompt_format += "Brief: [Summarize the purpose and main modifications]\n"
        prompt_format += "File modifications:\n"
        prompt_format += "- [File name]: [Briefly describe the modifications and their purpose]\n"

        # Combine all parts of the prompt
        prompt_template += prompt_instructions
        prompt_template += prompt_format

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
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user", 
                    "content": commit_prompt
                }
            ],
        }

        commit_messages = []

        for _ in range(self.config_values['CS_MAX_ITERATION']):
            response = openai.ChatCompletion.create(timeout=10, **kwargs)
            # response格式详情见：https://platform.openai.com/docs/guides/gpt/chat-completions-response-format
            message = response.choices[0].message['content']
            commit_messages.append(message)

        return commit_messages
