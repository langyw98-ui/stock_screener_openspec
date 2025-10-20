## MODIFIED Requirements
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