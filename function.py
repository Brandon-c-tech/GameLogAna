import os
import csv
import time

targetpath = os.getcwd()
filename = os.listdir(targetpath) # 获取程序所在目录的所有文件及文件夹
targetfile = [] # 用于储存符合需求的文件名
targettype = ".log" # 筛选的后缀

# 筛选出当前目录下的目标文件，并储存到targetfile中
i = 0
while i < len(filename):
    if targettype in filename[i]:
        targetfile.append(filename[i])
    i += 1

# 关键词表
KeywordList = [
'AI','shoot','True','deleted', #  
'get','get, horse','get, shield','get, coin_v_1',
'Name, get, horse','Name, get, shield','Name, get, coin_v_1',
'gen, horse','gen, shield',
'Remake','Name, shoot','shoot, Name','Name, shoot, Name','Name, get'] # 玩家分析关键词表
KeywordFreq = [0 for i in KeywordList]

i = 0
Keyword = {}
while i < len(KeywordList):
    Keyword[KeywordList[i]] = 0
    i += 1

# 从日志筛选含关键词特定行并计数的函数
def keyline(keyword,InputLogname):
    OriginalLog = open(targetpath + "\\" + InputLogname,"r",encoding = 'UTF-8')
    count = len(open(targetpath + "\\" + InputLogname,'r',encoding = 'UTF-8').readlines())
    i = 0
    j = 0
    while i < count:
        line = OriginalLog.readline()
        if keyword in line:
            j += 1
        i += 1
    OriginalLog.close
    return j

Outcsv = []
LevelTimeList = []
i = 0
while i < len(targetfile): # 对目录里的每一个目标类型文件执行一次
    InputLog = targetfile[i]
    i += 1
    k = 0
    while k < len(KeywordList): # 每一个目标类型文件的每一个关键词都执行一次
        KeywordFreq[k] = keyline(KeywordList[k],InputLog)
        Keyword[KeywordList[k]] = keyline(KeywordList[k],InputLog)
        print(Keyword)
        k += 1
    Outcsvline = [InputLog]
    Outcsvline.extend(KeywordFreq)
    with open(InputLog,"r") as f: # 输出处理过的文件的版本信息
        lines = f.readlines()
        LevelTime = lines[-2][0:5] # 本局游戏的时间长度，需要根据日志格式调整
        LevelTime = int(float(LevelTime)) # 获取日志最后一行
    Outcsvline.append(LevelTime)
    Outcsv.append(Outcsvline)

csvhead = []
csvhead = KeywordList
csvhead.insert(0,'logname')
csvhead.append('LevelTime')
with open("{name}.csv".format(name = 'Report-' + time.strftime('%m-%d-%H-%M-%S', time.localtime())),"w") as csvfile: # 创建csv文件
    writer = csv.writer(csvfile)
    writer.writerow(csvhead) # 写入csv表头
    writer.writerows(Outcsv) # 写入csv内容