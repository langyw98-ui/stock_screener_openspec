"""
数据源模块，封装xtquant数据接口
"""
import re
import pandas as pd
from ..logger import get_logger

# 获取日志记录器
logger = get_logger(__name__)


def format_stock_code(stock_code):
    """
    将A股代码转换为xtquant要求的格式
    
    Args:
        stock_code (str or int): 原始股票代码，支持多种格式如 000001, 600519, 000001.SZ, SZ.000001 等
        
    Returns:
        str: 转换后的股票代码格式，如 000001.SZ, 600519.SH
    """
    logger.debug(f"开始格式化股票代码: {stock_code}")
    
    # 转换为字符串并移除可能存在的空格
    stock_code = str(stock_code).strip()
    
    # 处理已经符合格式的代码 (如 000001.SZ, 600519.SH)
    if re.match(r'^\d{6}\.(SH|SZ)$', stock_code):
        logger.debug(f"股票代码已符合格式: {stock_code}")
        return stock_code
    
    # 处理带前缀的代码 (如 SZ.000001)
    if re.match(r'^(SH|SZ)\.\d{6}$', stock_code):
        prefix, code = stock_code.split('.')
        formatted_code = f"{code}.{prefix}"
        logger.debug(f"格式化带前缀的代码: {stock_code} -> {formatted_code}")
        return formatted_code
    
    # 处理纯数字代码 (如 000001, 600519)
    if re.match(r'^\d+$', stock_code):
        # 检查长度，只有6位数字才是有效的
        if len(stock_code) != 6:
            # 如果不是6位数字，补齐到6位或认为是无效代码
            if len(stock_code) < 6:
                stock_code = stock_code.zfill(6)
                logger.debug(f"股票代码补齐到6位: {stock_code}")
            else:
                # 太长的数字认为是无效代码
                logger.warning(f"股票代码长度超过6位，认为是无效代码: {stock_code}")
                return None
        
        # 根据代码前缀判断市场
        if stock_code.startswith(('6', '60', '68')):  # 6开头的为上海股票
            formatted_code = f"{stock_code}.SH"
        elif stock_code.startswith(('0', '00', '3', '30')):  # 0、3开头的为深圳股票
            formatted_code = f"{stock_code}.SZ"
        else:
            # 默认处理其他情况
            # 这里可以记录错误或抛出异常，但根据需求我们先尝试处理
            formatted_code = f"{stock_code}.SZ"  # 默认当作深圳股票
            logger.warning(f"无法确定股票市场，使用默认深圳市场: {stock_code}")
        
        logger.debug(f"格式化纯数字代码: {stock_code} -> {formatted_code}")
        return formatted_code
    
    # 如果都不匹配，返回None表示无效代码
    logger.warning(f"无效的股票代码格式: {stock_code}")
    return None


