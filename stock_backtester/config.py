"""
配置模块，用于读取和解析config.yaml配置文件
"""
import yaml
import os
from .logger import get_logger

# 获取日志记录器
logger = get_logger(__name__)


class Config:
    """配置类，用于加载和管理配置项"""
    
    def __init__(self, config_path="config.yaml"):
        """
        初始化配置对象
        
        Args:
            config_path (str): 配置文件路径
        """
        self.config_path = config_path
        self.excel_path = None
        self.max_threads = None
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        logger.info("开始加载配置文件")
        
        # 检查配置文件是否存在
        if not os.path.exists(self.config_path):
            logger.error(f"配置文件 {self.config_path} 不存在")
            raise FileNotFoundError(f"配置文件 {self.config_path} 不存在")
        
        # 读取配置文件
        with open(self.config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
        
        logger.info("配置文件加载成功")
        
        # 检查必需的配置项
        if 'excel_path' not in config_data:
            logger.error("配置文件中缺少必需的配置项: excel_path")
            raise KeyError("配置文件中缺少必需的配置项: excel_path")
        
        if 'max_threads' not in config_data:
            logger.error("配置文件中缺少必需的配置项: max_threads")
            raise KeyError("配置文件中缺少必需的配置项: max_threads")
        
        # 设置配置项
        self.excel_path = config_data['excel_path']
        self.max_threads = config_data['max_threads']
        
        logger.info(f"配置项设置完成: excel_path={self.excel_path}, max_threads={self.max_threads}")