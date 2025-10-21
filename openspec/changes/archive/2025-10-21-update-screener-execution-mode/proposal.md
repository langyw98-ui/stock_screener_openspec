## Why
当前的screener模块在添加筛选器后会立即执行筛选操作，这种方式不够灵活。用户可能希望在添加所有筛选器后再统一执行，而不是在添加每个筛选器时都执行。通过修改为显式调用exec()函数来执行筛选操作，可以提供更灵活的控制方式。

## What Changes
- 修改Screener类的实现，使其在添加筛选器时不自动执行
- 添加exec()方法，用于显式执行筛选操作
- 更新相关文档和示例代码
- 更新规范文档以反映新的执行方式

## Impact
- Affected specs: stock_backtester
- Affected code: stock_backtester/screener/screener.py, run.py, my_run.py
- 这是一个Breaking Change，需要更新所有使用Screener的代码