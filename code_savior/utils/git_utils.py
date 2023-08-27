import subprocess
import re
from typing import List, Dict, Union

from code_savior.config import git_logger

git_logger.info("This is an info message from git_utils.py.")

class GitDiffProcessor:
    def __init__(self, diff_content: str):
        if not diff_content:
            git_logger.error("Received empty git diff content.")
            raise ValueError("Received empty git diff content.")
        self.diff_content = diff_content

    def _extract_file_metadata(self) -> List[Dict[str, Union[str, bool]]]:
        # 提取文件的元数据，如文件状态、模式、索引等
        metadata = []
        lines = self.diff_content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("diff --git"):
                file_data = {
                    "old_path": line.split(" ")[2][2:], # 更改前的文件路径。
                    "new_path": line.split(" ")[3][2:], # 更改后的文件路径。
                    "is_new_file": False, # 一个布尔值，表示文件是否是新创建的。
                    "is_deleted_file": False, # 一个布尔值，表示文件是否已被删除。
                    "old_index": None, # 文件的旧索引（如果有的话）。
                    "new_index": None, # 文件的新索引（如果有的话）。
                    "file_mode": None # 文件的模式（例如，100644表示一个普通文件）。
                }
                if i + 1 < len(lines) and lines[i + 1].startswith("new file mode"):
                    file_data["is_new_file"] = True
                    file_data["file_mode"] = lines[i + 1].split(" ")[3]
                elif i + 1 < len(lines) and lines[i + 1].startswith("deleted file mode"):
                    file_data["is_deleted_file"] = True
                elif i + 1 < len(lines) and lines[i + 1].startswith("index"):
                    indices = lines[i + 1].split(" ")[1].split("..")
                    file_data["old_index"] = indices[0]
                    file_data["new_index"] = indices[1]
                metadata.append(file_data)
        
        if not metadata:
            git_logger.warning("No file metadata found in git diff content.")
        return metadata

    def _interpret_change_context(self, context: str) -> str:
        match = re.match(r"@@ -(?:(\d+),)?(\d+) \+(?:(\d+),)?(\d+) @@", context)
        if not match:
            git_logger.error(f"Unexpected change context format: {context}")
            raise ValueError(f"Unexpected change context format: {context}")
        
        old_start = int(match.group(1)) if match.group(1) else 1
        old_count = int(match.group(2))
        new_start = int(match.group(3)) if match.group(3) else 1
        new_count = int(match.group(4))

        if old_count == 0 and new_count > 0:
            return f"Added lines {new_start} to {new_start + new_count - 1} in the new version."
        elif old_count > 0 and new_count == 0:
            return f"Removed lines {old_start} to {old_start + old_count - 1} from the old version."
        else:
            return f"Changed lines {old_start} to {old_start + old_count - 1} in the old version to lines {new_start} to {new_start + new_count - 1} in the new version."





    def _extract_changes(self) -> Dict[str, List[Dict[str, List[str]]]]:
        # 提取文件的更改内容
        changes = {}
        lines = self.diff_content.split("\n")
        current_file = None
        current_change = []
        for i, line in enumerate(lines):
            if line.startswith("diff --git"):
                current_file = line.split(" ")[3][2:]
                changes[current_file] = []
            elif line.startswith("@@"):
                if current_change:
                    changes[current_file].append({
                        "info": current_change[0],
                        "lines": current_change[1:]
                    })
                    current_change = []
                current_change.append(line)
            elif current_change:
                current_change.append(line)
        if current_change:
            changes[current_file].append({
                "info": current_change[0],
                "lines": current_change[1:]
            })

        if not changes:
            git_logger.warning("No changes found in git diff content.")
        return changes

    def process_diff(self) -> Dict[str, Union[List[Dict[str, str]], Dict[str, List[Dict[str, Union[str, List[str]]]]]]]:
        # 主要的解析函数，调用上述方法并返回解析后的结果
        result = {
            "file_metadata": self._extract_file_metadata(),
            "changes": self._extract_changes()
        }

        for changes_list in result["changes"].values():
            for change in changes_list:
                change["info"] = self._interpret_change_context(change["info"])

        return result


