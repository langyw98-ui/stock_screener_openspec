## MODIFIED Requirements
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

## ADDED Requirements
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