# jd-tools

JD 工具包。 

[![PyPI version](https://badge.fury.io/py/jd-tools.svg)](https://pypi.python.org/pypi/jd-tools)
[![Python](https://img.shields.io/pypi/pyversions/jd-tools)](https://pypi.python.org/pypi/jd-tools)
[![Downloads](https://img.shields.io/pypi/dm/jd-tools)](https://pypi.python.org/pypi/jd-tools)


## 安装

```
pip install jd-tools
```

## 示例

```
from jd_tools import *

print(JdTools.trim("  12b   "))

dd = JdTools.str_to_datetime('2022-09-10 8:10:15')
print(dd)

输出
12b
2022-09-10 08:10:15
```


## 模块内方法说明

| 函数、对象名称            | 类型    | 说明                          |
|---------------------------|---------|-------------------------------|
| dc_gen_code               | 函数    | 生成单据编号， 例如 0001-XH-181008-001 |
| dc_records_changed        | 函数    | 修改记录（全量）， 判断在原纪录基础上的删、改、增情况。 |
| start_end_time            | 函数    | 返回 日期 tm(today, this-month, ...) ，对应的开始和结束日期 |
| start_end_time_ex         | 函数    | 返回 日期 tm，对应的开始和结束日期，带时间段描述 |
| name_list                 | 函数    | 提取列表元素中的特定名称，过滤空值和重复值，返回字符串 |
| sum_list                  | 函数    | 提取列表元素 some_list 中的现金券总面值 |
| sum_ticket                | 函数    | 提取列表元素 some_list(数组中数组) 中的现金券总面值 |
| humanize_date_delta       | 函数    | 将时间差转换为友好格式，如“7天”，“3个月”，“2年” |
| JdCalendar                | 对象    | 日历，计算 本周、上周、本月、上月的起止日期 |
| JdTools                   | 对象    | 主工具类，类型转换、日期转换、转decimal等 |
| JdDate                    | 对象    | 日期相关工具函数 |
| JdImage                   | 对象    | 图片处理公共类 |
| JdList                    | 对象    | 列表求索引 |
| JdPath                    | 对象    | 目录处理类， 反斜杠替换为斜杠等 |
| aes_decrypt               | 函数    | AES_GSM 解密， 腾讯相关推送接口数据解密用 |
| Core                      | 对象    | http/https post/get 请求发送对象 |
| jd_concat                 | 函数    | 字符串拼接，网关 + 路径，去除多余斜杠(/) |
| jd_create_key             | 函数    | 生成随机 key |
| get_nonce                 | 函数    | 生成随机字符串 |
| aes_gcm_encrypt           | 函数    | AES_GCM加密 |
| aes_gcm_decrypt           | 函数    | AES_GCM解密 |
| aes_cbc_encrypt           | 函数    | AES_CBC加密 zero padding |
| aes_ecb_encrypt           | 函数    | AES_ECB加密数据 |
| aes_ecb_decrypt           | 函数    | AES-AES_ECB解密数据 |
| generate_map              | 函数    | 将 子表记录，根据主表id，缓存到 map表  1:N |
| generate_map_ex           | 函数    | 将 记录，根据 主表id，缓存到 map表   1:1 |
| cyt_map                   | 函数    | 将记录，根据 args 提供的 key，缓存到 map表 |
| gen_key                   | 函数    | 生成key， 为 generate_map, cyt_map 使用 |
| notify_decrypt            | 函数    | AES_GSM 解密， 腾讯相关推送接口数据解密用 |
| is_windows_os             | 函数    | 是否 Windows 操作系统 |
| get_hostname              | 函数    | 获取主机名称 |
| get_ip                    | 函数    | 获取IP |
| TimeMeasure               | 对象    | 测量时间对象 |
| timeit                    | 函数    | 测量函数执行时长装饰器 |
| move_file                 | 函数    | 移动文件 |
| copy_file                 | 函数    | 拷贝文件 |
| zip_dir                   | 函数    | 压缩指定文件夹 |
| make_dirs                 | 函数    | 创建多级目录 |
| logger                    | 对象    | 日志对象 |
| jd_config_logger          | 函数    | 配置日志对象 |
| jd_set_logger_file_handler| 函数    | 配置日志对象文件名 |
| JdRsa                     | 对象    | RSA 对象 |
| jd_decrypt                | 函数    | RSA 解密 |
| remove_rsa_public_header  | 函数    | 移除 RSA 公钥数据头部 |
| remove_rsa_private_header | 函数    | 移除 RSA 私钥数据头部 |
| JdCheck                   | 对象    | 输入参数校验， 用于 web 请求参数校验 |
| JdThreadPool              | 对象    | 线程池 |
| AvatarDirMgr              | 对象    | 文件上传管理器 |
| Avatar                    | 对象    | 单文件上传路径处理对象 |

## 修改记录

[修改记录](CHANGELOG.md)