# 用来快速使用parsed_data所构建的类
class GitDiffData:
    def __init__(self, data: Dict[str, object]):
        self.data = data

    def get_changed_files(self) -> List[str]:
        """返回所有更改的文件路径"""
        return list(self.data['changes'].keys())

    def get_changes_for_file(self, file_path: str) -> List[Dict[str, List[str]]]:
        """返回指定文件的所有更改"""
        return self.data['changes'].get(file_path, [])

    def get_specific_change(self, file_path: str, index: int) -> Dict[str, List[str]]:
        """返回指定文件的特定更改"""
        changes = self.get_changes_for_file(file_path)
        if 0 <= index < len(changes):
            return changes[index]
        return {}

    def display_changes(self):
        """显示所有更改的摘要"""
        for file in self.get_changed_files():
            print(f"Changes for {file}:")
            for change in self.get_changes_for_file(file):
                print(change['info'])
                for line in change['lines']:
                    print(line)
            print("\n")



def get_git_diff_cached_output() -> str:
    try:
        # # 添加所有更改的文件
        # subprocess.run(["git", "add", "."], check=True)

        result = subprocess.run(['git', 'diff', '--cached'], stdout=subprocess.PIPE, check=True)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError:
        git_logger.error("Error executing git diff --cached. Are you in a git repository?")
        raise RuntimeError("Error executing git diff --cached. Are you in a git repository?")
    except Exception as e:
        git_logger.error(f"Unexpected error occurred: {e}")
        raise

def git_commit(commit_message:str, exclude_files:List[str]=[]) -> None:
    # # 添加所有更改的文件
    # subprocess.run(["git", "add", "."], check=True)
    
    # 从缓存区移除不想添加的文件
    for file in exclude_files:
        subprocess.run(["git", "reset", file], check=True)
    
    # 提交更改
    subprocess.run(["git", "commit", "-m", commit_message], check=True)



# # GitDiffProcessor使用示例
# diff_content = get_git_diff_cached_output()
# processor = GitDiffProcessor(diff_content)
# parsed_data = processor.process_diff()
# print(parsed_data)

# language = "Chinese"
# file_changes = ""
# for file_data in parsed_data["file_metadata"]:
#     old_path = file_data["old_path"]
#     new_path = file_data["new_path"]
#     is_new = file_data["is_new_file"]
#     is_deleted = file_data["is_deleted_file"]
#     old_index = file_data["old_index"]
#     new_index = file_data["new_index"]
#     file_mode = file_data["file_mode"]
    
#     if old_path != new_path:
#         file_changes += f"For the file '{old_path}', index changed from {old_index} to {new_index}:\n"
#     else:
#         file_changes += f"For the file '{old_path}' (index {old_index}) changed to '{new_path}' (index {new_index}):\n"
    
#     if is_new:
#         file_changes += "This is a new file.\n"
#     elif is_deleted:
#         file_changes += "This file was deleted.\n"
#     if file_mode:
#         file_changes += f"File mode: {file_mode}\n"
    
#     changes = parsed_data["changes"].get(new_path, [])
#     for change in changes:
#         file_changes += f"Change context: {change['info']}\n"
#         for line in change['lines']:
#             file_changes += f"{line}\n"
#         file_changes += "\n"

# prompt = f"In {language}, please summarize the following changes:\n{file_changes}"
# print(prompt)

# # "parsed_data"数据结构的使用示例
# diff_data = GitDiffData(parsed_data)

# # 获取所有更改的文件
# changed_files = diff_data.get_changed_files() 
# print(f"\n\n获取所有更改的文件\n{changed_files}\n")

# # 获取特定文件的所有更改
# changes_for_file = diff_data.get_changes_for_file('code.py')
# print(f"获取特定文件的所有更改\n{changes_for_file}\n")

# # 获取特定文件的特定更改
# specific_change = diff_data.get_specific_change('code.py', 0)
# print(f"获取特定文件的特定更改\n{specific_change}\n")

# # 显示所有更改的摘要
# diff_data.display_changes()
