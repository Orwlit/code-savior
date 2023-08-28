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
        prompt_template = "The following content lists some files that are about to undergo a git commit and the corresponding modifications within these files:\n"

        # 用特定语言回答
        language = self.language_mapping.get(self.commit_language, "Unknown Language")
        
        # file_changes = ""
        for file_data in parsed_data["file_metadata"]:
            old_path = file_data["old_path"]
            new_path = file_data["new_path"]
            is_new = file_data["is_new_file"]
            is_deleted = file_data["is_deleted_file"]
            # old_index = file_data["old_index"]
            # new_index = file_data["new_index"]
            # file_mode = file_data["file_mode"]
            


            if old_path != new_path:
                prompt_template += f"In file: '{new_path}' (changed from '{old_path}'), the specific modifications are as follows:\n"
            elif is_new:
                prompt_template += f"In file: '{new_path}' (new file), the specific modifications are as follows:\n"
            elif is_deleted:
                prompt_template += f"In file: '{old_path}' (deleted)\n"
                continue
            else:
                prompt_template += f"In file: '{new_path}' (modified), the specific modifications are as follows:\n"

            changes = parsed_data["changes"].get(new_path, []) # changes: 当前文件的所有更改
            n_changes = len(changes)
            prompt_template += f"There are {n_changes} changes in total.\n"
            
            for i in range(n_changes):
                prompt_template += f"Change context number {i+1}:\n"
                for line in changes[i]['lines']:
                    prompt_template += f"{line}\n"
                prompt_template += "\n"

        prompt_summarize = f"These files are all to be committed in this 'git commit'. Next, please answer in {language} and complete the following tasks:\n"
        prompt_summarize += "1. Speculate the purpose of this commit, such as what features were implemented, which codes were optimized, etc. If you analyze that these code modifications have multiple purposes, please explain these purposes separately.\n"
        prompt_summarize += "2. Summarize the modification content of each file and explain how these modifications serve the purpose of this commit.\n"
        prompt_summarize += "\n"

        prompt_answer_format =  "You will answer in the tone of the code's author and generate a git commit message within {self.commit_max_length} words.\n"
        prompt_answer_format += "You will answer the above questions in the following format:\n"
        prompt_answer_format += "Brief: [You will answer the purpose of this commit here]\n"
        prompt_answer_format += "File modifications:\n"
        prompt_answer_format += "- [File name]: [You will answer the modification content of each file in sequence here and explain how these modifications serve the purpose of this commit]\n"
        prompt_answer_format += "\n"

        prompt_end = "Your answer:"

        prompt_template += prompt_summarize
        prompt_template += prompt_answer_format
        prompt_template += prompt_end

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
