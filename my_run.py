"""
股票筛选脚本
根据Excel中的股票代码进行筛选，包含以下条件：
1. 收盘价高于MA5
2. 基于30分钟线的WR数据，小于-80
"""
import pandas as pd
from stock_backtester.config import Config
from stock_backtester.engine import calculate_time_range
from stock_backtester.logger import setup_logging, get_logger
from stock_backtester.screener.screener import Screener
from stock_backtester.screener.filters import GeneralComparisonFilter


def main():
    """主函数"""
    setup_logging()
    logger = get_logger(__name__)
    
    logger.info("开始执行股票筛选程序")
    
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
        
        # 计算时间范围
        start_date, end_date = calculate_time_range(None, None)
        print(f"数据下载时间范围: {start_date} 到 {end_date}")
        logger.info(f"数据下载时间范围: {start_date} 到 {end_date}")
        
        # 创建筛选器管理器
        screener = Screener(start_date, end_date)
        
        # 添加筛选条件1：收盘价高于MA5
        print("添加筛选条件1：收盘价高于MA5")
        price_above_ma_filter = GeneralComparisonFilter('close', 'MA5', 'gt')
        screener.add_filter(price_above_ma_filter)
        
        # 添加筛选条件2：基于30分钟线的WR数据小于-80
        print("添加筛选条件2：基于30分钟线的WR数据小于-80")
        from stock_backtester.screener.filters import WRFilter
        wr_filter = WRFilter(period=14, threshold=-80, condition='lt', data_period='30m')
        screener.add_filter(wr_filter)
        
        # 执行股票筛选
        print("\n开始执行股票筛选...")
        logger.info("开始执行股票筛选...")
        
        # 执行筛选
        screened_stocks = screener.screen(stock_list)
        
        print(f"\n筛选完成，符合条件的股票数量: {len(screened_stocks)}")
        logger.info(f"筛选完成，符合条件的股票数量: {len(screened_stocks)}")
        
        # 将结果保存到Excel文件
        result_df = pd.DataFrame({'筛选结果': screened_stocks})
        output_path = 'data/screened_stocks_result.xlsx'
        result_df.to_excel(output_path, index=False)
        print(f"筛选结果已保存到: {output_path}")
        logger.info(f"筛选结果已保存到: {output_path}")
        
        if screened_stocks:
            print(f"符合条件的股票: {screened_stocks}")
            logger.info(f"符合条件的股票: {screened_stocks}")
        else:
            print("没有股票符合条件")
            logger.info("没有股票符合条件")
            
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
        
    logger.info("程序执行完成")


if __name__ == "__main__":
    main()