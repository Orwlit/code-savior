import os

class MarkdownDocumentManager:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory

    def _create_or_open_file(self, filename: str) -> str:
        # 创建或打开一个 Markdown 文件
        file_path = os.path.join(self.base_directory, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("# " + filename.replace(".md", "") + "\n\n")
        return file_path

    def append_to_document(self, filename: str, content: str) -> None:
        # 将文本追加到指定的 Markdown 文件
        file_path = self._create_or_open_file(filename)
        with open(file_path, 'a') as file:
            file.write(content + "\n\n")

    def create_new_document(self, filename: str, content: str) -> None:
        # 创建一个新的 Markdown 文件并写入内容
        file_path = self._create_or_open_file(filename)
        with open(file_path, 'w') as file:
            file.write("# " + filename.replace(".md", "") + "\n\n")
            file.write(content + "\n\n")

# 使用示例
doc_manager = MarkdownDocumentManager("/path/to/directory")
doc_manager.append_to_document("sample.md", "This is a sample content.")
doc_manager.create_new_document("new_sample.md", "This is content for a new document.")

