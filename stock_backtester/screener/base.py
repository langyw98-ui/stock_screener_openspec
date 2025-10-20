"""
筛选器基类和接口定义
"""
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..logger import get_logger

logger = get_logger(__name__)


class Filter(ABC):
    """筛选器基类"""
    
    def __init__(self, name: str):
        """
        初始化筛选器
        
        Args:
            name (str): 筛选器名称
        """
        self.name = name
        logger.debug(f"初始化筛选器: {name}")
    
    @abstractmethod
    def filter(self, stock_codes: List[str], start_time: str = None, end_time: str = None) -> List[str]:
        """
        执行筛选逻辑
        
        Args:
            stock_codes (List[str]): 股票代码列表
            start_time (str): 数据开始时间
            end_time (str): 数据结束时间
            
        Returns:
            List[str]: 通过筛选的股票代码列表
        """
        pass


class Indicator(ABC):
    """技术指标基类"""
    
    def __init__(self, name: str):
        """
        初始化技术指标
        
        Args:
            name (str): 指标名称
        """
        self.name = name
        logger.debug(f"初始化技术指标: {name}")
    
    @abstractmethod
    def calculate(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """
        计算技术指标
        
        Args:
            stock_data (pd.DataFrame): 股票数据
            
        Returns:
            pd.DataFrame: 包含技术指标的股票数据
        """
        pass