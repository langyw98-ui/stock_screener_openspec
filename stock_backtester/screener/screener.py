"""
筛选器管理器
"""
import pandas as pd
from typing import List, Dict, Any
from .base import Filter
from .filters import MAFilter, WRFilter
from ..logger import get_logger
from ..config import Config

logger = get_logger(__name__)


class Screener:
    """筛选器管理器，支持链式筛选方式"""
    
    def __init__(self, start_time: str = None, end_time: str = None):
        """
        初始化筛选器管理器
        
        Args:
            start_time (str): 数据开始时间
            end_time (str): 数据结束时间
        """
        self.filters: List[Filter] = []
        self.filtered_stocks: List[str] = []
        self.start_time = start_time
        self.end_time = end_time
        logger.debug(f"初始化筛选器管理器，时间范围: {start_time} - {end_time}")
    
    def set_data_range(self, start_time: str, end_time: str):
        """
        设置数据范围
        
        Args:
            start_time (str): 数据开始时间
            end_time (str): 数据结束时间
        """
        self.start_time = start_time
        self.end_time = end_time
        logger.debug(f"设置数据范围: {start_time} - {end_time}")
    

    
    def add_filter(self, filter_obj: Filter) -> 'Screener':
        """
        添加筛选器到筛选链
        
        Args:
            filter_obj (Filter): 筛选器对象
            
        Returns:
            Screener: 筛选器管理器实例，支持链式调用
        """
        self.filters.append(filter_obj)
        logger.debug(f"添加筛选器到筛选链: {filter_obj.name}")
        return self  # 支持链式调用
    
    def remove_filter(self, filter_name: str) -> bool:
        """
        从筛选链中移除筛选器
        
        Args:
            filter_name (str): 筛选器名称
            
        Returns:
            bool: 是否成功移除
        """
        try:
            self.filters = [f for f in self.filters if f.name != filter_name]
            logger.debug(f"从筛选链中移除筛选器: {filter_name}")
            return True
        except Exception as e:
            logger.error(f"移除筛选器 {filter_name} 时出错: {str(e)}")
            return False
    
    def clear_filters(self):
        """清空筛选链"""
        self.filters.clear()
        logger.debug("清空筛选链")
    
    def screen(self, stock_codes: List[str]) -> List[str]:
        """
        执行链式筛选
        
        Args:
            stock_codes (List[str]): 股票代码列表
            
        Returns:
            List[str]: 通过所有筛选条件的股票代码列表
        """
        try:
            logger.info(f"开始执行链式筛选，筛选器数量: {len(self.filters)}")
            
            if not self.filters:
                logger.warning("筛选链为空，返回所有股票")
                return stock_codes
            
            # 初始化结果为所有股票
            current_stocks = stock_codes
            logger.debug(f"初始股票数量: {len(current_stocks)}")
            
            # 依次应用每个筛选器
            for i, filter_obj in enumerate(self.filters):
                try:
                    logger.info(f"应用第 {i+1} 个筛选器: {filter_obj.name}")
                    
                    # 应用筛选器，传递数据范围参数
                    filtered_stocks = filter_obj.filter(current_stocks, self.start_time, self.end_time)
                    
                    # 更新当前股票列表
                    current_stocks = [stock for stock in current_stocks if stock in filtered_stocks]
                    
                    logger.info(f"第 {i+1} 个筛选器应用完成，剩余股票数量: {len(current_stocks)}")
                    
                    # 如果没有股票通过筛选，提前结束
                    if not current_stocks:
                        logger.info("没有股票通过所有筛选条件")
                        break
                        
                except Exception as e:
                    logger.error(f"应用筛选器 {filter_obj.name} 时出错: {str(e)}")
                    # 根据spec要求，部分条件失败应视为整个筛选过程失败
                    raise Exception(f"筛选器 {filter_obj.name} 执行失败: {str(e)}")
            
            self.filtered_stocks = current_stocks
            logger.info(f"链式筛选完成，最终通过筛选的股票数量: {len(current_stocks)}")
            return current_stocks
            
        except Exception as e:
            logger.error(f"执行链式筛选时出错: {str(e)}")
            raise
    
    def get_filtered_stocks(self) -> List[str]:
        """
        获取筛选结果
        
        Returns:
            List[str]: 通过筛选的股票代码列表
        """
        return self.filtered_stocks.copy()
    
    def get_filter_chain(self) -> List[str]:
        """
        获取筛选链信息
        
        Returns:
            List[str]: 筛选器名称列表
        """
        return [f.name for f in self.filters]