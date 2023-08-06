import paramiko


class LzLinux:
    def __init__(self, server_ip, user, pwd, port=22):
        """ 初始化ssh客户端 """

        self.server_ip = server_ip
        self.user = user
        self.pwd = pwd

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client = client
            print(f'------------开始连接服务器 {server_ip}-----------')

            # 创建 ssh 命令 客户端
            self.client.connect(server_ip, port, username=user, password=pwd, timeout=5)

            # 创建 sftp 客户端
            trans = paramiko.Transport(sock=(server_ip, 22))
            trans.connect(username=user, password=pwd)
            self.sftp = paramiko.SFTPClient.from_transport(trans)

            print('------------认证成功!.....-----------')
        except Exception:
            print(f'连接远程linux服务器(ip:{server_ip})发生异常!请检查用户名和密码是否正确!')

    def execute_cmd(self, cmd):
        """
            发送命令到服务器
        :param cmd:
        :return:
        """
        try:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            content = stdout.read().decode()
            return content
        except Exception as e:
            print('link_server-->返回命令发生异常,内容:', e)
        finally:
            # self.client.close()
            pass

    def sftp_put(self, local_file_path, remote_file_path):
        """
            上传文件到服务器
        :param local_file_path:
        :param remote_file_path:
        :return:
        """
        # put('你要上传的文件','上传的位置+文件名')
        # 'D:/temp/lz_test.txt', '/home/hadoopuser/pydir/python-notebook/README.md'
        self.sftp.put(local_file_path, remote_file_path)

    def sftp_get(self, remote_file_path, local_file_path):
        """
            从服务器下载文件
        :param remote_file_path:
        :param local_file_path:
        :return:
        """
        # get('你要下载的文件','下载的位置+文件名')
        # '/home/hadoopuser/pydir/python-notebook/README.md', 'D:/temp/lz_test.txt'
        self.sftp.get(remote_file_path, local_file_path)

    def close_client(self):
        """
            关闭 ssh 连接
        :return:
        """
        self.client.close()

    def close_sftp(self):
        """
            关闭 sftp 连接
        :return:
        """
        self.sftp.close()


# server = LzLinux('192.168.156.3', 'hadoopuser', '1')
#
# cmd = 'tree -N /home/hadoopuser/pydir'
# res = server.execute_cmd(cmd)
# print(res)
