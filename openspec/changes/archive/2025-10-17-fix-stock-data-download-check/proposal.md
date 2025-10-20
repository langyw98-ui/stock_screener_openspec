## Why
在使用xtquant_feed下载股票数据时，程序对下载成功与否的判断存在缺陷。当前实现仅检查数据是否为None或空DataFrame，但没有检查下载的数据记录条数是否为0。当下载的股票数据记录条数为0时，程序仍认为下载成功，这会导致后续处理出现错误。

## What Changes
- 修改`stock_backtester/feeds/xtquant_feed.py`中的`download_stock_data`函数，增加对下载数据记录条数的检查
- 当下载的股票数据记录条数为0时，函数应返回None，表示下载失败
- 更新相关规范以反映这一变更

## Impact
- Affected specs: stock_backtester
- Affected code: stock_backtester/feeds/xtquant_feed.py