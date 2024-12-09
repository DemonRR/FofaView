# FofaView

## 简介
FofaView 是一款基于 Python 与 PyQt6 精心打造的图形界面化 FOFA 客户端。它专为渗透测试人员而设计，凭借简洁直观的操作界面，可助力渗透测试人员迅速且精准地获取 FOFA 平台上的关键信息，极大地提升渗透测试工作的效率与便捷性，使其在网络安全评估与漏洞探测等任务中能够游刃有余地开展工作，为保障网络安全提供强有力的辅助工具支持。
## 使用说明
工具基于Fofa Api进行封装的，win系统下载即可直接使用无需配置任何环境。使用时需要在fofa.ini文件配置高级会员或者普通会员的 API key，普通会员需要充值F币才能使用。
下载地址：https://github.com/DemonRR/FofaView/releases
![image](https://github.com/user-attachments/assets/ee8de294-62e6-4a63-b943-d4a7f2ecc8d1)

## 配置文件
fofa.ini
```
[info]
#fofa会员的key
key = xxxxxx

[fields]
#查询内容选项
fields = host,protocol,ip,port,title,domain,country
#fields可选项：['host', 'title', 'ip', 'domain', 'port', 'country', 'province', 'city', 'country_name', 'header',
#              'server','protocol', 'banner', 'cert', 'isp', 'as_number', 'as_organization', 'latitude',
#              'longitude', 'structinfo','icp', 'fid', 'cname']

[full]
#默认搜索一年内的数据，指定为true即可搜索全部数据，false为一年内数据
full = False
```

