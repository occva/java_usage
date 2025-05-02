import subprocess
import time
import os


def git_upload(directory):
    try:
        # 切换到指定目录
        os.chdir(directory)
        print(f"当前工作目录: {os.getcwd()}")
        # 检查是否有更改
        result = subprocess.run(['git','status', '--porcelain'], capture_output=True, text=True)
        if result.stdout:
            print("工作区有更改，开始提交和推送...")
            # 添加所有文件
            add_result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
            if add_result.returncode != 0:
                print(f"添加文件时出错: {add_result.stderr}")
            else:
                print("文件已添加到暂存区。")
            # 提交更改
            commit_result = subprocess.run(['git', 'commit', '-m', 'Auto commit'], capture_output=True, text=True)
            if commit_result.returncode != 0:
                print(f"提交更改时出错: {commit_result.stderr}")
            else:
                print("更改已提交。")
            # 推送到远程仓库
            push_result = subprocess.run(['git', 'push'], capture_output=True, text=True)
            if push_result.returncode != 0:
                print(f"推送时出错: {push_result.stderr}")
            else:
                print("文件已成功上传到 Git 仓库。")
        else:
            print("工作区没有更改，无需提交。")
    except subprocess.CalledProcessError as e:
        print(f"Git 操作出错: {e}")


if __name__ == "__main__":
    # 替换为你的本地文档仓库目录
    directory = r"D:\new\java八股"
    while True:
        git_upload(directory)
        # 每 6 小时执行一次（6 * 60 * 60 秒）
        time.sleep(6 * 60 * 60)