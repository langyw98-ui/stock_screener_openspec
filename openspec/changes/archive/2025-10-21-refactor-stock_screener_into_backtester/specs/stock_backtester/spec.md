## MODIFIED Requirements
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

### Requirement: Multiple Period Data Download
系统必须支持下载和处理多种数据周期。系统 SHALL 支持下载和处理多种数据周期。

#### Scenario: Support for different data periods
- **WHEN** 用户需要下载不同周期的数据
- **THEN** 系统 SHALL 支持下载和处理多种数据周期
- **AND** 包括但不限于1分钟线(1m)、5分钟线(5m)、30分钟线(30m)和日线(1d)等周期

#### Scenario: Concurrent download of multiple periods
- **WHEN** 用户需要同时下载多个周期的数据
- **THEN** 系统 SHALL 支持并发下载不同周期的数据
- **AND** 每个周期的数据 SHALL 独立处理和存储

### Requirement: Stock Screener Core Functionality and Chained Filtering
系统必须(SHALL)提供股票筛选功能，支持用户通过技术指标对股票进行筛选，并采用链式筛选方式实现，支持用户通过代码按顺序添加或移除多个筛选条件，每个筛选条件基于前一个条件的结果进行进一步筛选。

系统应采用类似backtrader的模块化架构设计，包括：
- Engine模块作为核心引擎，负责协调整个筛选流程
- Feeds模块作为数据源，负责提供股票市场数据
- Screener模块作为筛选器，负责实现具体的筛选逻辑

#### Scenario: 筛选模块初始化与调用
- **WHEN** 系统启动时
- **AND** 用户通过主程序调用筛选功能
- **THEN** 筛选模块应正确加载并初始化
- **AND** 系统应执行相应的筛选逻辑
- **AND** 返回筛选结果给用户
- **AND** 筛选模块应能处理由engine模块下载的多种周期数据

#### Scenario: 链式筛选条件添加与执行
- **WHEN** 用户通过代码添加多个筛选条件并执行筛选
- **THEN** 系统应按顺序执行筛选条件
- **AND** 每个筛选条件都基于前一个条件的结果进行进一步筛选
- **AND** 只有通过所有筛选器的股票才会被选中

#### Scenario: 链式筛选条件动态调整
- **WHEN** 用户在筛选过程中通过代码动态添加或移除筛选条件
- **THEN** 系统应支持动态调整筛选链
- **AND** 重新执行筛选流程

#### Scenario: 链式筛选部分条件失败
- **WHEN** 某些筛选条件执行失败
- **THEN** 系统应视为整个筛选过程失败
- **AND** 返回错误信息给用户

### Requirement: Screener Data Processing Approach
系统必须(SHALL)改变筛选器的数据处理方式，筛选器不应接收预下载的股票数据字典，而应通过股票代码列表和统一的数据范围参数，由Engine模块协调实时下载所需数据。

#### Scenario: 筛选器接收股票代码列表
- **WHEN** 用户调用Screener的筛选功能时
- **THEN** 系统应向Screener提供股票代码列表而非预下载的数据字典
- **AND** Screener应基于股票代码列表进行筛选

#### Scenario: 统一数据范围设置
- **WHEN** 用户设置筛选的数据范围参数时
- **THEN** 所有筛选器应使用相同的数据范围参数
- **AND** 这些参数应包括时间范围（start_time和end_time）
- **AND** 数据周期由各个筛选器根据自身需求决定

#### Scenario: 筛选器数据下载协调
- **WHEN** 筛选器需要特定股票和周期的数据时
- **THEN** 筛选器应请求Engine模块下载数据
- **AND** Engine模块应协调Feeds模块执行数据下载
- **AND** 下载的数据应直接提供给请求的筛选器使用

#### Scenario: 数据下载失败处理
- **WHEN** 某只股票的数据下载失败时
- **THEN** 系统应判定该股票筛选失败
- **AND** 不应影响其他股票的筛选过程

### Requirement: Module Collaboration
系统必须(SHALL)确保各模块之间的清晰职责划分和良好协同：

1. Engine模块职责：
   - 协调整个筛选流程
   - 管理并发数据下载
   - 处理数据分发给筛选器
   - 根据筛选器请求实时下载所需数据

2. Feeds模块职责：
   - 提供股票市场数据源
   - 支持多种数据格式和周期
   - 处理数据格式转换和时间戳处理
   - 响应Engine模块的数据下载请求

3. Screener模块职责：
   - 实现具体的筛选逻辑
   - 提供技术指标计算功能
   - 支持链式筛选方式
   - 通过Engine模块请求所需数据

#### Scenario: 模块间数据流
- **WHEN** 用户启动筛选流程
- **THEN** Engine模块应根据Screener模块的请求协调Feeds模块获取数据
- **AND** Engine模块应将下载的数据提供给Screener模块
- **AND** Screener模块应执行筛选逻辑并返回结果
- **AND** Engine模块应汇总结果并返回给用户

