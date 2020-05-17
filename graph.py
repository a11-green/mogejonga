# coding:utf-8

import numpy as np 
import pandas as pd
import re
import matplotlib.pyplot as plt

def graph_plot():
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
    pointSumA = [0] # 浅野
    pointSumB = [0] # 混同
    pointSumC = [0] # 長屋
    pointSumD = [0] # 諏訪
    pointSumE = [0] # 枝松　
    pointSumF = [0] # 土橋
    pointSumG = [0] # 落合
    pointSumH = [0] # 闘莉王
    LIST = []
    print(float("-2.0"))

    # lines: リスト。要素は1行の文字列データ
    for line in lines[1:]:
        if len(line) > 10: #変な行は飛ばす
            roomid  = line.split("|")[0]
            time    = line.split("|")[1]
            rools   = line.split("|")[2]
            players = line.split("|")[3]
            l = re.split('[ ()]', players)
            LIST.append([l[1],float(l[2].replace("+",""))])
            LIST.append([l[4],float(l[5].replace("+",""))])
            LIST.append([l[7],float(l[8].replace("+",""))])
    # print(LIST)
    for i,data in enumerate(LIST):
        player  = data[0]
        point   = data[1]
        if player == "場代負け":
            pointsA.append(point)
            pointSumA.append(pointSumA[-1]+point)
        elif player == "バラク・オマタ":
            pointsB.append(point)
            pointSumB.append(pointSumB[-1]+point)
        elif player == "ソギモギ皇帝":
            pointsC.append(point)
            pointSumC.append(pointSumC[-1]+point)
        elif player == "鳥谷タカシ":
            pointsD.append(point)
            pointSumD.append(pointSumD[-1]+point)
        elif player == "さかかきばら":
            pointsE.append(point)
            pointSumE.append(pointSumE[-1]+point)
        elif player == "ニートしたい":
            pointsF.append(point)
            pointSumF.append(pointSumF[-1]+point)
        elif player == "Toshi624":
            pointsG.append(point)
            pointSumG.append(pointSumG[-1]+point)
        elif (player == "遊びたい") or (player == "とぅーり王"):
            pointsH.append(point)
            pointSumH.append(pointSumH[-1]+point)

            
    xA = [i for i in range(len(pointsA))]
    xB = [i for i in range(len(pointsB))]
    xC = [i for i in range(len(pointsC))]
    xD = [i for i in range(len(pointsD))]
    xE = [i for i in range(len(pointsE))]
    xF = [i for i in range(len(pointsF))]
    xG = [i for i in range(len(pointsG))]
    xH = [i for i in range(len(pointsH))]

    plt.clf()

    plt.plot(xA,pointSumA,label="asano")
    plt.plot(xB,pointSumB,label="kondo")
    plt.plot(xC,pointSumC,label="nagaya")
    plt.plot(xD,pointSumD,label="suwa")
    plt.plot(xE,pointSumE,label="edamatsu")
    plt.plot(xF,pointSumF,label="tsuchihashi")
    plt.plot(xG,pointSumG,label="ochiai")
    plt.plot(xH,pointSumH,label="nakayama")

    plt.legend()
    # plt.xlim(0,300)
    plt.savefig("test.png")


    playerName = ["場代負け","バラク・オマタ","ソギモギ皇帝","鳥谷タカシ","さかかきばら","ニートしたい","Toshi624","遊びたい"]
    df = pd.DataFrame(index=playerName, columns=playerName)
    df = df.fillna(0.0).copy()
    df2 = df.copy()

    print(df)

    for i in range(0,len(LIST),3):
        data1 = LIST[i]
        data2 = LIST[i+1]
        data3 = LIST[i+2]
        players = [data1[0],data2[0],data3[0]]
        points = [data1[1],data2[1],data3[1]]
        df.loc[players[0],players[1]] += points[0]
        df.loc[players[0],players[2]] += points[0]
        df.loc[players[1],players[2]] += points[1]
        df.loc[players[1],players[0]] += points[1]
        df.loc[players[2],players[0]] += points[2]
        df.loc[players[2],players[1]] += points[2]

        df2.loc[players[0],players[1]] += points[0] - points[1]
        df2.loc[players[0],players[2]] += points[0] - points[2]
        df2.loc[players[1],players[2]] += points[1] - points[2]
        df2.loc[players[1],players[0]] += points[1] - points[0]
        df2.loc[players[2],players[0]] += points[2] - points[0]
        df2.loc[players[2],players[1]] += points[2] - points[1]

    print(df)
    df.to_csv("test.csv")
    df2.to_csv("test2.csv")



#     if playerName[0] in players:
#         ind = np.where(players=playerName[0])
#         print(ind)
#         print(players[ind],players[ind-1],players[ind-2])

