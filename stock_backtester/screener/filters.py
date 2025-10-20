"""
具体筛选器实现
"""
import pandas as pd
from typing import List, Dict, Union
from .base import Filter
from .indicators import MAIndicator, WRIindicator
from ..logger import get_logger

logger = get_logger(__name__)


class MAFilter(Filter):
    """移动平均线筛选器"""
    
    def __init__(self, period1: int = 5, period2: int = 10, condition: str = "gt"):
        """
        初始化移动平均线筛选器
        
        Args:
            period1 (int): 第一个MA周期
            period2 (int): 第二个MA周期
            condition (str): 比较条件 ("gt"表示MA1 > MA2, "lt"表示MA1 < MA2)
        """
        super().__init__(f"MA{period1}_vs_MA{period2}")
        self.period1 = period1
        self.period2 = period2
        self.condition = condition
        self.ma1_indicator = MAIndicator(period1)
        self.ma2_indicator = MAIndicator(period2)
        logger.debug(f"初始化移动平均线筛选器，条件: MA{period1} {condition} MA{period2}")
    
    def filter(self, stock_codes: List[str], start_time: str = None, end_time: str = None) -> List[str]:
        """
        执行移动平均线筛选
        
        Args:
            stock_codes (List[str]): 股票代码列表
            start_time (str): 数据开始时间
            end_time (str): 数据结束时间
            
        Returns:
            List[str]: 通过筛选的股票代码列表
        """
        try:
            logger.info("开始执行移动平均线筛选")
            filtered_stocks = []
            
            for stock_code in stock_codes:
                try:
                    # 下载股票数据
                    from ..engine import download_single_stock
                    data = download_single_stock(stock_code, start_time, end_time, '1d', 'pre')
                    
                    if data is None or data.empty:
                        logger.debug(f"股票 {stock_code} 数据为空，跳过")
                        # 根据spec要求，数据下载失败应视为该股票筛选失败
                        continue
                    
                    # 计算两个移动平均线
                    data_with_ma1 = self.ma1_indicator.calculate(data.copy())
                    data_with_ma2 = self.ma2_indicator.calculate(data_with_ma1.copy())
                    
                    # 获取最后一行数据进行比较
                    last_row = data_with_ma2.iloc[-1]
                    ma1_column = f'MA{self.period1}'
                    ma2_column = f'MA{self.period2}'
                    
                    # 检查是否有足够的数据
                    if pd.isna(last_row[ma1_column]) or pd.isna(last_row[ma2_column]):
                        logger.debug(f"股票 {stock_code} MA数据不足，跳过")
                        continue
                    
                    # 根据条件判断是否通过筛选
                    ma1_value = last_row[ma1_column]
                    ma2_value = last_row[ma2_column]
                    
                    if self.condition == "gt" and ma1_value > ma2_value:
                        filtered_stocks.append(stock_code)
                        logger.debug(f"股票 {stock_code} 通过MA筛选: {ma1_value} > {ma2_value}")
                    elif self.condition == "lt" and ma1_value < ma2_value:
                        filtered_stocks.append(stock_code)
                        logger.debug(f"股票 {stock_code} 通过MA筛选: {ma1_value} < {ma2_value}")
                    else:
                        logger.debug(f"股票 {stock_code} 未通过MA筛选")
                        
                except Exception as e:
                    logger.error(f"筛选股票 {stock_code} 时出错: {str(e)}")
                    continue
            
            logger.info(f"移动平均线筛选完成，通过筛选的股票数量: {len(filtered_stocks)}")
            return filtered_stocks
            
        except Exception as e:
            logger.error(f"执行移动平均线筛选时出错: {str(e)}")
            raise


