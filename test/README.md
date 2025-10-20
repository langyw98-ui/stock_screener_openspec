# 测试说明

## 目录结构

```
test/
├── unit/           # 单元测试
├── integration/    # 集成测试
└── run_tests.py    # 测试运行脚本
```

## 运行测试

### 运行所有测试

```bash
python test/run_tests.py
```

### 运行单元测试

```bash
python -m unittest discover -s test/unit -p "test_*.py" -v
```

### 运行集成测试

```bash
python -m unittest discover -s test/integration -p "test_*.py" -v
```

### 运行特定测试文件

```bash
python test/unit/test_config.py
python test/unit/test_xtquant_feed.py
python test/unit/test_engine.py
python test/integration/test_integration.py
```

## 测试内容

### 单元测试

1. **test_config.py** - 测试配置模块的功能
   - 配置文件加载
   - 配置项验证
   - 错误处理

2. **test_xtquant_feed.py** - 测试xtquant数据源模块的功能
   - 股票代码格式化
   - 有效和无效代码处理
   - 数字和字符串输入处理

3. **test_engine.py** - 测试核心引擎模块的功能
   - 时间范围计算逻辑
   - 各种参数组合的处理

### 集成测试

1. **test_integration.py** - 测试整个系统的集成功能
   - 完整的工作流程
   - 模块间的协作
   - 数据流验证