"""
股票筛选模块单元测试
"""
import unittest
import pandas as pd
import numpy as np
import tempfile
import os
import sys
import yaml

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from stock_backtester.screener.base import Filter, Indicator
from stock_backtester.screener.indicators import MAIndicator, WRIindicator
from stock_backtester.screener.filters import MAFilter, WRFilter, GeneralComparisonFilter
from stock_backtester.screener.screener import Screener
from stock_backtester.config import Config


class TestIndicators(unittest.TestCase):
    """技术指标测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试数据
        dates = pd.date_range('2025-01-01', periods=20, freq='D')
        self.test_data = pd.DataFrame({
            'date': dates,
            'open': np.random.uniform(100, 110, 20),
            'high': np.random.uniform(110, 120, 20),
            'low': np.random.uniform(90, 100, 20),
            'close': np.random.uniform(100, 110, 20),
            'volume': np.random.randint(1000000, 2000000, 20),
            'amount': np.random.uniform(10000000, 20000000, 20)
        })
    
    def test_ma_indicator(self):
        """测试移动平均线指标"""
        # 创建MA指标
        ma_indicator = MAIndicator(period=5)
        
        # 计算MA
        result_data = ma_indicator.calculate(self.test_data.copy())
        
        # 验证结果
        self.assertIn('MA5', result_data.columns)
        self.assertEqual(len(result_data), 20)
        # 前4个值应该是NaN（因为周期是5）
        self.assertTrue(pd.isna(result_data['MA5'].iloc[0]))
        self.assertTrue(pd.isna(result_data['MA5'].iloc[3]))
        # 第5个值应该是数值
        self.assertFalse(pd.isna(result_data['MA5'].iloc[4]))
    
    def test_wr_indicator(self):
        """测试威廉指标"""
        # 创建WR指标
        wr_indicator = WRIindicator(period=14)
        
        # 计算WR
        result_data = wr_indicator.calculate(self.test_data.copy())
        
        # 验证结果
        self.assertIn('WR14', result_data.columns)
        self.assertEqual(len(result_data), 20)
        # 前13个值应该是NaN（因为周期是14）
        self.assertTrue(pd.isna(result_data['WR14'].iloc[0]))
        self.assertTrue(pd.isna(result_data['WR14'].iloc[12]))
        # 第14个值应该是数值
        self.assertFalse(pd.isna(result_data['WR14'].iloc[13]))
        
        # 测试除零情况（最高价等于最低价）
        test_data_zero_range = self.test_data.copy()
        test_data_zero_range.loc[13:14, 'high'] = test_data_zero_range.loc[13:14, 'low']
        result_data_zero = wr_indicator.calculate(test_data_zero_range.copy())
        # 验证除零情况下的处理 - 当最高价等于最低价时，威廉指标应该是一个有限值
        self.assertFalse(pd.isna(result_data_zero['WR14'].iloc[13]))


class TestFilters(unittest.TestCase):
    """筛选器测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试数据
        dates = pd.date_range('2025-01-01', periods=20, freq='D')
        self.test_stock_data = {
            '000001.SZ': pd.DataFrame({
                'date': dates,
                'open': np.random.uniform(100, 110, 20),
                'high': np.random.uniform(110, 120, 20),
                'low': np.random.uniform(90, 100, 20),
                'close': np.random.uniform(100, 110, 20),
                'volume': np.random.randint(1000000, 2000000, 20),
                'amount': np.random.uniform(10000000, 20000000, 20)
            }),
            '600519.SH': pd.DataFrame({
                'date': dates,
                'open': np.random.uniform(1500, 1600, 20),
                'high': np.random.uniform(1600, 1700, 20),
                'low': np.random.uniform(1400, 1500, 20),
                'close': np.random.uniform(1500, 1600, 20),
                'volume': np.random.randint(100000, 200000, 20),
                'amount': np.random.uniform(100000000, 200000000, 20)
            })
        }
    
    def test_ma_filter(self):
        """测试移动平均线筛选器"""
        # 创建MA筛选器（MA5 > MA10）
        ma_filter = MAFilter(period1=5, period2=10, condition='gt')
        
        # 执行筛选
        result = ma_filter.filter(self.test_stock_data)
        
        # 验证结果类型
        self.assertIsInstance(result, list)
    
    def test_wr_filter(self):
        """测试威廉指标筛选器"""
        # 创建WR筛选器（WR < -80）
        wr_filter = WRFilter(period=14, threshold=-80, condition='lt')
        
        # 执行筛选
        result = wr_filter.filter(self.test_stock_data)
        
        # 验证结果类型
        self.assertIsInstance(result, list)

    def test_general_comparison_filter(self):
        """测试通用比较筛选器"""
        # 测试价格与价格比较（close > open）
        filter1 = GeneralComparisonFilter('close', 'open', 'gt')
        result1 = filter1.filter(self.test_stock_data)
        self.assertIsInstance(result1, list)
        
        # 测试指标与指标比较（MA5 > MA10）
        filter2 = GeneralComparisonFilter('MA5', 'MA10', 'gt')
        result2 = filter2.filter(self.test_stock_data)
        self.assertIsInstance(result2, list)
        
        # 测试价格与指标比较（close > MA5）
        filter3 = GeneralComparisonFilter('close', 'MA5', 'gt')
        result3 = filter3.filter(self.test_stock_data)
        self.assertIsInstance(result3, list)
        
        # 测试指标与数值比较（WR14 < -80）
        filter4 = GeneralComparisonFilter('WR14', -80, 'lt')
        result4 = filter4.filter(self.test_stock_data)
        self.assertIsInstance(result4, list)
        
        # 测试不同的比较操作
        filter5 = GeneralComparisonFilter('close', 'open', 'lt')  # 小于
        result5 = filter5.filter(self.test_stock_data)
        self.assertIsInstance(result5, list)
        
        filter6 = GeneralComparisonFilter('close', 'open', 'eq')  # 等于
        result6 = filter6.filter(self.test_stock_data)
        self.assertIsInstance(result6, list)
        
        filter7 = GeneralComparisonFilter('close', 'open', 'gte')  # 大于等于
        result7 = filter7.filter(self.test_stock_data)
        self.assertIsInstance(result7, list)
        
        filter8 = GeneralComparisonFilter('close', 'open', 'lte')  # 小于等于
        result8 = filter8.filter(self.test_stock_data)
        self.assertIsInstance(result8, list)