class WRFilter(Filter):
    """威廉指标筛选器"""
    
    def __init__(self, period: int = 14, threshold: float = -80, condition: str = "lt", data_period: str = "1d"):
        """
        初始化威廉指标筛选器
        
        Args:
            period (int): WR周期
            threshold (float): 阈值
            condition (str): 比较条件 ("lt"表示WR < threshold，"gt"表示WR > threshold)
            data_period (str): 数据周期，支持'1m', '5m', '30m', '1d'等
        """
        super().__init__(f"WR{period}_{data_period}")
        self.period = period
        self.threshold = threshold
        self.condition = condition
        self.data_period = data_period
        self.wr_indicator = WRIindicator(period)
        logger.debug(f"初始化威廉指标筛选器，条件: WR{period} {condition} {threshold} 数据周期: {data_period}")
    
    def filter(self, stock_codes: List[str], start_time: str = None, end_time: str = None) -> List[str]:
        """
        执行威廉指标筛选
        
        Args:
            stock_codes (List[str]): 股票代码列表
            start_time (str): 数据开始时间
            end_time (str): 数据结束时间
            
        Returns:
            List[str]: 通过筛选的股票代码列表
        """
        try:
            logger.info(f"开始执行威廉指标筛选，数据周期: {self.data_period}")
            filtered_stocks = []
            
            for stock_code in stock_codes:
                try:
                    # 下载股票数据
                    from ..engine import download_single_stock
                    data = download_single_stock(stock_code, start_time, end_time, self.data_period, 'pre')
                    
                    if data is None or data.empty:
                        logger.debug(f"股票 {stock_code} 数据为空，跳过")
                        # 根据spec要求，数据下载失败应视为该股票筛选失败
                        continue
                    
                    # 计算威廉指标
                    data_with_wr = self.wr_indicator.calculate(data.copy())
                    
                    # 获取最后一行数据进行比较
                    last_row = data_with_wr.iloc[-1]
                    wr_column = f'WR{self.period}'
                    
                    # 检查是否有足够的数据
                    if pd.isna(last_row[wr_column]):
                        logger.debug(f"股票 {stock_code} WR数据不足，跳过")
                        continue
                    
                    # 根据条件判断是否通过筛选
                    wr_value = last_row[wr_column]
                    
                    if self.condition == "lt" and wr_value < self.threshold:
                        filtered_stocks.append(stock_code)
                        logger.debug(f"股票 {stock_code} 通过WR筛选: {wr_value} < {self.threshold}")
                    elif self.condition == "gt" and wr_value > self.threshold:
                        filtered_stocks.append(stock_code)
                        logger.debug(f"股票 {stock_code} 通过WR筛选: {wr_value} > {self.threshold}")
                    else:
                        logger.debug(f"股票 {stock_code} 未通过WR筛选")
                        
                except Exception as e:
                    logger.error(f"筛选股票 {stock_code} 时出错: {str(e)}")
                    continue
            
            logger.info(f"威廉指标筛选完成，通过筛选的股票数量: {len(filtered_stocks)}")
            return filtered_stocks
            
        except Exception as e:
            logger.error(f"执行威廉指标筛选时出错: {str(e)}")
            raise


