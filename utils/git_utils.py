import re
from typing import List, Dict, Union

class GitDiffProcessor:
    def __init__(self, diff_content: str):
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
        return metadata

    def _interpret_change_context(self, context: str) -> str:
        match = re.match(r"@@ -(\d+,\d+) \+(\d+,\d+) @@", context)
        if match:
            old = match.group(1)
            new = match.group(2)
        old_start, old_count = map(int, old.split(","))
        new_start, new_count = map(int, new.split(","))

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



import subprocess
def get_git_diff_cached_output() -> str:
    result = subprocess.run(['git', 'diff', '--cached'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


# GitDiffProcessor使用示例
diff_content = get_git_diff_cached_output()
processor = GitDiffProcessor(diff_content)
parsed_data = processor.process_diff()
print(parsed_data)





# "parsed_data"数据结构的使用示例
diff_data = GitDiffData(parsed_data)

# 获取所有更改的文件
changed_files = diff_data.get_changed_files() 
print(f"\n\n获取所有更改的文件\n{changed_files}\n")

# 获取特定文件的所有更改
changes_for_file = diff_data.get_changes_for_file('code.py')
print(f"获取特定文件的所有更改\n{changes_for_file}\n")

# 获取特定文件的特定更改
specific_change = diff_data.get_specific_change('code.py', 0)
print(f"获取特定文件的特定更改\n{specific_change}\n")

# 显示所有更改的摘要
diff_data.display_changes()


# 遗留问题
# 假设我想把我写的这个文件做成pypi包发布出去，其中提取git diff --cached的函数如下。这个文件名字是git_utils.py，它一定会被我项目中其他组件调用。我在想像这样一个获得git diff的功能性函数应该放在哪里，是项目的主函数还是git_utils.py，还是另开一个单独的通用性的工具文件utils.py。而且我也不太明白这个函数有没有必要设成静态函数或其他相关修饰也好操作也罢，我不想让这个函数出错，也用最好的方式在我的工程中实现这个函数

# import subprocess
# def get_git_diff_cached_output() -> str:
#     result = subprocess.run(['git', 'diff', '--cached'], stdout=subprocess.PIPE)
#     return result.stdout.decode('utf-8')