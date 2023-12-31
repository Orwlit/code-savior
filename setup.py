from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-savior",
    version="1.0",
    author="Yuzhe Wang (GitHub: Orwlit)",  # 添加您的名字
    author_email="orwlit31@outlook.com",  # 添加您的邮箱
    description="good to generate a brief commit",  # 添加简短的描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Orwlit/code-savior",  # 添加项目的 GitHub 链接或其他项目主页链接
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 如果您使用的是其他许可证，请更改此处
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "inquirer",
        "rich",
        "argparse",
        "openai",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'code-savior=code_savior.main:main',  # 这将允许用户在命令行中使用 `code-savior` 命令
        ],
    },
    python_requires='>=3.10',  # 指定支持的最低Python版本，还需要测试
)
