# cURL(bash)自动生成requests请求

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

## 支持
目前已支持 豆瓣，知乎，哔哩哔哩动画（修改requests方法为get）等大型网站
还在陆续更新中。。

