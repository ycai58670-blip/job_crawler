# 猎聘职位抓取工具

按关键词抓取猎聘职位信息，并导出为Excel文件。关键词可在config.py中KEYWORD = ""修改。

## 文件功能：

scrape_jobs_to_excel.py：程序入口、抓取流程编排
config.py：关键词、分页、认证、输出路径等配置
liepin_api.py：HTTP 会话、请求参数和接口调用
job_parser.py：职位字段解析和分页判断
excel_export.py：数据去重及 Excel 导出

## 安装依赖

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 配置认证信息

接口需要浏览器会话中的认证信息。请在 PowerShell 中设置当前会话的环境变量，不要把真实 Token 或 Cookie 写进代码或提交到 GitHub：

```powershell
$env:LIEPIN_XSRF_TOKEN="实际的X-XSRF-TOKEN"
$env:LIEPIN_SK_ID="实际的skId"
$env:LIEPIN_FK_ID="实际的fkId"
$env:LIEPIN_CK_ID="实际的ckId"
# 如接口需要 Cookie，再设置：
# $env:LIEPIN_COOKIE="实际的Cookie"
```

这些值可以从浏览器开发者工具 Network 中对应的请求 Headers 和 Payload 获取。具体操作如下：


1.进入猎聘官网，点击职位；


2.f12打开“开发者工具”，点击“网络”，勾选“保留日志”，点击“清除网络日志”，点击“Fetch/XHR”并刷新页面，在网页中点击筛选条件；


3.在“名称”栏，即左侧栏找到“https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job”这个URL：
LIEPIN_XSRF_TOKEN:“标头”拉至最下查看
skId，fkId，ckId：从“负载”中passThroughForm查看
Cookie：“标头”下查看

## 运行

```powershell
python .\scrape_jobs_to_excel.py
```

## 声明
1.代码涉及的爬虫技术仅用于演示 HTTP 请求原理与数据解析方法，请勿将相关代码用于任何违反目标网站服务条款、用户协议或相关法律法规的行为。

2.在使用爬虫程序前，请务必查阅目标网站的 robots.txt 文件，并严格遵守其规定。

3.大规模、高频次的数据抓取可能对目标服务器造成压力，请控制请求频率，避免影响网站正常运营。

4.所抓取的数据涉及企业及个人信息，请勿传播、出售或用于任何侵犯他人隐私及知识产权的用途。

5.因使用本文代码所产生的任何法律责任，由使用者自行承担，作者不负任何连带责任。
