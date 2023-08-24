class GitDiffProcessor:
    def __init__(self, diff_content: str):
        self.diff_content = diff_content

    def _extract_file_paths(self) -> list[str]:
        # 提取发生变化的文件名和路径
        paths = []
        lines = self.diff_content.split("\n")
        for line in lines:
            if line.startswith("diff --git"):
                paths.append(line.split(" ")[-1])
        return paths

    def _extract_changed_functions(self) -> dict:
        # 提取发生变化的函数及其变化前后的内容
        # 这个函数的实现可能会比较复杂，因为需要解析函数的开始和结束
        # 这里只是一个简化的示例
        functions = {}
        lines = self.diff_content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("@@"):
                function_name = lines[i-1]  # 假设函数名在@@上面的行
                functions[function_name] = line
        return functions

    def _extract_other_info(self) -> dict:
        # 提取其他相关信息，如行号等
        # 这个函数的实现可能会比较复杂，因为需要解析行号和其他细节
        # 这里只是一个简化的示例
        info = {}
        lines = self.diff_content.split("\n")
        for line in lines:
            if line.startswith("@@"):
                info["line_info"] = line
        return info

    def process_diff(self) -> dict:
        # 主要的解析函数，调用上述方法并返回解析后的结果
        result = {
            "file_paths": self._extract_file_paths(),
            "changed_functions": self._extract_changed_functions(),
            "other_info": self._extract_other_info()
        }
        return result

# 使用示例
diff_content = "..."  # 这是从git diff获取的内容
processor = GitDiffProcessor(diff_content)
parsed_data = processor.process_diff()
print(parsed_data)

