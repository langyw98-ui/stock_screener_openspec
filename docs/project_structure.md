# 项目文件结构说明

## 项目概述

本项目是一个基于xtquant库的股票数据下载和回测系统，支持多线程并发下载股票数据，并提供完整的测试框架。

## 目录结构

```
stock_screener_openspec_new/
├── api/                    # API文档
│   └── xtquant.md          # xtquant库API文档
├── config/                 # 配置文件
│   └── logging_config.yaml # 日志配置文件
├── data/                   # 数据文件
│   └── stock_list.xlsx     # 股票代码列表文件
├── docs/                   # 文档目录
│   ├── project_structure.md # 项目结构说明（本文档）
├── openspec/               # OpenSpec规范目录
│   ├── changes/            # 变更提案
│   │   └── add-stock-screener-module/ # 股票筛选模块变更
│   ├── specs/              # 规范定义
│   │   ├── logging/        # 日志规范
│   │   └── stock_backtester/ # 回测系统规范
│   ├── AGENTS.md           # Agent说明
│   └── project.md          # 项目规范
├── stock_backtester/       # 核心回测模块
│   ├── feeds/              # 数据源模块
│   │   ├── __init__.py     # 包初始化文件
│   │   └── xtquant_feed.py # xtquant数据接口封装
│   ├── screener/           # 股票筛选模块
│   │   ├── __init__.py     # 包初始化文件
│   │   ├── base.py         # 筛选器基类和接口
│   │   ├── indicators.py   # 技术指标计算
│   │   ├── filters.py      # 具体筛选器实现
│   │   └── screener.py     # 筛选器管理器
│   ├── __init__.py         # 包初始化文件
│   ├── config.py           # 配置模块
│   ├── engine.py           # 核心引擎模块
│   └── logger.py           # 日志模块
├── test/                   # 测试目录
│   ├── unit/               # 单元测试
│   │   ├── test_config.py      # 配置模块测试
│   │   ├── test_engine.py      # 引擎模块测试
│   │   └── test_xtquant_feed.py # 数据源模块测试
│   ├── integration/        # 集成测试
│   │   └── test_integration.py # 集成测试
│   ├── README.md           # 测试说明文档
│   └── run_tests.py        # 测试运行脚本
├── .git/                   # Git版本控制目录
├── .gemini/                # Gemini配置目录
├── .qwen/                  # Qwen配置目录
├── .gitignore              # Git忽略文件配置
├── AGENTS.md               # Agent说明文档
├── config.yaml             # 项目配置文件
├── requirements.txt        # Python依赖包列表
└── run.py                  # 项目主执行文件
```

## 核心模块说明

### 1. 主执行模块 (run.py)

项目入口文件，负责：
- 加载配置
- 读取股票列表
- 计算时间范围
- 调用引擎模块下载股票数据

### 2. 配置模块 (stock_backtester/config.py)

负责读取和解析`config.yaml`配置文件：
- `excel_path`: 股票代码Excel文件路径
- `max_threads`: 最大线程数，控制并发下载数量

### 3. 核心引擎模块 (stock_backtester/engine.py)

核心业务逻辑模块：
- `calculate_time_range`: 计算数据下载时间范围
- `download_single_stock`: 下载单只股票数据
- `download_all_stocks`: 并发下载所有股票数据

### 4. 数据源模块 (stock_backtester/feeds/xtquant_feed.py)

封装xtquant数据接口：
- `format_stock_code`: 格式化股票代码为xtquant要求的格式
- `download_stock_data`: 从xtquant下载股票数据
- `_simulate_download_stock_data`: 模拟数据下载（用于测试）

### 5. 日志模块 (stock_backtester/logger.py)

日志配置和管理：
- `setup_logging`: 设置日志配置
- `get_logger`: 获取日志记录器实例

### 6. 股票筛选模块 (stock_backtester/screener/)

股票筛选功能模块，支持基于技术指标的股票筛选：

#### screener/base.py
- 筛选器基类和接口定义
- 定义筛选器的通用接口和基础功能

#### screener/indicators.py
- 技术指标计算模块
- 提供移动平均线(MA)和威廉指标(WR)等指标计算功能
- 支持用户自定义计算周期

#### screener/filters.py
- 具体筛选器实现
- 实现基于MA和WR指标的筛选器
- 支持链式筛选方式
- 新增收盘价与移动平均线比较筛选器

#### screener/screener.py
- 筛选器管理器
- 管理和执行链式筛选流程
- 集成配置管理模块

#### 核心功能特性：
- 链式筛选方式：支持按顺序添加多个筛选条件，每个筛选条件基于前一个条件的结果进行进一步筛选
- 技术指标计算：提供移动平均线(MA)和威廉指标(WR)等指标计算
- 技术指标筛选：基于技术指标的股票筛选功能
- 配置管理集成：使用项目的配置管理模块进行相关信息配置
- 新增收盘价与移动平均线比较筛选功能：支持筛选收盘价高于或低于指定周期移动平均线的股票

## 配置文件

### config.yaml

```yaml
# 存放股票代码的Excel文件路径
excel_path: "data/stock_list.xlsx"

# 最大线程数，控制并发下载的数量
max_threads: 4
```

### config/logging_config.yaml

定义日志输出格式和级别：
- 控制台输出INFO级别及以上日志
- 文件输出DEBUG级别及以上日志
- 日志文件名为`stock_backtester.log`

## 测试框架

### 单元测试

1. `test_config.py` - 测试配置模块的功能
2. `test_xtquant_feed.py` - 测试xtquant数据源模块的功能
3. `test_engine.py` - 测试核心引擎模块的功能
4. `test_screener.py` - 测试股票筛选模块的功能

### 集成测试

1. `test_integration.py` - 测试整个系统的集成功能

### 运行测试

```bash
# 运行所有测试
python test/run_tests.py

# 运行单元测试
python -m unittest discover -s test/unit -p "test_*.py" -v

# 运行集成测试
python -m unittest discover -s test/integration -p "test_*.py" -v
```

## 依赖包

项目依赖的Python包定义在`requirements.txt`中：
- pandas>=1.3.0: 数据处理
- PyYAML>=5.4.0: YAML配置文件解析
- tqdm>=4.62.0: 进度条显示
- openpyxl>=3.0.7: Excel文件读取
- numpy>=1.21.0: 数值计算

## 数据文件

`data/stock_list.xlsx` - 包含需要下载的股票代码列表的Excel文件，第一列为`stock_code`。

## OpenSpec规范

项目采用OpenSpec规范进行开发，包含：
- `specs/logging`: 日志规范
- `specs/stock_backtester`: 回测系统规范
- `changes/add-stock-screener-module`: 股票筛选模块变更提案