## Why
当前系统中，stock_screener被设计为一个独立的规范模块，但实际上股票筛选功能应该是股票回测系统的一个组成部分。为了更好地反映系统架构的实际情况和功能关系，需要将stock_screener规范合并到stock_backtester规范中，使筛选功能成为回测系统的一个子功能模块。

## What Changes
- 将stock_screener规范中的所有要求移动到stock_backtester规范中
- 更新stock_backtester规范以包含股票筛选功能的相关要求
- 删除独立的stock_screener规范
- 更新相关文档以反映新的架构设计

## Impact
- stock_backtester规范将包含更多功能要求
- 系统架构更加合理，筛选功能作为回测系统的一部分
- 删除stock_screener规范，减少规范碎片化
- 代码结构可能需要相应调整以反映规范变更