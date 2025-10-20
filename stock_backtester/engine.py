"""
核心引擎模块，负责任务调度和并发执行
"""
import pandas as pd
import concurrent.futures
from tqdm import tqdm
import datetime
import os
from .logger import get_logger

# 获取日志记录器
logger = get_logger(__name__)


def calculate_time_range(start_date=None, end_date=None):
    """
    根据start_date和end_date参数计算数据下载的时间范围
    
    Args:
        start_date (str): 开始日期，格式为YYYY-MM-DD
        end_date (str): 结束日期，格式为YYYY-MM-DD
        
    Returns:
        tuple: (start_date, end_date) 格式化后的日期字符串
    """
    logger.info("开始计算时间范围")
    today = datetime.date.today()
    
    # 如果没有提供开始日期和结束日期
    if start_date is None and end_date is None:
        # 下载从当前系统日期起向前倒推6个月的数据
        end_date = today
        start_date = end_date - datetime.timedelta(days=180)  # 大约6个月
        logger.info("未提供日期参数，使用默认6个月时间范围")
    
    # 如果只提供开始日期
    elif start_date is not None and end_date is None:
        # 下载从start_date到当前系统日期的所有数据
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = today
        logger.info(f"只提供开始日期，结束日期设为今天: {end_date}")
    
    # 如果只提供结束日期
    elif start_date is None and end_date is not None:
        # 下载从end_date当天起向前倒推6个月的数据
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        start_date = end_date - datetime.timedelta(days=180)  # 大约6个月
        logger.info(f"只提供结束日期，开始日期设为6个月前: {start_date}")
    
    # 如果同时提供开始日期和结束日期
    else:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        logger.info(f"提供了开始和结束日期: {start_date} 到 {end_date}")
    
    result = start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    logger.info(f"时间范围计算完成: {result}")
    return result


def download_single_stock(stock_code, start_date, end_date, period='1d', adjustment='pre'):
    """
    下载单只股票的数据
    
    Args:
        stock_code (str): 股票代码
        start_date (str): 开始日期
        end_date (str): 结束日期
        period (str): 数据周期
        adjustment (str): 复权方式
        
    Returns:
        pandas.DataFrame: 股票数据
    """
    try:
        logger.info(f"开始下载股票 {stock_code} 的数据")
        
        # 导入xtquant_feed模块
        from stock_backtester.feeds.xtquant_feed import download_stock_data, format_stock_code
        
        # 格式化股票代码
        formatted_code = format_stock_code(stock_code)
        if formatted_code is None:
            logger.error(f"无效的股票代码格式: {stock_code}")
            raise ValueError(f"无效的股票代码格式: {stock_code}")
        
        # 下载数据
        data = download_stock_data(formatted_code, start_date, end_date, period, adjustment)
        
        logger.info(f"股票 {stock_code} 数据下载完成")
        return data
    except Exception as e:
        # 记录错误但不终止程序
        logger.error(f"下载股票 {stock_code} 数据时出错: {str(e)}")
        print(f"下载股票 {stock_code} 数据时出错: {str(e)}")
        return stock_code, None


def download_all_stocks(stock_list, start_date, end_date, period='1d', adjustment='pre', max_threads=4):
    """
    并发下载所有股票的数据
    
    Args:
        stock_list (list): 股票代码列表
        start_date (str): 开始日期
        end_date (str): 结束日期
        period (str): 数据周期
        adjustment (str): 复权方式
        max_threads (int): 最大线程数
        
    Returns:
        dict: 股票代码到数据的映射
    """
    logger.info(f"开始并发下载所有股票数据，股票数量: {len(stock_list)}, 最大线程数: {max_threads}")
    
    # 存储结果的字典
    results = {}
    
    # 使用线程池执行器
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # 提交所有任务
        future_to_stock = {
            executor.submit(download_single_stock, stock, start_date, end_date, period, adjustment): stock
            for stock in stock_list
        }
        
        # 使用tqdm显示进度条
        for future in tqdm(concurrent.futures.as_completed(future_to_stock), 
                          total=len(future_to_stock), 
                          desc="下载进度"):
            stock = future_to_stock[future]
            try:
                data = future.result()
                results[stock] = data
                logger.debug(f"股票 {stock} 数据处理完成")
            except Exception as e:
                logger.error(f"处理股票 {stock} 时发生未预期的错误: {str(e)}")
                print(f"处理股票 {stock} 时发生未预期的错误: {str(e)}")
                results[stock] = None
    
    logger.info("所有股票数据下载完成")
    return results