class TestScreener(unittest.TestCase):
    """筛选器管理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试数据
        dates = pd.date_range('2025-01-01', periods=20, freq='D')
        self.test_stock_data = {
            '000001.SZ': pd.DataFrame({
                'date': dates,
                'open': np.random.uniform(100, 110, 20),
                'high': np.random.uniform(110, 120, 20),
                'low': np.random.uniform(90, 100, 20),
                'close': np.random.uniform(100, 110, 20),
                'volume': np.random.randint(1000000, 2000000, 20),
                'amount': np.random.uniform(10000000, 20000000, 20)
            }),
            '600519.SH': pd.DataFrame({
                'date': dates,
                'open': np.random.uniform(1500, 1600, 20),
                'high': np.random.uniform(1600, 1700, 20),
                'low': np.random.uniform(1400, 1500, 20),
                'close': np.random.uniform(1500, 1600, 20),
                'volume': np.random.randint(100000, 200000, 20),
                'amount': np.random.uniform(100000000, 200000000, 20)
            })
        }
    
    def test_screener_chain(self):
        """测试链式筛选"""
        # 创建筛选器管理器
        screener = Screener()
        
        # 添加筛选器
        ma_filter = MAFilter(period1=5, period2=10, condition='gt')
        wr_filter = WRFilter(period=14, threshold=-80, condition='lt')
        
        screener.add_filter(ma_filter).add_filter(wr_filter)
        
        # 验证筛选链
        chain = screener.get_filter_chain()
        self.assertEqual(len(chain), 2)
        self.assertIn('MA5_vs_MA10', chain)
        self.assertIn('WR14_1d', chain)  # 现在WRFilter包含数据周期信息
        
        # 执行筛选
        result = screener.exec(self.test_stock_data)
        
        # 验证结果类型
        self.assertIsInstance(result, list)
    
    def test_screener_config_loading(self):
        """测试从配置加载筛选器"""
        # 创建临时配置文件
        temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        temp_config_path = temp_config.name
        
        # 写入测试配置
        test_config = {
            'excel_path': 'data/stock_list.xlsx',
            'max_threads': 4
        }
        
        yaml.dump(test_config, temp_config)
        temp_config.close()
        
        try:
            # 创建配置对象
            config = Config(temp_config_path)
            
            # 创建筛选器管理器（不再从配置加载筛选器）
            screener = Screener()
            
            # 验证筛选链为空
            chain = screener.get_filter_chain()
            self.assertEqual(len(chain), 0)
            
        finally:
            # 清理临时文件
            os.unlink(temp_config_path)


if __name__ == '__main__':
    unittest.main()