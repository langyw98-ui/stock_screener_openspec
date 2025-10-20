"""
配置模块单元测试
"""
import unittest
import os
import sys
import tempfile
import yaml

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from stock_backtester.config import Config


class TestConfig(unittest.TestCase):
    """配置模块测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        self.temp_config_path = self.temp_config.name
        
        # 写入测试配置
        test_config = {
            'excel_path': 'test_data/stock_list.xlsx',
            'max_threads': 2
        }
        yaml.dump(test_config, self.temp_config)
        self.temp_config.close()
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时配置文件
        if os.path.exists(self.temp_config_path):
            os.unlink(self.temp_config_path)
    
    def test_config_loading_success(self):
        """测试配置加载成功"""
        config = Config(self.temp_config_path)
        self.assertEqual(config.excel_path, 'test_data/stock_list.xlsx')
        self.assertEqual(config.max_threads, 2)
    
    def test_config_file_not_found(self):
        """测试配置文件不存在的情况"""
        with self.assertRaises(FileNotFoundError):
            Config('nonexistent_config.yaml')
    
    def test_config_missing_excel_path(self):
        """测试缺少excel_path配置项"""
        # 创建缺少excel_path的配置文件
        temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        temp_config_path = temp_config.name
        test_config = {
            'max_threads': 2
        }
        yaml.dump(test_config, temp_config)
        temp_config.close()
        
        with self.assertRaises(KeyError):
            Config(temp_config_path)
        
        # 清理
        os.unlink(temp_config_path)
    
    def test_config_missing_max_threads(self):
        """测试缺少max_threads配置项"""
        # 创建缺少max_threads的配置文件
        temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        temp_config_path = temp_config.name
        test_config = {
            'excel_path': 'test_data/stock_list.xlsx'
        }
        yaml.dump(test_config, temp_config)
        temp_config.close()
        
        with self.assertRaises(KeyError):
            Config(temp_config_path)
        
        # 清理
        os.unlink(temp_config_path)


if __name__ == '__main__':
    unittest.main()