#### Scenario: 模块间错误处理
- **WHEN** 任一模块发生错误
- **THEN** 系统应能准确定位错误来源
- **AND** 不应影响其他模块的正常运行（除非是关键依赖）
- **AND** 应提供清晰的错误信息给用户

### Requirement: Configuration Management Integration
系统必须(SHALL)使用项目的配置管理模块进行股票筛选模块相关信息的配置。

#### Scenario: 筛选模块配置加载与更新
- **WHEN** 系统启动时
- **AND** 用户更新筛选配置时
- **THEN** 筛选模块应通过项目配置管理模块加载相关配置
- **AND** 配置信息应包括基本的筛选参数设置
- **AND** 系统应通过配置管理模块保存新的配置信息
- **AND** 在下次启动时使用新配置

### Requirement: Technical Indicator Calculation and Screening
系统必须(SHALL)提供常用技术指标计算功能，支持用户自定义计算周期，并基于这些指标进行股票筛选。

系统应支持处理由feeds模块提供的多种数据周期，包括但不限于1分钟线(1m)、5分钟线(5m)、30分钟线(30m)和日线(1d)等周期。

#### Scenario: 指标计算与错误处理
- **WHEN** 系统接收到股票数据和指标周期参数
- **AND** 系统接收到无效的股票数据或周期参数
- **THEN** 系统应计算指定周期的技术指标值
- **AND** 返回计算结果用于后续筛选
- **AND** 系统应返回适当的错误信息
- **AND** 不应中断其他指标的计算

#### Scenario: 支持的指标类型与数据周期
- **WHEN** 用户选择技术指标进行计算或筛选
- **AND** 用户需要计算不同周期的技术指标
- **THEN** 系统应支持至少以下指标：
- **AND** 移动平均线(MA)
- **AND** 威廉指标(WR)，支持多种时间周期计算包括但不限于30分钟线(30m)、5分钟线(5m)、日线(1d)等周期
- **AND** 系统应支持下载和处理多种数据周期，包括但不限于1分钟线(1m)、5分钟线(5m)、30分钟线(30m)和日线(1d)等周期

#### Scenario: 指标筛选条件设置与结果处理
- **WHEN** 用户设置基于技术指标的筛选条件
- **AND** 没有股票满足指标筛选条件
- **THEN** 系统应根据设定条件筛选符合条件的股票
- **AND** 返回筛选结果
- **AND** 系统应返回空结果集
- **AND** 不应报错

#### Scenario: 支持的筛选条件类型
- **WHEN** 用户设置技术指标筛选条件
- **THEN** 系统应支持至少以下筛选条件：
- **AND** MA条件（如MA5 > MA10）
- **AND** WR条件（如WR < -80表示超卖）
- **AND** 收盘价与MA比较条件（如收盘价 > MA5）
- **AND** 通用比较条件（支持任意两个指标或价格之间的比较）

### Requirement: Generic Comparison Screener
系统必须(SHALL)提供通用比较筛选器，支持用户对任意两个技术指标或价格进行比较筛选。

#### Scenario: 通用比较筛选器初始化
- **WHEN** 用户创建通用比较筛选器实例
- **THEN** 系统应支持指定两个比较对象（技术指标或价格字段）
- **AND** 支持指定比较条件（大于、小于、等于等）
- **AND** 比较对象可以是以下任意组合：
- **AND** 技术指标与技术指标（如MA5 > MA10）
- **AND** 价格字段与技术指标（如close > MA5）
- **AND** 技术指标与数值（如WR14 < -80）
- **AND** 价格字段与价格字段（如close > open）

#### Scenario: 指标与指标比较
- **WHEN** 用户设置两个技术指标之间的比较条件
- **THEN** 系统应正确执行比较逻辑
- **AND** 返回满足条件的股票列表

#### Scenario: 价格与指标比较
- **WHEN** 用户设置价格字段与技术指标的比较条件
- **THEN** 系统应正确执行比较逻辑
- **AND** 返回满足条件的股票列表

#### Scenario: 支持的比较操作
- **WHEN** 用户使用通用比较筛选器
- **THEN** 系统应支持至少以下比较操作：
- **AND** 大于（gt）
- **AND** 小于（lt）
- **AND** 等于（eq）
- **AND** 大于等于（gte）
- **AND** 小于等于（lte）

#### Scenario: 支持的操作数类型
- **WHEN** 用户使用通用比较筛选器
- **THEN** 系统应支持以下操作数类型：
- **AND** 技术指标：MA（移动平均线，支持自定义周期）、WR（威廉指标，支持自定义周期）
- **AND** 价格字段：open（开盘价）、high（最高价）、low（最低价）、close（收盘价）、volume（成交量）、amount（成交额）
- **AND** 数值：整数或浮点数