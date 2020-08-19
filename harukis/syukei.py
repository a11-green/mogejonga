from datetime import datetime, timedelta, timezone
from tenhoulog import fetch_lobby_log, ResultBook
from tenhoulog.utils import df2table, start_of_today
class Tools:
    def __init__(self):
        from datetime import datetime, timedelta, timezone
        from tenhoulog import fetch_lobby_log, ResultBook
        from tenhoulog.utils import df2table, start_of_today

        self.JST = timezone(timedelta(hours=+9), "JST")
        # PLAYERS = ["さかかきばら", "kitagaw", "場代負け", "Toshi624", "バラク・オマタ", "鳥谷タカシ", "ニートしたい", "とぅーり王", "ソギモギ皇帝", "遊びたい"]
        self.PLAYERS = ["さかかきばら", "kitagaw", "場代負け", "Toshi624", "バラク・オマタ", "鳥谷タカシ", "ニートしたい", "とぅーり王", "ソギモギ皇帝"]

    def main(self):
        results_c5449 = fetch_lobby_log("C5449")
        results_c6529 = fetch_lobby_log("C6529")
        results_c8823 = fetch_lobby_log("C8823")
        results_all = results_c8823 + results_c5449 + results_c6529

        with open("test.txt",'w') as f:
            for line in results_all:
                f.write("{}\n".format(line))

        book = ResultBook.from_results(results_all, self.PLAYERS)
        book_season1 = book.filter_by_period((datetime(2020, 4,  1, 12, 00, tzinfo=self.JST), datetime(2020, 5, 23, 23, 59, tzinfo=self.JST)))
        book_season2 = book.filter_by_period((datetime(2020, 5, 24, 00, 00, tzinfo=self.JST), datetime(2020, 6, 30, 23, 59, tzinfo=self.JST)))
        book_season3 = book.filter_by_period((datetime(2020, 7,  1, 00, 00, tzinfo=self.JST), datetime(2020, 8, 15, 12, 00, tzinfo=self.JST)))
        book_season4 = book.filter_by_period((datetime(2020, 8, 15, 12, 00, tzinfo=self.JST), datetime.now(tz=self.JST)))
        book_today = book.filter_by_period((start_of_today(self.JST), datetime.now(tz=self.JST)))
        # 全体
        print(df2table(book.aggregate(3).sort_values("得点", ascending=False)))
        # シーズン1
        print(df2table(book_season1.aggregate(3).sort_values("得点", ascending=False)))
        # シーズン2
        print(df2table(book_season2.aggregate(3).sort_values("得点", ascending=False)))
        # シーズン3
        print(df2table(book_season3.aggregate(3).sort_values("得点", ascending=False)))
        # シーズン4
        print(df2table(book_season4.aggregate(3).sort_values("得点", ascending=False)))
        # 今日の結果
        print(df2table(book_today.aggregate(3).sort_values("得点", ascending=False)))
        # チーム別
        teams = {
            "そろそろプラスになるズ": ["kitagaw", "バラク・オマタ", "ソギモギ皇帝"],
            "AGE": ["場代負け", "とぅーり王", "ニートしたい"],
            "薄利多売": ["Toshi624", "さかかきばら", "鳥谷タカシ"],
        }
        for name, self.PLAYERS in teams.items():
            score = book_season4.scores[players].fillna(0).values.sum()
            print(name, ":", score)
        # # グラフ
        # fig = book.plot_cumsum("scores")
        # fig.savefig("scores.png")
        # fig = book.plot_cumsum("tips")
        # fig.savefig("tips.png")

        print(type(book))

    def all_results(self):
        results_c5449 = fetch_lobby_log("C5449")
        results_c6529 = fetch_lobby_log("C6529")
        results_c8823 = fetch_lobby_log("C8823")
        results_all = results_c8823 + results_c5449 + results_c6529
        book = ResultBook.from_results(results_all, self.PLAYERS)
        return book


    def season_summary(self,sten):
        book = self.all_results()
        book_season = book.filter_by_period(sten)
        df_season = book_season.aggregate(player_num=3).sort_values("得点", ascending=False)
        df_season_summary = df_season[["名前", "回数", "得点"]]
        text = df_season_summary.to_string(
            index=False, 
            formatters={'名前':'{:<8}'.format, "回数":'{:>4}'.format, "得点":'{:>7}'.format})
        print(text)
        return text

    def season_rank(self,sten):
        book = self.all_results()
        book_season = book.filter_by_period(sten)
        df_season = book_season.aggregate(player_num=3).sort_values("得点", ascending=False)
        df_season_rank = df_season[["名前", "順位分布", "平均順位"]]
        text = df_season_rank.to_string(
            index=False, 
            formatters={'名前':'{:<8}'.format, "順位分布":'{:>9}'.format, "平均順位":'{:>5.2f}'.format})
        print(text)
        return text

    def season_team(self,sten):
        teams = {
            "そろそろプラスになるズ": ["kitagaw", "バラク・オマタ", "ソギモギ皇帝"],
            "AGE"               : ["場代負け", "とぅーり王", "ニートしたい"],
            "薄利多売"            : ["Toshi624", "さかかきばら", "鳥谷タカシ"],
        }
        book = self.all_results()
        book_season = book.filter_by_period(sten)
        text = ""
        for name, players in teams.items():
            score = book_season.scores[players].fillna(0).values.sum()
            text += "{} : {}\n".format(name,score)
        print(text)
        return text

if __name__ == "__main__":
    # main()
    tools = Tools()
    tools.season_summary((datetime(2020, 8, 15, 12, 00, tzinfo=tools.JST), datetime.now(tz=tools.JST)))
    tools.season_rank((datetime(2020, 8, 15, 12, 00, tzinfo=tools.JST), datetime.now(tz=tools.JST)))
    tools.season_team((datetime(2020, 8, 15, 12, 00, tzinfo=tools.JST), datetime.now(tz=tools.JST)))