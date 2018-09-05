import re

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
#关键字函数，进行headers的各个字段的筛选与清理。
def dealwith_parameter(parameter,r):
    #可能存在某些网页headers的字段是小写情况，所以这里加了一个小写情况的判定
    parameter_lower = parameter.lower()
    parameter = str(str(re.findall(parameter+'.*?(?:\' )+',r)).strip("[]").strip('" \'').split(": "))\
                    .strip("[]").replace(", ",": ") + ", " + '\n'
    #如果大写情况字段满足条件（为空）则进行小写情况判断，不满足条件直接返回大写情况结果
    if parameter == "'', \n":
        parameter1 = str(str(re.findall(parameter_lower + '.*?(?:\' )+', r)).strip("[]").strip('" \'').split(": "))\
                         .strip("[]").replace(", ",": ",1) + ", " + '\n'
        #如果小写情况不存在则输出为空
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

    headers = "headers = {\n"+Origin+Accept_Encoding+Accept_Language+Upgrade_Insecure_Requests+User_Agent+Content_Type+Accept+Cache_Control+Referer+Connection+"}"+'\n'
    print(headers)



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
    #url选取清理
    url = str(re.findall('curl.*?(?:\' )', r)).strip("[]' ").split(" ")[1]
    #由于data字段很少有网页有所包含，所以这里加了一个判断语句用来打印data
    if  data != []:
        print("r = requests.post(" + url + ", headers=headers, cookies=cookies, data=data,)")
    else:
        print("r = requests.post(" + url + ", headers=headers, cookies=cookies,)")
    print("print(r.text)")

main()