class GeneralComparisonFilter(Filter):
    """通用比较筛选器"""
    
    def __init__(self, 
                 left_operand: Union[str, int, float], 
                 right_operand: Union[str, int, float], 
                 condition: str = "gt"):
        """
        初始化通用比较筛选器
        
        Args:
            left_operand: 左操作数，可以是指标名称(如"MA5")、价格字段(如"close")或数值
            right_operand: 右操作数，可以是指标名称、价格字段或数值
            condition: 比较条件 ("gt"表示>, "lt"表示<, "eq"表示=, "gte"表示>=, "lte"表示<=)
        """
        super().__init__(f"GeneralComparison_{left_operand}_{condition}_{right_operand}")
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.condition = condition
        
        # 解析操作数类型
        self.left_type = self._parse_operand_type(left_operand)
        self.right_type = self._parse_operand_type(right_operand)
        
        # 如果是指标类型，创建相应的指标对象
        self.left_indicator = self._create_indicator(left_operand) if self.left_type == "indicator" else None
        self.right_indicator = self._create_indicator(right_operand) if self.right_type == "indicator" else None
        
        logger.debug(f"初始化通用比较筛选器: {left_operand} {condition} {right_operand}")
    
    def _parse_operand_type(self, operand: Union[str, int, float]) -> str:
        """解析操作数类型"""
        if isinstance(operand, (int, float)):
            return "value"
        elif isinstance(operand, str):
            # 检查是否为指标
            if operand.startswith(('MA', 'WR')):
                return "indicator"
            # 检查是否为价格字段
            elif operand in ['open', 'high', 'low', 'close', 'volume', 'amount']:
                return "field"
            else:
                raise ValueError(f"未知的操作数类型: {operand}")
        else:
            raise ValueError(f"不支持的操作数类型: {type(operand)}")
    
    def _create_indicator(self, indicator_str: str):
        """根据指标字符串创建指标对象"""
        if indicator_str.startswith('MA'):
            period = int(indicator_str[2:])  # 提取周期，如MA5中的5
            return MAIndicator(period)
        elif indicator_str.startswith('WR'):
            period = int(indicator_str[2:])  # 提取周期，如WR14中的14
            return WRIindicator(period)
        else:
            raise ValueError(f"不支持的指标类型: {indicator_str}")
    
    def _get_value(self, data: pd.DataFrame, operand: Union[str, int, float], operand_type: str):
        """获取操作数的值"""
        if operand_type == "value":
            return operand
        elif operand_type == "field":
            # 获取价格字段的最新值
            return data.iloc[-1][operand]
        elif operand_type == "indicator":
            # 计算指标值并返回最新值
            indicator_data = self._create_indicator(operand).calculate(data.copy())
            indicator_column = operand
            return indicator_data.iloc[-1][indicator_column]
        else:
            raise ValueError(f"未知的操作数类型: {operand_type}")
    
    def filter(self, stock_codes: List[str], start_time: str = None, end_time: str = None) -> List[str]:
        """
        执行通用比较筛选
        
        Args:
            stock_codes (List[str]): 股票代码列表
            start_time (str): 数据开始时间
            end_time (str): 数据结束时间
            
        Returns:
            List[str]: 通过筛选的股票代码列表
        """
        try:
            logger.info(f"开始执行通用比较筛选: {self.left_operand} {self.condition} {self.right_operand}")
            filtered_stocks = []
            
            for stock_code in stock_codes:
                try:
                    # 下载股票数据
                    from ..engine import download_single_stock
                    data = download_single_stock(stock_code, start_time, end_time, '1d', 'pre')
                    
                    if data is None or data.empty:
                        logger.debug(f"股票 {stock_code} 数据为空，跳过")
                        # 根据spec要求，数据下载失败应视为该股票筛选失败
                        continue
                    
                    # 获取左操作数的值
                    left_value = self._get_value(data, self.left_operand, self.left_type)
                    
                    # 获取右操作数的值
                    right_value = self._get_value(data, self.right_operand, self.right_type)
                    
                    # 检查是否有足够的数据
                    if pd.isna(left_value) or pd.isna(right_value):
                        logger.debug(f"股票 {stock_code} 比较数据不足，跳过")
                        continue
                    
                    # 根据条件判断是否通过筛选
                    passed = False
                    if self.condition == "gt" and left_value > right_value:
                        passed = True
                    elif self.condition == "lt" and left_value < right_value:
                        passed = True
                    elif self.condition == "eq" and left_value == right_value:
                        passed = True
                    elif self.condition == "gte" and left_value >= right_value:
                        passed = True
                    elif self.condition == "lte" and left_value <= right_value:
                        passed = True
                    
                    if passed:
                        filtered_stocks.append(stock_code)
                        logger.debug(f"股票 {stock_code} 通过筛选: {left_value} {self.condition} {right_value}")
                    else:
                        logger.debug(f"股票 {stock_code} 未通过筛选: {left_value} {self.condition} {right_value}")
                        
                except Exception as e:
                    logger.error(f"筛选股票 {stock_code} 时出错: {str(e)}")
                    continue
            
            logger.info(f"通用比较筛选完成，通过筛选的股票数量: {len(filtered_stocks)}")
            return filtered_stocks
            
        except Exception as e:
            logger.error(f"执行通用比较筛选时出错: {str(e)}")
            raise