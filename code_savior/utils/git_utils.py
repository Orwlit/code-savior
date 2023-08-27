from code_savior.config import git_logger

        match = re.match(r"@@ -(?:(\d+),)?(\d+) \+(?:(\d+),)?(\d+) @@", context)
        old_start = int(match.group(1)) if match.group(1) else 1
        old_count = int(match.group(2))
        new_start = int(match.group(3)) if match.group(3) else 1
        new_count = int(match.group(4))


        # 添加所有更改的文件
        subprocess.run(["git", "add", "."], check=True)
        
def git_commit(commit_message:str, exclude_files:List[str]=[]) -> None:
    # # 添加所有更改的文件
    # subprocess.run(["git", "add", "."], check=True)
    
    # 从缓存区移除不想添加的文件
    for file in exclude_files:
        subprocess.run(["git", "reset", file], check=True)
    
    # 提交更改
    subprocess.run(["git", "commit", "-m", commit_message], check=True)



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