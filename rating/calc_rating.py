# import os
# import pprint
# import time
# import urllib.error
# import urllib.request
# import gzip
# import shutil
# import datetime
import re
# from datetime import date,timedelta
import matplotlib.pyplot as plt
# import download4

def initialize_rating(initial_file):
    
    with open(initial_file) as f:
        init_ratings = f.readlines() 

    rating = {}
    games  = {}
    rating_history = {}
    
    for l in init_ratings:
        player      = l.split()[0]
        init_rating = l.split()[1] 
        init_games  = l.split()[2]
        rating[player] = float(init_rating) 
        games[player]  = int(init_games)
        rating_history[player] = [float(init_rating)]
        print(games)
    
    return rating,games,rating_history

def calc_rating(initial_rating,initial_games,initial_rating_history,logfile,tip=False):
    with open(logfile) as f:
        lines = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)

    rating = initial_rating
    games  = initial_games
    rating_history = initial_rating_history

    for line in lines[1:]:
        # print(games)

        if len(line) > 10: #変な行は飛ばす
         
            roomid  = line.split("|")[0]
            time    = line.split("|")[1]
            rools   = line.split("|")[2]
            players = line.split("|")[3]
            # 祝儀なしの場合
            
            if tip == False:
                l = re.split('[ ()]', players)

                player1 = l[1].replace("遊びたい","とぅーり王")
                player2 = l[4].replace("遊びたい","とぅーり王")
                player3 = l[7].replace("遊びたい","とぅーり王")
                

            # 祝儀ありの場合
            if tip == True:
                l = re.split('[ (,)]', players)

                player1 = l[1].replace("遊びたい","とぅーり王")
                player2 = l[5].replace("遊びたい","とぅーり王")
                player3 = l[9].replace("遊びたい","とぅーり王")


            rate_average = (rating[player1]+rating[player2]+rating[player3])/3.0
            rate_average = round(rate_average,3)
            if rate_average < 1500.0:
                rate_average = 1500.0

            # print(rate_average)

            print(player1,player2,player3)
            # 試合数補正
            if games[player1] < 400:
                games_correction1 = 1.0 - games[player1]*0.002
            if games[player1] >= 400:
                games_correction1 = 0.2
            if games[player2] < 400:
                games_correction2 = 1.0 - games[player2]*0.002
            if games[player2] >= 400:
                games_correction2 = 0.2
            if games[player3] < 400:
                games_correction3 = 1.0 - games[player3]*0.002
            if games[player3] >= 400:
                games_correction3 = 0.2

            # 平均R補正
            averageR_correction1 = (rate_average - rating[player1])/40.0
            averageR_correction2 = (rate_average - rating[player2])/40.0
            averageR_correction3 = (rate_average - rating[player3])/40.0

            # Rating変動
            rate_delta1 = round(games_correction1 * ( 30.0  + averageR_correction1 ) * 1.0, 3) # 1st
            rate_delta2 = round(games_correction2 * ( 0.0   + averageR_correction2 ) * 1.0, 3) # 2nd
            rate_delta3 = round(games_correction3 * ( -30.0 + averageR_correction3 ) * 1.0, 3) # 3rd
            print(rate_delta1,rate_delta2,rate_delta3)

            # rate_delta1 = 30.0
            # rate_delta2 = 0.0
            # rate_delta3 = -30.0
            

            # Rating
            rating[player1] += rate_delta1
            rating[player2] += rate_delta2
            rating[player3] += rate_delta3

            # Rating History
            rating_history[player1].append(rating[player1]) 
            rating_history[player2].append(rating[player2]) 
            rating_history[player3].append(rating[player3])             

            # Games
            games[player1] += 1
            games[player2] += 1
            games[player3] += 1

            # print("場代負け　{}".format(rating["場代負け"]))

            # print(rating_history["バラク・オマタ"])


    

    return rating,games,rating_history

def rating_plot(rating_history):

    plt.clf()
    names = {"場代負け":"asano","バラク・オマタ":"kondo","ソギモギ皇帝":"nagaya","鳥谷タカシ":"suwa","さかかきばら":"edamatsu","ニートしたい":"tsuchihashi","Toshi624":"ochiai","とぅーり王":"king","kitagaw":"kitagawa"}
    for player in rating_history.keys():
        x = [i for i in range(len(rating_history[player]))]
        y = rating_history[player]
        plt.plot(x,y,linewidth=0.5,alpha=0.5)
        plt.scatter(x[-1],y[-1],label=names[player])
        plt.text(x[-1],y[-1]+5,int(y[-1]))

    plt.legend()
    plt.savefig("rating.png")
    

if __name__ == "__main__":
    r,g,h = initialize_rating("rating.txt")
    r,g,h = calc_rating(r,g,h,"logvol1.txt",tip=False)
    r,g,h = calc_rating(r,g,h,"logvol2.txt",tip=True)
    r,g,h = calc_rating(r,g,h,"logvol3.txt",tip=True)

    rating_plot(h)
    