"""
engine模块单元测试
"""
import unittest
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from stock_backtester.engine import calculate_time_range


class TestEngine(unittest.TestCase):
    """engine模块测试类"""
    
    def test_calculate_time_range_default(self):
        """测试默认时间范围计算"""
        start_date, end_date = calculate_time_range(None, None)
        # 验证日期格式
        self.assertRegex(start_date, r'^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(end_date, r'^\d{4}-\d{2}-\d{2}$')
        
        # 验证时间范围大约为6个月
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end - start
        self.assertAlmostEqual(delta.days, 180, delta=5)  # 允许5天的误差
    
    def test_calculate_time_range_only_start(self):
        """测试只有开始日期的时间范围计算"""
        start_date, end_date = calculate_time_range("2024-01-01", None)
        self.assertEqual(start_date, "2024-01-01")
        # 结束日期应该是今天
        self.assertRegex(end_date, r'^\d{4}-\d{2}-\d{2}$')
    
    def test_calculate_time_range_only_end(self):
        """测试只有结束日期的时间范围计算"""
        start_date, end_date = calculate_time_range(None, "2024-12-31")
        self.assertEqual(end_date, "2024-12-31")
        # 开始日期应该是结束日期前6个月
        self.assertRegex(start_date, r'^\d{4}-\d{2}-\d{2}$')
    
    def test_calculate_time_range_both_dates(self):
        """测试开始和结束日期都提供的时间范围计算"""
        start_date, end_date = calculate_time_range("2024-01-01", "2024-12-31")
        self.assertEqual(start_date, "2024-01-01")
        self.assertEqual(end_date, "2024-12-31")


if __name__ == '__main__':
    unittest.main()