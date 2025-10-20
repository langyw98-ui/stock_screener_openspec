## Why
在使用xtquant_feed下载股票数据时，时间显示存在错误。当前实现中，从xtquant获取的时间数据没有正确处理时区信息，导致显示的时间与实际的北京时间不一致。特别是股市在15:00收盘，但当前下载的股票数据显示的时间不是在15:00收盘，这会影响数据分析的准确性。

## What Changes
- 修改`stock_backtester/feeds/xtquant_feed.py`中的`download_stock_data`函数，增加对时间数据的时区处理
- 确保从xtquant获取的时间数据被正确转换为北京时间
- 更新相关规范以反映这一变更

## Impact
- Affected specs: stock_backtester
- Affected code: stock_backtester/feeds/xtquant_feed.py