import subprocess
import os


def commit_and_remove_previous_five(directory):
    try:
        # 切换到指定目录
        os.chdir(directory)
        print(f"当前工作目录: {os.getcwd()}")

        # 检查是否有更改
        status_result = subprocess.run(['git','status', '--porcelain'], capture_output=True, text=True, encoding='utf-8')
        if status_result.stdout:
            print("工作区有更改，开始提交...")
            # 添加所有文件
            add_result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True, encoding='utf-8')
            if add_result.returncode != 0:
                print(f"添加文件时出错: {add_result.stderr}")
            else:
                print("文件已添加到暂存区。")
            # 提交更改
            commit_result = subprocess.run(['git', 'commit', '-m', 'Auto commit'], capture_output=True, text=True, encoding='utf-8')
            if commit_result.returncode != 0:
                print(f"提交更改时出错: {commit_result.stderr}")
            else:
                print("更改已提交。")

        # 获取前 5 次提交的哈希值
        log_result = subprocess.run(['git', 'log', '--pretty=format:%H', '-n', '5', 'HEAD~1'], capture_output=True, text=True, encoding='utf-8')
        if log_result.returncode != 0:
            print(f"获取提交哈希值时出错: {log_result.stderr}")
            return
        commit_hashes = log_result.stdout.strip().split('\n')

        # 回退到前 5 次提交之前的状态
        previous_commit = f"HEAD~{len(commit_hashes)}"
        reset_result = subprocess.run(['git', 'reset', '--hard', previous_commit], capture_output=True, text=True, encoding='utf-8')
        if reset_result.returncode != 0:
            print(f"重置提交时出错: {reset_result.stderr}")
            return
        print("已回退到前 5 次提交之前的状态。")

        # 强制推送到远程仓库以删除远程的提交记录
        push_result = subprocess.run(['git', 'push', '-f', 'origin', 'master'], capture_output=True, text=True, encoding='utf-8')
        if push_result.returncode != 0:
            print(f"推送时出错: {push_result.stderr}")
        else:
            print("已成功删除远程仓库的前 5 次提交记录。")

    except subprocess.CalledProcessError as e:
        print(f"Git 操作出错: {e}")
    except FileNotFoundError:
        print(f"指定的目录 {directory} 不存在。")


if __name__ == "__main__":
    # 替换为你的本地 Git 仓库目录
    directory = r'D:\new\java_usages'
    commit_and_remove_previous_five(directory)
    