def download_stock_data(stock_code, start_date, end_date, period='1d', adjustment='pre'):
    """
    从xtquant下载股票数据
    
    Args:
        stock_code (str): 股票代码，格式为 '600000.SH'
        start_date (str): 开始日期，格式为YYYY-MM-DD
        end_date (str): 结束日期，格式为YYYY-MM-DD
        period (str): 数据周期，支持1m, 5m, 30m, 1d
        adjustment (str): 复权方式，pre(前复权), post(后复权), none(不复权)
        
    Returns:
        pandas.DataFrame: 股票K线数据
    """
    logger.info(f"开始下载股票数据: {stock_code}, 时间范围: {start_date} 到 {end_date}, 周期: {period}, 复权: {adjustment}")
    
    try:
        # 导入xtquant库
        from xtquant import xtconstant, xtdata
        
        # 转换日期格式为xtquant要求的格式 (YYYYMMDD)
        start_date_xt = start_date.replace('-', '')
        end_date_xt = end_date.replace('-', '')
        
        logger.debug(f"转换日期格式: {start_date} -> {start_date_xt}, {end_date} -> {end_date_xt}")
        
        # 下载历史数据
        # 注意：xtquant的download_history_data函数不直接返回数据，而是将数据保存在本地
        # 我们需要使用get_market_data_ex来获取数据
        logger.debug(f"调用xtdata.download_history_data下载历史数据")
        xtdata.download_history_data(stock_code, period, start_date_xt, end_date_xt)
        
        # 获取复权类型
        dividend_type = 'none'  # 默认不复权
        if adjustment == 'pre':
            dividend_type = 'front'  # 前复权
        elif adjustment == 'post':
            dividend_type = 'back'   # 后复权
        
        logger.debug(f"复权类型: {dividend_type}")
        
        # 获取数据
        logger.debug(f"调用xtdata.get_market_data_ex获取数据")
        data = xtdata.get_market_data_ex(
            field_list=['time', 'open', 'high', 'low', 'close', 'volume', 'amount'],  # 正确的参数名是field_list
            stock_list=[stock_code],  # 正确的参数名是stock_list
            period=period,
            start_time=start_date_xt,
            end_time=end_date_xt,
            dividend_type=dividend_type
        )
        
        # 检查是否有数据
        if not data or stock_code not in data or data[stock_code] is None or data[stock_code].empty:
            logger.warning(f"未获取到股票 {stock_code} 的数据")
            return None
        
        # 获取DataFrame
        df = data[stock_code]
        
        # 检查数据记录条数是否为0
        if len(df) == 0:
            logger.warning(f"股票 {stock_code} 的数据记录条数为0")
            return None
        
        logger.debug(f"获取到 {len(df)} 条数据记录")
        
        # 重命名列以匹配需求
        df = df.rename(columns={
            'time': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'amount': 'amount'
        })
        
        # 将时间戳转换为日期格式
        # xtquant返回的时间可能是时间戳格式，需要转换
        if not df.empty:
            # 尝试不同的日期解析方式
            try:
                # 如果是时间戳格式（毫秒）
                df['date'] = pd.to_datetime(df['date'], unit='ms')
                # 将UTC时间转换为北京时间（UTC+8）
                df['date'] = df['date'] + pd.Timedelta(hours=8)
                logger.debug("时间戳格式转换完成")
            except:
                try:
                    # 如果是YYYYMMDD格式
                    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
                    logger.debug("YYYYMMDD格式转换完成")
                except:
                    # 如果是其他格式，让pandas自动推断
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')
                    logger.debug("自动推断日期格式完成")
        
        # 重置索引
        df = df.reset_index(drop=True)
        
        logger.info(f"股票 {stock_code} 数据下载完成，共 {len(df)} 条记录")
        return df
        
    except ImportError:
        # 如果没有安装xtquant，使用模拟数据
        logger.warning("未安装xtquant库，使用模拟数据")
        print("警告: 未安装xtquant库，使用模拟数据")
        return _simulate_download_stock_data(stock_code, start_date, end_date, period, adjustment)
    except Exception as e:
        # 记录错误并返回None
        logger.error(f"下载股票 {stock_code} 数据时出错: {str(e)}")
        print(f"下载股票 {stock_code} 数据时出错: {str(e)}")
        return None


def _simulate_download_stock_data(stock_code, start_date, end_date, period='1d', adjustment='pre'):
    """
    模拟下载股票数据的实现（用于测试或xtquant不可用时）
    
    Args:
        stock_code (str): 股票代码
        start_date (str): 开始日期，格式为YYYY-MM-DD
        end_date (str): 结束日期，格式为YYYY-MM-DD
        period (str): 数据周期，支持1m, 5m, 30m, 1d
        adjustment (str): 复权方式，pre(前复权), post(后复权), none(不复权)
        
    Returns:
        pandas.DataFrame: 股票K线数据
    """
    logger.info(f"使用模拟数据生成股票数据: {stock_code}")
    
    import numpy as np
    from datetime import datetime, timedelta
    
    # 模拟生成一些数据
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    days = (end - start).days + 1
    
    dates = [start + timedelta(days=i) for i in range(days)]
    
    # 生成模拟的股价数据
    np.random.seed(42)  # 为了结果可重现
    open_prices = 100 + np.cumsum(np.random.randn(days) * 0.5)
    high_prices = open_prices + np.abs(np.random.randn(days) * 0.5)
    low_prices = open_prices - np.abs(np.random.randn(days) * 0.5)
    close_prices = low_prices + np.abs(np.random.randn(days) * 0.5)
    volumes = np.random.randint(1000000, 10000000, days)
    amounts = close_prices * volumes
    
    # 创建DataFrame
    data = pd.DataFrame({
        'date': dates,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volumes,
        'amount': amounts
    })
    
    logger.info(f"模拟数据生成完成，共 {len(data)} 条记录")
    return data