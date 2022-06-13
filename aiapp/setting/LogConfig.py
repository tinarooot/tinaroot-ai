'''
mlstudio后端引擎核心配置文件，注意部署服务前先拉到最后，确认4个开关选项
1.
'''
# 配置日志输出路径
from loguru import logger
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上一级
current_dir = os.path.dirname(current_dir)
# 获取上上一级
current_dir = os.path.dirname(current_dir)

# 配置日志输入路径
master_log_path = f'{current_dir}/logs/master.log'
# 设置每天12点生成一个文件
logger.add(master_log_path, rotation="12:00")
logger.info(f"当前应用根路径为[path={current_dir}]")
