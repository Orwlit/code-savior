# # OpenAI
# CS_OPENAI_API_KEY = None
# CS_OPENAI_BASE_PATH = None
# CS_OPENAI_MODEL = "gpt-3.5-turbo"
# CS_OPENAI_MAX_LENGTH = 1000  # 最长生成单词数

# # Messages
# CS_LANGUAGE = "en"
# CS_N_GENERATE = 3  # 单次生成commit message的数量
# CS_RESPONSE_TYPE = ""  # 生成内容满足的格式

# # Network
# CS_PROXY = None
# CS_TIMEOUT = 10000  # 10 seconds

# # Logging Configuration
# LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# LOGGING_LEVEL = logging.DEBUG




import configparser
import argparse
import os

# 初始化配置解析器
config = configparser.ConfigParser()

# 读取配置文件
config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
config.read(config_file_path)

# 参数映射
param_mapping = {
    'api_key': ('OpenAI', 'API_KEY'),
    'base_path': ('OpenAI', 'BASE_PATH'),
    'model': ('OpenAI', 'MODEL'),
    'max_length': ('OpenAI', 'MAX_LENGTH'),
    'language': ('Messages', 'LANGUAGE'),
    'n_generate': ('Messages', 'N_GENERATE'),
    'response_type': ('Messages', 'RESPONSE_TYPE'),
    'proxy': ('Network', 'PROXY'),
    'timeout': ('Network', 'TIMEOUT')
}

# 使用argparse处理命令行参数
parser = argparse.ArgumentParser(description='Configure settings for the application.')

# 定义所有的命令行参数
for param in param_mapping.keys():
    parser.add_argument(f'--{param.replace("_", "-")}', type=str, help=f'Set {param.replace("_", " ")}.')

args = parser.parse_args()

# 遍历所有的参数，检查哪些参数被设置了，并更新相应的配置
for param, value in vars(args).items():
    if value:
        section, key = param_mapping[param]
        config.set(section, key, value)
        # 保存更新到config.ini
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)

# 从config.ini获取配置
CS_OPENAI_API_KEY = config.get('OpenAI', 'API_KEY', fallback=None)
CS_OPENAI_BASE_PATH = config.get('OpenAI', 'BASE_PATH', fallback="https://api.openai.com")
CS_OPENAI_MODEL = config.get('OpenAI', 'MODEL', fallback="gpt-3.5-turbo")
CS_OPENAI_MAX_TOKEN = config.getint('OpenAI', 'MAX_TOKEN', fallback=1000)

CS_MAX_LENGTH = config.getint('Messages', 'MAX_LENGTH', fallback=1000)
CS_LANGUAGE = config.get('Messages', 'LANGUAGE', fallback="en") # ISO 639-1格式
CS_N_GENERATE = config.getint('Messages', 'N_GENERATE', fallback=3)
CS_RESPONSE_TYPE = config.get('Messages', 'RESPONSE_TYPE', fallback="")

CS_PROXY = config.get('Network', 'PROXY', fallback=None)
CS_TIMEOUT = config.getint('Network', 'TIMEOUT', fallback=10) # 10 seconds

exclude_files = [] # 不添加到git暂存区的文件


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
