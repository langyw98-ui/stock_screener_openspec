"""
技术指标计算模块
"""
import pandas as pd
import numpy as np
from .base import Indicator
from ..logger import get_logger

logger = get_logger(__name__)


class MAIndicator(Indicator):
    """移动平均线指标"""
    
    def __init__(self, period: int = 5):
        """
        初始化移动平均线指标
        
        Args:
            period (int): 计算周期
        """
        super().__init__(f"MA{period}")
        self.period = period
        logger.debug(f"初始化移动平均线指标，周期: {period}")
    
    def calculate(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """
        计算移动平均线
        
        Args:
            stock_data (pd.DataFrame): 股票数据
            
        Returns:
            pd.DataFrame: 包含移动平均线的股票数据
        """
        try:
            logger.debug(f"计算移动平均线，周期: {self.period}")
            # 确保数据按日期排序
            stock_data = stock_data.sort_values('date').reset_index(drop=True)
            
            # 计算移动平均线
            ma_column = f'MA{self.period}'
            stock_data[ma_column] = stock_data['close'].rolling(window=self.period).mean()
            
            logger.debug(f"移动平均线计算完成，新增列: {ma_column}")
            return stock_data
        except Exception as e:
            logger.error(f"计算移动平均线时出错: {str(e)}")
            raise


class WRIindicator(Indicator):
    """威廉指标"""
    
    def __init__(self, period: int = 14):
        """
        初始化威廉指标
        
        Args:
            period (int): 计算周期
        """
        super().__init__(f"WR{period}")
        self.period = period
        logger.debug(f"初始化威廉指标，周期: {period}")
    
    def calculate(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """
        计算威廉指标
        
        Args:
            stock_data (pd.DataFrame): 股票数据
            
        Returns:
            pd.DataFrame: 包含威廉指标的股票数据
        """
        try:
            logger.debug(f"计算威廉指标，周期: {self.period}")
            # 确保数据按日期排序
            stock_data = stock_data.sort_values('date').reset_index(drop=True)
            
            # 计算威廉指标
            wr_column = f'WR{self.period}'
            
            # 计算周期内的最高价和最低价
            high_period = stock_data['high'].rolling(window=self.period).max()
            low_period = stock_data['low'].rolling(window=self.period).min()
            
            # 计算威廉指标
            # 避免除零错误
            denominator = high_period - low_period
            # 当最高价等于最低价时，威廉指标设为-50（中性值）
            stock_data[wr_column] = np.where(
                denominator == 0,
                -50.0,
                (high_period - stock_data['close']) / denominator * -100
            )
            
            logger.debug(f"威廉指标计算完成，新增列: {wr_column}")
            return stock_data
        except Exception as e:
            logger.error(f"计算威廉指标时出错: {str(e)}")
            raise