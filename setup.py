from setuptools import setup, find_packages

setup(
    name="code-savior",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # 列出你的依赖项
    ],
    entry_points={
        'console_scripts': [
            'code-savior=code_savior.main:main',  # 这将允许用户在命令行中使用 `code-savior` 命令
        ],
    },
)

