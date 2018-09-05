# cURL(bash)自动生成request请求

## 前言

当我们用requests库写cookies，headers时非常麻烦而又浪费时间，于是我想到了一种可以快速解决这种问题的方案。因为cURL(bash)中含有网页的cookies，headers，data等请求信息，可以用re正则表达式进行选取再进行数据清理最终使得自动生成request请求。

## cURL(bash)提取

我们以知乎为例，登录知乎之后，在网页点击F12进入开发者模式，然后右键选择Copy再选择Copy as cURL(bash)。

![1.png](https://upload-images.jianshu.io/upload_images/5498924-b25e4b22d36f7583.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这是我们得到的cURL(bash)，因为cookie字段含有个人信息，所以这里我用“privacy=1”表示。

`curl 'https://www.zhihu.com/' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.8' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'cache-control: max-age=0' -H 'authority: www.zhihu.com' -H 'cookie: privacy=1' -H 'referer: https://www.zhihu.com/signup?next=%2F' --compressed`

## 编译环境

* Win10操作系统
* Python3.6语言版本
* Google Chrome浏览器
* Pycharm编译软件

## 项目步骤

> * 主函数编写
> * Cookies编写
> * Data编写
> * Headers编写

## 相关库调用

```python
import re
```

## 主函数编写

```python
def main():
    #输入
    text = str(input("请输入CURL:"))
    print("import requests")
    #尾部无用信息清理
    r = text.replace(" --compressed", "").strip()
    #cookies，data，headers函数调用
    dealwith_cookies(r)
    data = []
    dealwith_data(r,data)
    dealwith_headers(r)
    #url字段re正则选取清理
    url = str(re.findall('curl.*?(?:\' )', r)).strip("[]' ").split(" ")[1]
    #由于data字段很少有网页有所包含，所以这里加了一个判断语句用来打印data
    if  data != []:
        print("r = requests.post(" + url + ", headers=headers, cookies=cookies, data=data,)")
    else:
        print("r = requests.post(" + url + ", headers=headers, cookies=cookies,)")
    print("print(r.text)")
```

## Cookies编写

```python
def dealwith_cookies(r):
    #re正则选取cookie字段
    cookie = re.findall('cookie.*?(?:\' )|Cookie.*?(?:\' )',r)
    #数据清洗打印
    cookie = eval(str(cookie).strip("[]")).strip(" ")
    cookie = cookie[:-1].split(": ")
    cookie = cookie[1].split("; ")
    print("cookies = {")
    for i in cookie:
        l = str(i.split("=",1)).strip("[]").replace(", ",": ",1)+','
        print(l)
    print("}\n")
```

## Data编写

```python
def dealwith_data(r,datas):
    #re正则选取data字段
    data = re.findall('data.*',r)
    #如果data字段不为[]则进行数据清理与打印
    if data!=[]:
        data = str(data).strip("[]' ").replace('"','').split(' ')
        data = str(data[1]).split("^&")
        for i in data:
            t = str(i.split("=")).strip("[]")
            datas.append(eval(t))
        data = "data = " + str(datas)
        print(data)
```

## Header编写

```python
#关键字函数，进行header的各个字段的筛选与清理。
def dealwith_parameter(parameter,r):
    #可能存在某些网页headers的字段是小写情况，所以这里加了一个小写情况的判定
    parameter_lower = parameter.lower()
    parameter = str(str(re.findall(parameter+'.*?(?:\' )+',r)).strip("[]")\
    .strip('" \'').split(": ")).strip("[]").replace(", ",": ") + ", " + '\n'
    #如果大写情况字段满足条件（为空）则进行小写情况判断，不满足条件直接返回大写情况结果
    if parameter == "'', \n":
        parameter1 = str(str(re.findall(parameter_lower + '.*?(?:\' )+', r))\
                     .strip(" []").strip('" \'').split(": ")).strip("[]")\
                     .replace(", ",": ",1) + ", " + '\n'
        #如果小写情况不存在则最终输出为空
        if parameter1 =="'', \n":
            return ""
        else:return parameter1
    else:return parameter

def dealwith_headers(r):
    #分别调用关键字函数最后进行汇总打印
    Accept_Encoding = dealwith_parameter("Accept_Encoding",r)
    Origin = dealwith_parameter("Origin",r)
    Accept_Language = dealwith_parameter("Accept-Language",r)
    Upgrade_Insecure_Requests = dealwith_parameter("Upgrade-Insecure-Requests",r)
    User_Agent = dealwith_parameter("User-Agent",r)
    Content_Type = dealwith_parameter("Content-Type",r)
    Accept = dealwith_parameter("Accept:",r)
    Cache_Control = dealwith_parameter("Cache-Control",r)
    Referer = dealwith_parameter("Referer",r)
    Connection = dealwith_parameter("Connection",r)

    headers = "headers ={\n"+Origin+Accept_Encoding+Accept_Language+Upgrade_Insecure_Requests\
    +User_Agent+Content_Type+Accept+Cache_Control+Referer+Connection+"}"+"\n"
    print(headers)
```

## 运行结果

输入刚才得到的cURL(bash)，运行结果为

```python
import requests
cookies = {
'privacy': '1',
}

headers = {
'accept-language': 'zh-CN,zh;q=0.8', 
'upgrade-insecure-requests': '1', 
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36', 
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
'cache-control': 'max-age=0', 
}

r = requests.post('https://www.zhihu.com/', headers=headers, cookies=cookies,)
print(r.text)

```

运用完整的cookies进行运行并复制运行结果进行验证，最终得到了直接登录后的网页源码。

![2.png](https://upload-images.jianshu.io/upload_images/5498924-bb4fbf1319016f2f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



![3.png](https://upload-images.jianshu.io/upload_images/5498924-725eb9a8e90bd8a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



