# coding:utf-8

import numpy as np 
import pandas as pd
import re
import matplotlib.pyplot as plt

def sumup(tip):
    

    f = open('log.txt')
    lines = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    f.close()
    pointsA   = [0] # 浅野
    pointsB   = [0] # 混同
    pointsC   = [0] # 長屋
    pointsD   = [0] # 諏訪
    pointsE   = [0] # 枝松　
    pointsF   = [0] # 土橋
    pointsG   = [0] # 落合
    pointsH   = [0] #　闘莉王
    pointsI   = [0] # はるきさん
    pointSumA = [0] # 浅野
    pointSumB = [0] # 混同
    pointSumC = [0] # 長屋
    pointSumD = [0] # 諏訪
    pointSumE = [0] # 枝松　
    pointSumF = [0] # 土橋
    pointSumG = [0] # 落合
    pointSumH = [0] # 闘莉王
    pointSumI = [0] # はるきさん
    tipA   = [0] # 浅野
    tipB   = [0] # 混同
    tipC   = [0] # 長屋
    tipD   = [0] # 諏訪
    tipE   = [0] # 枝松　
    tipF   = [0] # 土橋
    tipG   = [0] # 落合
    tipH   = [0] #　闘莉王
    tipI   = [0] # はるきさん
    tipSumA = [0] # 浅野
    tipSumB = [0] # 混同
    tipSumC = [0] # 長屋
    tipSumD = [0] # 諏訪
    tipSumE = [0] # 枝松　
    tipSumF = [0] # 土橋
    tipSumG = [0] # 落合
    tipSumH = [0] # 闘莉王
    tipSumI = [0] # はるきさん
    LIST = []
   

    # lines: リスト。要素は1行の文字列データ
    for line in lines[1:]:
        if len(line) > 10: #変な行は飛ばす
            roomid  = line.split("|")[0]
            time    = line.split("|")[1]
            rools   = line.split("|")[2]
            players = line.split("|")[3]
            # 祝儀なしの場合
            if tip == False:
                l = re.split('[ ()]', players)
                LIST.append([l[1],float(l[2].replace("+",""))])
                LIST.append([l[4],float(l[5].replace("+",""))])
                LIST.append([l[7],float(l[8].replace("+",""))])
            # 祝儀ありの場合
            if tip == True:
                l = re.split('[ (,)]', players)
                print(l)
                LIST.append([l[1],float(l[2].replace("+","")),float(l[3].replace("+","").replace("枚",""))])
                LIST.append([l[5],float(l[6].replace("+","")),float(l[7].replace("+","").replace("枚",""))])
                LIST.append([l[9],float(l[10].replace("+","")),float(l[11].replace("+","").replace("枚",""))])


    # print(LIST)
    for i,data in enumerate(LIST):
        player  = data[0]
        point   = data[1]
        if tip == True:
            tips    = data[2]
        if player == "場代負け":
            pointsA.append(point)
            pointSumA.append(pointSumA[-1]+point)
            if tip == True:
                tipA.append(tips)
                tipSumA.append(tipSumA[-1]+tips)
        elif player == "バラク・オマタ":
            pointsB.append(point)
            pointSumB.append(pointSumB[-1]+point)
            if tip == True:
                tipB.append(tips)
                tipSumB.append(tipSumB[-1]+tips)
        elif player == "ソギモギ皇帝":
            pointsC.append(point)
            pointSumC.append(pointSumC[-1]+point)
            if tip == True:
                tipC.append(tips)
                tipSumC.append(tipSumC[-1]+tips)
        elif player == "鳥谷タカシ":
            pointsD.append(point)
            pointSumD.append(pointSumD[-1]+point)
            if tip == True:
                tipD.append(tips)
                tipSumD.append(tipSumD[-1]+tips)
        elif player == "さかかきばら":
            pointsE.append(point)
            pointSumE.append(pointSumE[-1]+point)
            if tip == True:
                tipE.append(tips)
                tipSumE.append(tipSumE[-1]+tips)
        elif player == "ニートしたい":
            pointsF.append(point)
            pointSumF.append(pointSumF[-1]+point)
            if tip == True:
                tipF.append(tips)
                tipSumF.append(tipSumF[-1]+tips)
        elif player == "Toshi624":
            pointsG.append(point)
            pointSumG.append(pointSumG[-1]+point)
            if tip == True:
                tipG.append(tips)
                tipSumG.append(tipSumG[-1]+tips)
        elif player == "遊びたい":
            pointsH.append(point)
            pointSumH.append(pointSumH[-1]+point)
            if tip == True:
                tipH.append(tips)
                tipSumH.append(tipSumH[-1]+tips)
        elif player == "とぅーり王":
            pointsH.append(point)
            pointSumH.append(pointSumH[-1]+point)
            if tip == True:
                tipH.append(tips)
                tipSumH.append(tipSumH[-1]+tips)
        elif player == "kitagaw":
            pointsI.append(point)
            pointSumI.append(pointSumI[-1]+point)
            if tip == True:
                tipI.append(tips)
                tipSumI.append(tipSumI[-1]+tips)

            
    xA = [i for i in range(len(pointsA))]
    xB = [i for i in range(len(pointsB))]
    xC = [i for i in range(len(pointsC))]
    xD = [i for i in range(len(pointsD))]
    xE = [i for i in range(len(pointsE))]
    xF = [i for i in range(len(pointsF))]
    xG = [i for i in range(len(pointsG))]
    xH = [i for i in range(len(pointsH))]
    xI = [i for i in range(len(pointsI))]

    with open("summary.txt",'w') as f:
        if tip == True:
            f.write("NAME POINTS GAMES\n")
            f.write("場代負け {} {} {}\n".format(pointSumA[-1],xA[-1],tipSumA[-1]))
            f.write("バラク・オマタ {} {} {}\n".format(pointSumB[-1],xB[-1],tipSumB[-1]))
            f.write("ソギモギ皇帝 {} {} {}\n".format(pointSumC[-1],xC[-1],tipSumC[-1]))
            f.write("鳥谷タカシ {} {} {}\n".format(pointSumD[-1],xD[-1],tipSumD[-1]))
            f.write("さかかきばら {} {} {}\n".format(pointSumE[-1],xE[-1],tipSumE[-1]))
            f.write("ニートしたい {} {} {}\n".format(pointSumF[-1],xF[-1],tipSumF[-1]))
            f.write("Toshi624 {} {} {}\n".format(pointSumG[-1],xG[-1],tipSumG[-1]))
            f.write("とぅーり王 {} {} {}\n".format(pointSumH[-1],xH[-1],tipSumH[-1]))
            f.write("kitagaw {} {} {}\n".format(pointSumI[-1],xI[-1],tipSumI[-1]))
        if tip == False:
            f.write("NAME POINTs GAMEs TIPs\n")
            f.write("場代負け {} {}\n".format(pointSumA[-1],xA[-1]))
            f.write("バラク・オマタ {} {}\n".format(pointSumB[-1],xB[-1]))
            f.write("ソギモギ皇帝 {} {}\n".format(pointSumC[-1],xC[-1]))
            f.write("鳥谷タカシ {} {}\n".format(pointSumD[-1],xD[-1]))
            f.write("さかかきばら {} {}\n".format(pointSumE[-1],xE[-1]))
            f.write("ニートしたい {} {}\n".format(pointSumF[-1],xF[-1]))
            f.write("Toshi624 {} {}\n".format(pointSumG[-1],xG[-1]))
            f.write("とぅーり王 {} {}\n".format(pointSumH[-1],xH[-1]))
            f.write("kitagaw {} {}\n".format(pointSumI[-1],xI[-1]))



    

if __name__ == "__main__":
    sumup(tip=True)