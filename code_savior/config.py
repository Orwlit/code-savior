import argparse
import os

# 设置默认值
DEFAULT_OPENAI_API_KEY = None
DEFAULT_OPENAI_BASE_PATH = "https://api.openai.com"
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
DEFAULT_OPENAI_MAX_TOKEN = 1000

DEFAULT_MAX_LENGTH = 1000
DEFAULT_LANGUAGE = "en"
DEFAULT_N_GENERATE = 1
DEFAULT_RESPONSE_TYPE = ""

DEFAULT_PROXY = None
DEFAULT_TIMEOUT = 10

# 从环境变量中读取配置
CS_OPENAI_API_KEY = os.environ.get('CS_OPENAI_API_KEY', DEFAULT_OPENAI_API_KEY)
CS_OPENAI_BASE_PATH = os.environ.get('CS_OPENAI_BASE_PATH', DEFAULT_OPENAI_BASE_PATH)
CS_OPENAI_MODEL = os.environ.get('CS_OPENAI_MODEL', DEFAULT_OPENAI_MODEL)
CS_OPENAI_MAX_TOKEN = int(os.environ.get('CS_OPENAI_MAX_TOKEN', DEFAULT_OPENAI_MAX_TOKEN))

CS_MAX_LENGTH = int(os.environ.get('CS_MAX_LENGTH', DEFAULT_MAX_LENGTH))
CS_LANGUAGE = os.environ.get('CS_LANGUAGE', DEFAULT_LANGUAGE)
CS_N_GENERATE = int(os.environ.get('CS_N_GENERATE', DEFAULT_N_GENERATE))
CS_RESPONSE_TYPE = os.environ.get('CS_RESPONSE_TYPE', DEFAULT_RESPONSE_TYPE)

CS_PROXY = os.environ.get('CS_PROXY', DEFAULT_PROXY)
CS_TIMEOUT = int(os.environ.get('CS_TIMEOUT', DEFAULT_TIMEOUT))

exclude_files = [] # 不添加到git暂存区的文件

# 参数映射
param_mapping = {
    'api_key'       : 'CS_OPENAI_API_KEY',
    'base_path'     : 'CS_OPENAI_BASE_PATH',
    'model'         : 'CS_OPENAI_MODEL',
    'max_token'     : 'CS_OPENAI_MAX_TOKEN',
    'max_length'    : 'CS_MAX_LENGTH',
    'language'      : 'CS_LANGUAGE',
    'n_generate'    : 'CS_N_GENERATE',
    'response_type' : 'CS_RESPONSE_TYPE',
    'proxy'         : 'CS_PROXY',
    'timeout'       : 'CS_TIMEOUT',
}

def configure_from_args():
    parser = argparse.ArgumentParser(description='Configure settings for the code-savior package.')
    parser.add_argument('--api-key', type=str, help='Set the OpenAI API key.')
    parser.add_argument('--base-path', type=str, help='Set the OpenAI base path.')
    parser.add_argument('--model', type=str, help='Set the OpenAI model.')
    parser.add_argument('--max-token', type=int, help='Set the maximum token limit for OpenAI.')
    parser.add_argument('--max-length', type=int, help='Set the maximum message length.')
    parser.add_argument('--language', type=str, help='Set the language (ISO 639-1 format).')
    parser.add_argument('--n-generate', type=int, help='Set the number of messages to generate.')
    parser.add_argument('--response-type', type=str, help='Set the response type.')
    parser.add_argument('--proxy', type=str, help='Set the network proxy.')
    parser.add_argument('--timeout', type=int, help='Set the network timeout in seconds.')

    args = parser.parse_args()

    for param, value in vars(args).items():
        if value is not None:
            globals()[param_mapping[param]] = value


def get_config_values():
    return {
        'CS_OPENAI_API_KEY': CS_OPENAI_API_KEY,
        'CS_OPENAI_BASE_PATH': CS_OPENAI_BASE_PATH,
        'CS_OPENAI_MODEL': CS_OPENAI_MODEL,
        'CS_OPENAI_MAX_TOKEN': CS_OPENAI_MAX_TOKEN,
        'CS_MAX_LENGTH': CS_MAX_LENGTH,
        'CS_LANGUAGE': CS_LANGUAGE,
        'CS_N_GENERATE': CS_N_GENERATE,
        'CS_RESPONSE_TYPE': CS_RESPONSE_TYPE,
        'CS_PROXY': CS_PROXY,
        'CS_TIMEOUT': CS_TIMEOUT,
    }

import logging

# Logging Configuration
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LEVEL = logging.DEBUG

# Main logger
logger = logging.getLogger('main')
logger.setLevel(LOGGING_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter(LOGGING_FORMAT)
ch.setFormatter(formatter)
logger.addHandler(ch)

# git_utils logger
git_logger = logging.getLogger('git_utils')
git_logger.setLevel(LOGGING_LEVEL)
ch_git = logging.StreamHandler()
ch_git.setLevel(LOGGING_LEVEL)
ch_git.setFormatter(formatter)
git_logger.addHandler(ch_git)

# ai_model logger
ai_logger = logging.getLogger('ai_model')
ai_logger.setLevel(LOGGING_LEVEL)
ch_ai = logging.StreamHandler()
ch_ai.setLevel(LOGGING_LEVEL)
ch_ai.setFormatter(formatter)
ai_logger.addHandler(ch_ai)

# doc_utils logger
doc_logger = logging.getLogger('doc_utils')
doc_logger.setLevel(LOGGING_LEVEL)
ch_doc = logging.StreamHandler()
ch_doc.setLevel(LOGGING_LEVEL)
ch_doc.setFormatter(formatter)
doc_logger.addHandler(ch_doc)

# utils logger
utils_logger = logging.getLogger('utils')
utils_logger.setLevel(LOGGING_LEVEL)
ch_utils = logging.StreamHandler()
ch_utils.setLevel(LOGGING_LEVEL)
ch_utils.setFormatter(formatter)
utils_logger.addHandler(ch_utils)
