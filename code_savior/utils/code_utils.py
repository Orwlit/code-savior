import ast

class PythonCodeRetriever:
    def __init__(self):
        pass

    def get_function_by_name(self, file_path: str, function_name: str) -> str:
        with open(file_path, 'r') as f:
            code = f.read()

        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                start_line = node.lineno - 1  # ast 的行号从 1 开始
                end_line = node.end_lineno  # ast 的 end_lineno 已经是正确的行号

                function_code_lines = code.split('\n')[start_line:end_line]
                function_code = '\n'.join(function_code_lines)

                return function_code

        return f"Function {function_name} not found in {file_path}."

    def get_function_by_code_snippet(self, file_path: str, code_snippet: list, start_line: int, end_line: int) -> str:
        with open(file_path, 'r') as f:
            code = f.read()

        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_start_line = node.lineno - 1  # ast 的行号从 1 开始
                func_end_line = node.end_lineno  # ast 的 end_lineno 已经是正确的行号

                # 检查函数是否包含给定的代码片段
                if func_start_line <= start_line and func_end_line >= end_line:
                    snippet_in_func = code.split('\n')[start_line-1:end_line]
                    if snippet_in_func == code_snippet:
                        function_code_lines = code.split('\n')[func_start_line:func_end_line]
                        function_code = '\n'.join(function_code_lines)
                        return function_code

        return "Function containing the given code snippet not found."



# # 使用示例: name
# retriever = PythonCodeRetriever()
# file_path = '/root/code-savior/code_savior/utils/git_utils.py'  # 替换为实际的文件路径
# function_name = '_extract_file_metadata'  # 替换为实际的函数名
# print(retriever.get_function_by_name(file_path, function_name))



# 使用示例: snippet
retriever = PythonCodeRetriever()
file_path = '/root/code-savior/code_savior/utils/code_utils.py'  # 替换为实际的文件路径
# 替换为实际的代码片段
code_snippet = [
    "        for node in ast.walk(tree):", 
    "            if isinstance(node, ast.FunctionDef) and node.name == function_name:", 
    "                start_line = node.lineno - 1  # ast 的行号从 1 开始", 
    "                end_line = node.end_lineno  # ast 的 end_lineno 已经是正确的行号",
]

start_line = 13  # 替换为实际的起始行号（从 0 开始）
end_line = 16  # 替换为实际的结束行号
print(retriever.get_function_by_code_snippet(file_path, code_snippet, start_line, end_line))




class CppCodeRetriever:
    def __init__(self):
        pass
