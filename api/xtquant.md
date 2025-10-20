# XtQuant 精简文档

本文档仅包含项目中实际使用到的xtquant功能说明、示例代码和数据字典。

## 使用到的功能

download_history_data - 下载指定合约代码指定周期对应时间范围的行情数据
提示

QMT提供的行情数据中，基础周期包含 tick 1m 5m 1d，这些是实际用于存储的周期 其他周期为合成周期，以基础周期合成得到

合成周期

3m， 由1m线合成
10m, 15m, 30m, 60m, 2h, 3h, 4h 由5分钟线合成
2d(2日线), 3d(3日线), 5d(5日线), 1w（周线）, 1mon（月线）, 1q(季线), 1hy(半年线), 1y（年线） 由日线数据合成
获取合成周期时

如果取历史，需要下载历史的基础周期（如取15m需要下载5m）
如果取实时，可以直接订阅原始周期（如直接订阅15m）
如果同时用到基础周期和合成周期，只需要下载基础周期,例如同时使用5m和15m，因为15m也是由5m合成，所以只需要下载一次5m的数据即可

原型

内置python

download_history_data(stockcode,period,startTime,endTime)
释义

下载指定合约代码指定周期对应时间范围的行情数据

参数

字段名	数据类型	解释
stockcode	string	股票代码，格式为'stkcode.market'，例如 '600000.SH'
period	string	K线周期类型，包括:
'tick'：分笔线
'1d'：日线
'1m'：分钟线
'5m'：5分钟线
startTime	string	起始时间，格式为 "20200101" 或 "20200101093000"，可以为空
endTime	string	结束时间，格式为 "20200101" 或 "20200101093000"，可以为空
incrementally	bool	默认为 None 是否从本地最后一条数据往后增量下载，部分版本客户端可能不支持此参数
返回值

none

示例

示例

# coding:gbk
def init(C):
	download_history_data("000001.SZ","1d","20230101","") # 下载000001.SZ,从20230101至今的日线数据
    download_history_data("000001.SZ","1d","20230101","",incrementally=True) # 下载000001.SZ,从20230101至今的日线数据,增量下载

def handlebar(C):
    return
界面端进行数据下载还可参考:

提示

【攻略】K线/财务数据下载方式 https://www.xuntou.net/forum.php?mod=viewthread&tid=1354&user_code=7zqjlm 来自: 迅投QMT社区

获取行情数据
该目录下的函数用于获取实时行情,历史行情

ContextInfo.get_market_data_ex - 获取行情数据
注意

该函数不建议在init中运行,在init中运行时仅能取到本地数据
关于获取行情函数之间的区别与注意事项可在 - 常见问题-行情相关 查看
除实时行情外，该函数还可用于获取特色数据，如资金流向数据,订单流数据等，获取方式见数据字典
原型

内置python

ContextInfo.get_market_data_ex(
    fields=[], 
    stock_code=[], 
    period='follow', 
    start_time='', 
    end_time='', 
    count=-1, 
    dividend_type='follow', 
    fill_data=True, 
    subscribe=True)
释义

获取实时行情与历史行情数据

参数

名称	类型	描述
field	list	数据字段，详情见下方field字段表
stock_list	list	合约代码列表
period	str	数据周期，可选字段为:
"tick"
"1m"：1分钟线
"5m"：5分钟线；"15m"：15分钟线；"30m"：30分钟线
"1h"小时线
"1d"：日线
"1w"：周线
"1mon"：月线
"1q"：季线
"1hy"：半年线
"1y"：年线
'l2quote'：Level2行情快照
'l2quoteaux'：Level2行情快照补充
'l2order'：Level2逐笔委托
'l2transaction'：Level2逐笔成交
'l2transactioncount'：Level2大单统计
'l2orderqueue'：Level2委买委卖队列
start_time	str	数据起始时间，格式为 %Y%m%d 或 %Y%m%d%H%M%S，填""为获取历史最早一天
end_time	str	数据结束时间，格式为 %Y%m%d 或 %Y%m%d%H%M%S ，填""为截止到最新一天
count	int	数据个数
dividend_type	str	除权方式,可选值为
'none'：不复权
'front':前复权
'back':后复权
'front_ratio': 等比前复权
'back_ratio': 等比后复权
fill_data	bool	是否填充数据
subscribe	bool	订阅数据开关，默认为True，设置为False时不做数据订阅，只读取本地已有数据。
field字段可选：
field	数据类型	含义
time	int	时间
open	float	开盘价
high	float	最高价
low	float	最低价
close	float	收盘价
volume	float	成交量
amount	float	成交额
settle	float	今结算
openInterest	float	持仓量
preClose	float	前收盘价
suspendFlag	int	停牌 1停牌，0 不停牌
period周期为tick时，field字段可选:
field	数据类型	含义
time	int	时间
lastPrice	float	最新价
lastClose	float	前收盘价
open	float	开盘价
high	float	最高价
low	float	最低价
close	float	收盘价
volume	float	成交量
amount	float	成交额
settle	float	今结算
openInterest	float	持仓量
stockStatus	int	停牌 1停牌，0 不停牌
period周期为Level2数据时，字段参考数据结构
返回值

返回dict { stock_code1 : value1, stock_code2 : value2, ... }
value1, value2, ... ：pd.DataFrame 数据集，index为time_list，columns为fields,可参考Bar字段
各标的对应的DataFrame维度相同、索引相同
示例

示例data1返回值data2返回值data3返回值data4返回值历史tick期货五档盘口

# coding:gbk
import pandas as pd
import numpy as np

def init(C):	
	C.stock_list = ["000001.SZ","600519.SH", "510050.SH"]# 指定获取的标的
	C.start_time = "20230901"# 指定获取数据的开始时间
	C.end_time = "20231101"# 指定获取数据的结束时间
	
def handlebar(C):
	# 获取多只股票，多个字段，一条数据
	data1 = C.get_market_data_ex([],C.stock_list, period = "1d",count = 1)
	# 获取多只股票，多个字段，指定时间数据
	data2 = C.get_market_data_ex([],C.stock_list, period = "1d", start_time = C.start_time, end_time = C.end_time)
	# 获取多只股票，多个字段，指定时间15m数据
	data3 = C.get_market_data_ex([],C.stock_list, period = "15m", start_time = C.start_time, end_time = C.end_time)
	# 获取多只股票，指定字段，指定时间15m数据
	data4 = C.get_market_data_ex(["close","open"],C.stock_list, period = "15m", start_time = C.start_time, end_time = C.end_time)
	# 获取多只股票，历史tick
	tick = C.get_market_data_ex([],C.stock_list, period = "tick", start_time = C.start_time, end_time = C.end_time)
	# 获取期货5档盘口tick
	future_lv2_quote = C.get_market_data_ex([],["rb2405.SF","ec2404.INE"], period = "l2quote", count = 1)
	print(data1)
	print(data2["000001.SZ"].tail())
	print(data3)
	print(data4["000001.SZ"])
	print(data4["000001.SZ"].to_csv("your_path")) # 导出文件为csv格式，路径填本机路径
	print(tick["000001.SZ"])
	print(future_lv2_quote)

```