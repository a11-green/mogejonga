# coding:utf-8

import numpy as np 
import pandas as pd
import re
import matplotlib.pyplot as plt

def graph_plot(tip):
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
    print(float("-2.0"))

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

    plt.clf()

    plt.plot(xA,pointSumA,label="asano")
    plt.plot(xB,pointSumB,label="kondo")
    plt.plot(xC,pointSumC,label="nagaya")
    plt.plot(xD,pointSumD,label="suwa")
    plt.plot(xE,pointSumE,label="edamatsu")
    plt.plot(xF,pointSumF,label="tsuchihashi")
    plt.plot(xG,pointSumG,label="ochiai")
    plt.plot(xH,pointSumH,label="nakayama")
    plt.plot(xI,pointSumI,label="kitagawa")

    plt.legend()
    plt.savefig("test.png")

    plt.clf()
    plt.plot(xA,tipSumA,label="asano")
    plt.plot(xB,tipSumB,label="kondo")
    plt.plot(xC,tipSumC,label="nagaya")
    plt.plot(xD,tipSumD,label="suwa")
    plt.plot(xE,tipSumE,label="edamatsu")
    plt.plot(xF,tipSumF,label="tsuchihashi")
    plt.plot(xG,tipSumG,label="ochiai")
    plt.plot(xH,tipSumH,label="nakayama")
    plt.plot(xI,tipSumI,label="kitagawa")
    plt.legend()
    plt.savefig("test2.png")



if __name__ == "__main__":
    graph_plot(tip=True)