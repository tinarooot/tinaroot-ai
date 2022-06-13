#!/data/devops/miniconda2/envs/flaskapp_env_v1.0/bin/python
'''
本模块作为统一命令行入口，目前支持以下几个操作：
[devops@devops flaskappDemo]$ ./command_manager.py 
Usage: command_manager.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  master-start
'''

import click
import signal
import os
from loguru import logger


# 增加信号检测机制，捕捉ctrl + z信号，因为部分环境下ctrl + c不起作用
def handler(signum, frame):
    print('检测到信号[Ctrl+Z]，程序将被终止')
    os.system('kill -s 9 %d' % os.getpid())


# signal.signal(signal.SIGTSTP, handler)
signal.signal(signal.SIGABRT , handler)


@click.group()
def cli():
    pass


# 定义启动master命令
@cli.command()
@click.option('--port', default=4000, help='端口')
@click.option('--ip', default='0.0.0.0', help='ip')
def master_start(ip, port):
    from aiapp.app import app
    # 判断端口是否可用
    def tryPort(port):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = False
        try:
            sock.bind(("0.0.0.0", port))
            result = True
        except:
            print("Port is in use")
        sock.close()
        return result

    if not tryPort(port):
        raise Exception(f"端口[port={port}]被占用！请在命令行参数中选择其它端口！")
    logger.warning(f"注意，要停止当前服务，请输入[ctrl + z]")
    app.run(host="0.0.0.0", port=port, threaded=True)


if __name__ == '__main__':
    cli()
