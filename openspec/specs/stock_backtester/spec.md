# stock_backtester Specification

## Purpose
TBD - created by archiving change implement-basic-stock-backtester. Update Purpose after archive.
## Requirements
### Requirement: Configuration Management
系统必须提供配置管理功能，能够读取和解析YAML格式的配置文件。系统 SHALL 提供配置管理功能，能够读取和解析YAML格式的配置文件。

#### Scenario: Successful configuration loading
- **WHEN** 系统启动时
- **AND** config.yaml文件存在且格式正确
- **THEN** 系统 SHALL 成功加载配置项excel_path和max_threads
- **AND** 将这些配置项提供给其他模块使用

#### Scenario: Missing configuration file
- **WHEN** 系统启动时
- **AND** config.yaml文件不存在
- **THEN** 系统 SHALL 抛出FileNotFoundError异常
- **AND** 在控制台输出清晰的错误信息

#### Scenario: Missing required configuration items
- **WHEN** 系统启动时
- **AND** config.yaml文件存在但缺少必需的配置项
- **THEN** 系统 SHALL 抛出KeyError异常
- **AND** 在控制台输出清晰的错误信息

### Requirement: Stock Code Processing
系统必须能够处理股票代码，将A股代码转换为xtquant要求的格式。系统 SHALL 能够处理股票代码，将A股代码转换为xtquant要求的格式。

#### Scenario: Successful stock code formatting with various formats
- **WHEN** 系统读取到有效的A股代码（如000001, 600519, 000001.SZ, SZ.000001等格式）
- **THEN** 系统 SHALL 将其转换为xtquant要求的格式（如000001.SZ, 600519.SH）

#### Scenario: Numeric stock code formatting
- **WHEN** 系统读取到数值型的A股代码（如1, 600519等）
- **THEN** 系统 SHALL 将其转换为6位数字字符串并格式化为xtquant要求的格式（如1转换为000001.SZ）

#### Scenario: Short numeric stock code formatting
- **WHEN** 系统读取到少于6位数字的股票代码（如12345）
- **THEN** 系统 SHALL 将其补齐为6位数字并格式化为xtquant要求的格式（如12345转换为012345.SZ）

#### Scenario: Invalid stock code handling
- **WHEN** 系统遇到不符合A股代码规则的输入（如非6位数字代码、无效的前缀、超过6位的数字等）
- **THEN** 系统 SHALL 记录错误信息
- **AND** 跳过该股票，继续处理其他股票

### Requirement: Excel File Reading
系统必须能够正确读取Excel文件中的股票代码列表。系统 SHALL 能够正确读取Excel文件中的股票代码列表。

#### Scenario: Reading stock codes from Excel with correct data types
- **WHEN** 系统读取Excel文件中的股票代码列
- **THEN** 系统 SHALL 确保股票代码作为字符串类型读取
- **AND** 正确处理数值型股票代码（如1转换为"000001"）

#### Scenario: Handling mixed stock code formats in Excel
- **WHEN** Excel文件中包含不同格式的股票代码（数值型和字符串型混合）
- **THEN** 系统 SHALL 正确解析所有股票代码
- **AND** 将其转换为xtquant要求的格式

### Requirement: Time Range Calculation
系统必须根据start_date和end_date参数正确计算数据下载的时间范围。系统 SHALL 根据start_date和end_date参数正确计算数据下载的时间范围。

#### Scenario: Only start_date provided
- **WHEN** 用户只提供start_date参数
- **THEN** 系统 SHALL 下载从start_date到当前系统日期的所有数据

#### Scenario: Only end_date provided
- **WHEN** 用户只提供end_date参数
- **THEN** 系统 SHALL 下载从end_date当天起向前倒推6个月的数据

#### Scenario: Neither start_date nor end_date provided
- **WHEN** 用户未提供start_date和end_date参数
- **THEN** 系统 SHALL 下载从当前系统日期起向前倒推6个月的数据

#### Scenario: Both start_date and end_date provided
- **WHEN** 用户同时提供start_date和end_date参数
- **THEN** 系统 SHALL 使用这两个日期作为精确的下载范围

### Requirement: Concurrent Data Download
系统必须支持多线程并发下载不同股票的数据。系统 SHALL 支持多线程并发下载不同股票的数据。

#### Scenario: Concurrent download with progress tracking
- **WHEN** 系统开始下载多只股票的数据
- **THEN** 系统 SHALL 使用多线程技术并发下载
- **AND** 最大并发线程数 SHALL 由max_threads配置项控制
- **AND** 系统 SHALL 在控制台显示实时进度条，显示完成百分比、已处理项/总项数及预估剩余时间

### Requirement: Data Format Requirements
系统获取的K线数据必须包含指定字段并支持不同的复权模式。系统 SHALL 获取包含指定字段并支持不同复权模式的K线数据。

#### Scenario: Correct data fields
- **WHEN** 系统成功下载股票K线数据
- **THEN** 数据 SHALL 包含以下字段：开盘价(Open), 最高价(High), 最低价(Low), 收盘价(Close), 成交量(Volume), 成交额(Amount)

#### Scenario: Adjustment method configuration
- **WHEN** 系统下载股票K线数据
- **AND** 未指定复权方式参数
- **THEN** 系统 SHALL 默认使用前复权模式进行数据获取

#### Scenario: Custom adjustment method
- **WHEN** 用户通过参数指定了复权方式
- **THEN** 系统 SHALL 使用用户指定的复权方式进行数据获取

#### Scenario: Timezone handling
- **WHEN** 系统下载股票K线数据
- **THEN** 时间数据 SHALL 被正确转换为北京时间
- **AND** 股市收盘时间 SHALL 显示为15:00

### Requirement: Error Handling
系统必须正确处理不同类型的错误。系统 SHALL 正确处理不同类型的错误。

#### Scenario: Critical configuration error
- **WHEN** 发生阻断程序核心流程的错误（如配置文件缺失）
- **THEN** 程序 SHALL 立即抛出异常并终止执行
- **AND** 在控制台输出清晰、易于理解的错误信息

#### Scenario: Individual stock download error
- **WHEN** 单个股票数据下载过程中出现错误（如股票代码无效、网络问题等）
- **THEN** 程序 SHALL 记录错误信息
- **AND** 继续处理其他股票，不终止整个程序执行

#### Scenario: Zero records stock download
- **WHEN** 系统成功调用数据下载接口但返回0条记录
- **THEN** 系统 SHALL 视为下载失败
- **AND** 程序 SHALL 记录错误信息
- **AND** 继续处理其他股票，不终止整个程序执行

### Requirement: Timezone Conversion
系统必须正确处理从xtquant获取的时间数据并转换为北京时间。系统 SHALL 正确处理从xtquant获取的时间数据并转换为北京时间。

#### Scenario: Timezone conversion for daily data
- **WHEN** 系统下载日线数据
- **THEN** 时间数据 SHALL 被正确转换为北京时间
- **AND** 股市收盘时间 SHALL 显示为15:00

#### Scenario: Timezone conversion for minute data
- **WHEN** 系统下载分钟线数据
- **THEN** 时间数据 SHALL 被正确转换为北京时间
- **AND** 股市交易时间 SHALL 符合实际交易时间

