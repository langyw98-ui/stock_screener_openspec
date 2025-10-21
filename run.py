"""
项目主执行文件，作为程序入口点
"""
import pandas as pd
from stock_backtester.config import Config
from stock_backtester.engine import download_all_stocks, calculate_time_range
from stock_backtester.logger import setup_logging, get_logger
from stock_backtester.screener.screener import Screener
from stock_backtester.screener.filters import MAFilter, WRFilter, GeneralComparisonFilter

# 设置日志
setup_logging()
logger = get_logger(__name__)


def main():
    """主函数"""
    logger.info("程序启动")
    
    try:
        # 读取配置
        config = Config()
        print(f"配置加载成功: excel_path={config.excel_path}, max_threads={config.max_threads}")
        logger.info(f"配置加载成功: excel_path={config.excel_path}, max_threads={config.max_threads}")
        
        # 读取股票列表，确保股票代码作为字符串读取
        logger.info("正在读取股票列表...")
        print("正在读取股票列表...")
        stock_df = pd.read_excel(config.excel_path, dtype={'stock_code': str})
        stock_list = stock_df['stock_code'].tolist()
        print(f"共找到 {len(stock_list)} 只股票")
        print(f"股票代码列表: {stock_list}")
        logger.info(f"共找到 {len(stock_list)} 只股票")
        
        # 设置时间范围参数（可以根据需要修改）
        start_date = None  # 如果为None，则使用默认逻辑
        end_date = None    # 如果为None，则使用默认逻辑
        
        # 计算时间范围
        actual_start_date, actual_end_date = calculate_time_range(start_date, end_date)
        print(f"数据下载时间范围: {actual_start_date} 到 {actual_end_date}")
        logger.info(f"数据下载时间范围: {actual_start_date} 到 {actual_end_date}")
        
        # 定义所有需要下载的周期
        periods = ['1m', '5m', '30m', '1d']  # 支持多种周期数据下载
        adjustment = 'pre' # 复权方式，默认前复权
        
        # 为每个周期下载所有股票数据
        all_stock_data = {}
        for period in periods:
            print(f"\n开始下载 {period} 周期的股票数据...")
            logger.info(f"开始下载 {period} 周期的股票数据...")
            
            # 下载所有股票数据
            stock_data = download_all_stocks(
                stock_list, 
                actual_start_date, 
                actual_end_date, 
                period, 
                adjustment, 
                config.max_threads
            )
            
            # 存储结果
            all_stock_data[period] = stock_data
            
            # 处理结果
            successful_downloads = sum(1 for data in stock_data.values() if data is not None)
            failed_downloads = len(stock_data) - successful_downloads
            
            print(f"{period} 周期数据下载完成: 成功 {successful_downloads} 只，失败 {failed_downloads} 只")
            logger.info(f"{period} 周期数据下载完成: 成功 {successful_downloads} 只，失败 {failed_downloads} 只")
            
            # 显示成功下载的股票
            successful_stocks = [code for code, data in stock_data.items() if data is not None]
            if successful_stocks:
                print(f"成功下载的股票 ({period}): {successful_stocks}")
                logger.info(f"成功下载的股票 ({period}): {successful_stocks}")
        
        # 创建筛选器管理器
        screener = Screener(actual_start_date, actual_end_date)
        
        # 通过代码添加筛选条件
        # 示例：添加MA筛选条件（MA5 > MA10）
        ma_filter = MAFilter(period1=5, period2=10, condition='gt')
        screener.add_filter(ma_filter)
        
        # 示例：添加WR筛选条件（WR < -80）
        wr_filter = WRFilter(period=14, threshold=-80, condition='lt')
        screener.add_filter(wr_filter)
        
        # 示例：添加收盘价高于MA5的筛选条件（使用通用比较筛选器）
        price_above_ma_filter = GeneralComparisonFilter('close', 'MA5', 'gt')
        screener.add_filter(price_above_ma_filter)
        
        # 示例：添加通用比较筛选条件（收盘价 > 开盘价）
        general_filter = GeneralComparisonFilter('close', 'open', 'gt')
        screener.add_filter(general_filter)
        
        # 执行股票筛选
        print("\n开始执行股票筛选...")
        logger.info("开始执行股票筛选...")
        
        # 获取用于筛选的数据周期（默认使用日线数据）
        screening_period = '1d'  # 可以根据需要修改为其他周期，如'5m', '30m'等
        
        # 显示使用的筛选周期
        print(f"使用 {screening_period} 周期数据进行筛选")
        logger.info(f"使用 {screening_period} 周期数据进行筛选")
        
        try:
            # 执行筛选，传递股票代码列表和数据范围参数
            stock_codes = list(stock_list)  # 使用从Excel文件读取的股票代码列表
            screened_stocks = screener.exec(stock_codes)
            
            print(f"\n筛选完成，符合条件的股票数量: {len(screened_stocks)}")
            logger.info(f"筛选完成，符合条件的股票数量: {len(screened_stocks)}")
            
            if screened_stocks:
                print(f"符合条件的股票: {screened_stocks}")
                logger.info(f"符合条件的股票: {screened_stocks}")
            else:
                print("没有股票符合条件")
                logger.info("没有股票符合条件")
                
        except Exception as e:
            error_msg = f"股票筛选执行出错: {str(e)}"
            print(error_msg)
            logger.error(error_msg, exc_info=True)
        
        # 这里可以添加进一步的数据处理逻辑
        # 例如：数据存储、分析等
        logger.info("程序执行完成")
        
    except FileNotFoundError as e:
        error_msg = f"配置文件错误: {str(e)}"
        print(error_msg)
        print("请确保config.yaml文件存在且路径正确")
        logger.error(error_msg)
        logger.error("请确保config.yaml文件存在且路径正确")
    except KeyError as e:
        error_msg = f"配置项缺失: {str(e)}"
        print(error_msg)
        print("请检查config.yaml文件是否包含所有必需的配置项")
        logger.error(error_msg)
        logger.error("请检查config.yaml文件是否包含所有必需的配置项")
    except Exception as e:
        error_msg = f"程序执行出错: {str(e)}"
        print(error_msg)
        logger.error(error_msg, exc_info=True)
        
    logger.info("程序退出")


if __name__ == "__main__":
    main()