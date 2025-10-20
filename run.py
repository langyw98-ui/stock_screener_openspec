"""
项目主执行文件，作为程序入口点
"""
import pandas as pd
from stock_backtester.config import Config
from stock_backtester.engine import download_all_stocks, calculate_time_range
from stock_backtester.logger import setup_logging, get_logger

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
        
        # 设置其他参数
        period = '1d'      # 数据周期
        adjustment = 'pre' # 复权方式，默认前复权
        
        # 下载所有股票数据
        logger.info("开始下载股票数据...")
        print("开始下载股票数据...")
        stock_data = download_all_stocks(
            stock_list, 
            actual_start_date, 
            actual_end_date, 
            period, 
            adjustment, 
            config.max_threads
        )
        
        # 处理结果
        successful_downloads = sum(1 for data in stock_data.values() if data is not None)
        failed_downloads = len(stock_data) - successful_downloads
        
        print(f"数据下载完成: 成功 {successful_downloads} 只，失败 {failed_downloads} 只")
        logger.info(f"数据下载完成: 成功 {successful_downloads} 只，失败 {failed_downloads} 只")
        
        # 显示成功下载的股票
        successful_stocks = [code for code, data in stock_data.items() if data is not None]
        if successful_stocks:
            print(f"成功下载的股票: {successful_stocks}")
            logger.info(f"成功下载的股票: {successful_stocks}")
        
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