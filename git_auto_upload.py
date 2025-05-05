import subprocess
import os


def git_upload(directory):
    try:
        # 取消 Git 代理设置
        subprocess.run(['git', 'config', '--global', '--unset', 'http.proxy'], capture_output=True)
        subprocess.run(['git', 'config', '--global', '--unset', 'https.proxy'], capture_output=True)

        # 切换到指定目录
        os.chdir(directory)
        print(f"当前工作目录: {os.getcwd()}")
        # 检查是否有更改
        result = subprocess.run(['git','status', '--porcelain'], capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print("工作区有更改，开始提交和推送...")
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
            # 推送到远程仓库
            push_result = subprocess.run(['git', 'push'], capture_output=True, text=True, encoding='utf-8')
            if push_result.returncode != 0:
                print(f"推送时出错: {push_result.stderr}")
                # 尝试获取更详细的网络错误信息
                try:
                    import socket
                    import errno
                    # 模拟检查网络连接
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(5)
                    s.connect(('github.com', 443))
                    s.close()
                except socket.error as se:
                    if se.errno == errno.ECONNREFUSED:
                        print("无法连接到 GitHub 服务器，请检查网络或 GitHub 状态。")
                    elif se.errno == errno.ETIMEDOUT:
                        print("连接超时，请检查网络连接。")
                    else:
                        print(f"网络连接出现未知错误: {se}")
            else:
                print("文件已成功上传到 Git 仓库。")
        else:
            print("工作区没有更改，无需提交。")
    except subprocess.CalledProcessError as e:
        print(f"Git 操作出错: {e}")


if __name__ == "__main__":
    # 替换为你的本地文档仓库目录
    directory = r'D:\new\java_usages'
    git_upload(directory)
    