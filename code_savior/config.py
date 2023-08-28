import argparse
import os
from dotenv import load_dotenv

load_dotenv()

# 设置默认值
DEFAULT_OPENAI_API_KEY = None
DEFAULT_OPENAI_BASE_PATH = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
DEFAULT_OPENAI_MAX_TOKEN = 1000

DEFAULT_MAX_LENGTH = 1000
DEFAULT_LANGUAGE = "en"
DEFAULT_MAX_ITERATION = 1
DEFAULT_RESPONSE_TYPE = ""

DEFAULT_HTTP_PROXY = None
DEFAULT_HTTPS_PROXY = None
DEFAULT_TIMEOUT = 10

# 从环境变量中读取配置
CS_OPENAI_API_KEY = os.environ.get('CS_OPENAI_API_KEY', DEFAULT_OPENAI_API_KEY)
CS_OPENAI_BASE_PATH = os.environ.get('CS_OPENAI_BASE_PATH', DEFAULT_OPENAI_BASE_PATH)
CS_OPENAI_MODEL = os.environ.get('CS_OPENAI_MODEL', DEFAULT_OPENAI_MODEL)
CS_OPENAI_MAX_TOKEN = int(os.environ.get('CS_OPENAI_MAX_TOKEN', DEFAULT_OPENAI_MAX_TOKEN))

CS_MAX_LENGTH = int(os.environ.get('CS_MAX_LENGTH', DEFAULT_MAX_LENGTH))
CS_LANGUAGE = os.environ.get('CS_LANGUAGE', DEFAULT_LANGUAGE)
CS_MAX_ITERATION = int(os.environ.get('CS_MAX_ITERATION', DEFAULT_MAX_ITERATION))
CS_RESPONSE_TYPE = os.environ.get('CS_RESPONSE_TYPE', DEFAULT_RESPONSE_TYPE)

CS_HTTP_PROXY = os.environ.get("HTTP_PROXY", DEFAULT_HTTP_PROXY)
CS_HTTPS_PROXY = os.environ.get("HTTPS_PROXY", DEFAULT_HTTPS_PROXY)
CS_PROXY = {
    "http": CS_HTTP_PROXY,
    "https": CS_HTTPS_PROXY
}
CS_TIMEOUT = int(os.environ.get('CS_TIMEOUT', DEFAULT_TIMEOUT))

exclude_files_str = os.environ.get('CS_EXCLUDE_FILES', '')
CS_EXCLUDE_FILES = exclude_files_str.split(',') if exclude_files_str else []


# 参数映射
param_mapping = {
    'api_key'       : 'CS_OPENAI_API_KEY',
    'base_path'     : 'CS_OPENAI_BASE_PATH',
    'model'         : 'CS_OPENAI_MODEL',
    'max_token'     : 'CS_OPENAI_MAX_TOKEN',
    'max_length'    : 'CS_MAX_LENGTH',
    'language'      : 'CS_LANGUAGE',
    'max_iteration' : 'CS_MAX_ITERATION',
    'response_type' : 'CS_RESPONSE_TYPE',
    'http_proxy'    : 'CS_HTTP_PROXY',
    'https_proxy'   : 'CS_HTTPS_PROXY',
    'timeout'       : 'CS_TIMEOUT',
    'exclude_files' : 'CS_EXCLUDE_FILES',
}

def configure_from_args():
    parser = argparse.ArgumentParser(description='Configure settings for the code-savior package.')
    parser.add_argument('--api_key', type=str, help='Set the OpenAI API key.')
    parser.add_argument('--base_path', type=str, help='Set the OpenAI base path.')
    parser.add_argument('--model', type=str, help='Set the OpenAI model.')
    parser.add_argument('--max_token', type=int, help='Set the maximum token limit for OpenAI.')
    parser.add_argument('--max_length', type=int, help='Set the maximum message length.')
    parser.add_argument('--language', type=str, help='Set the language (ISO 639-1 format).')
    parser.add_argument('--max_iteration', type=int, help='Set the number of messages to generate.')
    parser.add_argument('--response_type', type=str, help='Set the response type.')
    parser.add_argument('--http_proxy', type=str, help='Set the http proxy.')
    parser.add_argument('--https_proxy', type=str, help='Set the https proxy.')
    parser.add_argument('--timeout', type=int, help='Set the network timeout in seconds.')
    parser.add_argument('--exclude_files', nargs='+', help='List of files to exclude.')

    args = parser.parse_args()

    for param, value in vars(args).items():
        if value is not None:
            if param == 'exclude_files':
                CS_EXCLUDE_FILES.extend(value)
            else:
                globals()[param_mapping[param]] = value


def get_config_values():
    return {
        'CS_OPENAI_API_KEY': CS_OPENAI_API_KEY,
        'CS_OPENAI_BASE_PATH': CS_OPENAI_BASE_PATH,
        'CS_OPENAI_MODEL': CS_OPENAI_MODEL,
        'CS_OPENAI_MAX_TOKEN': CS_OPENAI_MAX_TOKEN,

        'CS_MAX_LENGTH': CS_MAX_LENGTH,
        'CS_LANGUAGE': CS_LANGUAGE,
        'CS_MAX_ITERATION': CS_MAX_ITERATION,
        'CS_RESPONSE_TYPE': CS_RESPONSE_TYPE,
        'CS_PROXY': CS_PROXY,
        'CS_TIMEOUT': CS_TIMEOUT,

        'CS_EXCLUDE_FILES': CS_EXCLUDE_FILES,
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
