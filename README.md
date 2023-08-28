# code-savior

[English](#english-version) | [中文](#中文版本)

---

## English Version

### Introduction

`code-savior` is a Python package that empowers AI to automatically generate git commit messages. It supports multiple languages and has plans to extend its capabilities to auto-generate code documentation in the future.

### Installation and Usage

1. Install the package via pip:
   ```shell
   pip install code-savior
   ```
2. Add files to the staging area using git:
    ```shell
    git add .
    ```
3. Run `code-savior`:
    ```shell
    code-savior
    ```
The tool will automatically generate a commit message and prompt you for confirmation before committing.

### Configuration Options
#### Configuring `.env`

Refer to the env.example file for available configurations:

1. OpenAI related configurations:

    - `CS_OPENAI_API_KEY`: The API key for OpenAI, used for authentication and API requests.
    - `CS_OPENAI_BASE_PATH`: The base path for OpenAI's API, default is https://api.openai.com.
    - `CS_OPENAI_MODEL`: The OpenAI model to use, default is gpt-3.5-turbo.
    - `CS_OPENAI_MAX_TOKEN`: The maximum token limit for OpenAI requests, default is 1000.

2. code-savior related configurations:
    - `CS_MAX_LENGTH`: The maximum length of the message, default is 1000.
    - `CS_LANGUAGE`: Set the language (ISO 639-1 format), default is en.
    - `CS_MAX_ITERATION`: The number of messages to generate, default is 1.
    - `CS_RESPONSE_TYPE`: Set the response type, default is empty.
    - `CS_PROXY`: Set the network proxy, default is empty.
    - `CS_TIMEOUT`: Set the network timeout in seconds, default is 10.
    - `CS_EXCLUDE_FILES`: List of files not to be added to the git staging area, separated by commas.
#### Command Line Arguments
The above environment variables can also be configured using command line arguments. Below are the purposes and examples of the command line arguments:
1. OpenAI related configurations:
    - `--api_key`: Set the OpenAI API key. For example: `--api_key=YOUR_API_KEY`
    - `--base_path`: Set the base path for OpenAI's API. For example: `--base_path=https://api.openai.com`
    - `--model`: Set the OpenAI model to use. For example: `--model=gpt-3.5-turbo`
    - `--max_token`: Set the maximum token limit for OpenAI requests. For example: `--max_token=1000`
2. code-savior related configurations:
    - `--max_length`: Set the maximum length of the message. For example: `--max_length=1000`
    - `--language`: Set the language (ISO 639-1 format). For example: `--language=en`
    - `--max_iteration`: Set the number of messages to generate. For example: `--max_iteration=3`
    - `--response_type`: Set the response type. For example: `--response_type=TYPE`
    - `--proxy`: Set the network proxy. For example: `--proxy=http://your_proxy.com`
    - `--timeout`: Set the network timeout in seconds. For example: `--timeout=10`
    - `--exclude_files`: Set the list of files not to be added to the git staging area. For example: `--exclude_files file1.py file2.py`

Note: In this command, apart from `--exclude_files` which adds files you don't want to track, all other command line arguments will override the corresponding settings in the `.env` file.

### Code review
Comming soon.

### Auto-generate Code Documentation
Comming soon.


## 中文版本
### 介绍
code-savior 是一个Python包，可以让AI自动生成git commit的描述文字。它支持多种语言，并计划在未来扩展其功能，以自动生成代码文档。

### 安装和使用方法
1. 通过pip安装此包：
    ```shell
    pip install code-savior
    ```
2. 使用git命令将文件添加到暂存区：
    ```shell
    git add .
    ```
3. 运行 `code-savior`：
    ```shell
    code-savior
    ```
工具会自动为您生成commit消息，并在提交前询问您是否确认。

### 相关可选项的配置
#### 配置.env
参考env.example文件，可配置项如下：

1. OpenAI相关配置：
    - `CS_OPENAI_API_KEY`：OpenAI的API密钥，用于身份验证和API请求。
    - `CS_OPENAI_BASE_PATH`：OpenAI的API基础路径，默认为https://api.openai.com。
    - `CS_OPENAI_MODEL`：要使用的OpenAI模型，默认为gpt-3.5-turbo。
    - `CS_OPENAI_MAX_TOKEN`：OpenAI请求的最大令牌限制，默认为1000。
2. code-savior相关配置：
    - `CS_MAX_LENGTH`：消息的最大长度，默认为1000。
    - `CS_LANGUAGE`：设置语言（ISO 639-1格式），默认为en。
    - `CS_MAX_ITERATION`：要生成的消息数量，默认为1。
    - `CS_RESPONSE_TYPE`：设置响应类型，默认为空。
    - `CS_PROXY`：设置网络代理，默认为空。
    - `CS_TIMEOUT`：设置网络超时（以秒为单位），默认为10。
    - `CS_EXCLUDE_FILES`：不添加到git暂存区的文件列表，文件之间用逗号分隔。
#### 命令行参数
上述环境变量均能用命令行参数配置，以下是命令行参数的作用和示例：
1. OpenAI相关配置：
    - `--api_key`：设置OpenAI API密钥。例如：`--api_key=YOUR_API_KEY`
    - `--base_path`：设置OpenAI的API基础路径。例如：`--base_path=https://api.openai.com`
    - `--model`：设置要使用的OpenAI模型。例如：`--model=gpt-3.5-turbo`
    - `--max_token`：设置OpenAI请求的最大令牌限制。例如：`--max_token=1000`
2. code-savior相关配置：
    - `--max_length`：设置消息的最大长度。例如：`--max_length=1000`
    - `--language`：设置语言（ISO 639-1格式）。例如：`--language=en`
    - `--max_iteration`：设置要生成的消息数量。例如：`--max_iteration=3`
    - `--response_type`：设置响应类型。例如：`--response_type=TYPE`
    - `--proxy`：设置网络代理。例如：`--proxy=http://your_proxy.com`
    - `--timeout`：设置网络超时（以秒为单位）。例如：`--timeout=10`
    - `--exclude_files`：设置不添加到git暂存区的文件列表。例如：`--exclude_files file1.py file2.py`

注意：在本次命令中，除了`--exclude_files`会添加不希望跟踪的文件，其余命令行参数均会覆盖`.env`文件中的相应设置。

### 代码审查
敬请期待

### 自动输出代码文档
敬请期待。