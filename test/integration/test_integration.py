"""
集成测试 - 测试整个股票回测软件的基本功能
"""
import unittest
import pandas as pd
import tempfile
import os
import sys
import yaml

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from stock_backtester.config import Config
from stock_backtester.feeds.xtquant_feed import format_stock_code
from stock_backtester.engine import calculate_time_range, download_single_stock


class TestIntegration(unittest.TestCase):
    """集成测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.test_dir = tempfile.mkdtemp()
        
        # 创建临时Excel文件
        self.excel_path = os.path.join(self.test_dir, 'stock_list.xlsx')
        test_data = pd.DataFrame({
            'stock_code': ['000001', '600519', '000858']
        })
        test_data.to_excel(self.excel_path, index=False)
        
        # 创建临时配置文件
        self.config_path = os.path.join(self.test_dir, 'config.yaml')
        config_data = {
            'excel_path': self.excel_path,
            'max_threads': 2
        }
        with open(self.config_path, 'w') as f:
            yaml.dump(config_data, f)
    
    def tearDown(self):
        """测试后清理"""
        # 清理临时文件和目录
        if os.path.exists(self.excel_path):
            os.unlink(self.excel_path)
        if os.path.exists(self.config_path):
            os.unlink(self.config_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_full_workflow(self):
        """测试完整的工作流程"""
        # 1. 加载配置
        config = Config(self.config_path)
        self.assertEqual(config.excel_path, self.excel_path)
        self.assertEqual(config.max_threads, 2)
        
        # 2. 读取股票列表
        stock_df = pd.read_excel(config.excel_path, dtype={'stock_code': str})
        stock_list = stock_df['stock_code'].tolist()
        self.assertEqual(len(stock_list), 3)
        self.assertIn('000001', stock_list)
        self.assertIn('600519', stock_list)
        self.assertIn('000858', stock_list)
        
        # 3. 格式化股票代码
        formatted_codes = [format_stock_code(code) for code in stock_list]
        expected_codes = ['000001.SZ', '600519.SH', '000858.SZ']
        for expected in expected_codes:
            self.assertIn(expected, formatted_codes)
        
        # 4. 计算时间范围
        start_date, end_date = calculate_time_range(None, None)
        self.assertRegex(start_date, r'^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(end_date, r'^\d{4}-\d{2}-\d{2}$')
        
        # 5. 测试单只股票下载（使用模拟数据）
        data = download_single_stock('000001', start_date, end_date)
        # 验证返回结果
        self.assertIsNotNone(data)
        self.assertIsInstance(data, pd.DataFrame)
        # 验证数据结构
        expected_columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount']
        for col in expected_columns:
            self.assertIn(col, data.columns)


if __name__ == '__main__':
    unittest.main()