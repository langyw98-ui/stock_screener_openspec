"""
测试运行脚本 - 运行所有单元测试和集成测试
"""
import unittest
import sys
import os


def run_tests():
    """运行所有测试"""
    # 添加项目根目录到Python路径
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加单元测试
    print("加载单元测试...")
    unit_tests_dir = os.path.join(project_root, 'test', 'unit')
    unit_suite = loader.discover(unit_tests_dir, pattern='test_*.py')
    suite.addTest(unit_suite)
    
    # 添加集成测试
    print("加载集成测试...")
    integration_tests_dir = os.path.join(project_root, 'test', 'integration')
    integration_suite = loader.discover(integration_tests_dir, pattern='test_*.py')
    suite.addTest(integration_suite)
    
    # 运行测试
    print("\n" + "="*50)
    print("开始运行所有测试...")
    print("="*50)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)