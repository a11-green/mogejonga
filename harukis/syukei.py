from datetime import datetime, timedelta, timezone
from tenhoulog import fetch_lobby_log, ResultBook
from tenhoulog.utils import df2table, start_of_today


class Tools:
    def __init__(self):
        self.JST = timezone(timedelta(hours=+9), "JST")
        # PLAYERS = ["さかかきばら", "kitagaw", "場代負け", "Toshi624", "バラク・オマタ", "鳥谷タカシ", "ニートしたい", "とぅーり王", "ソギモギ皇帝", "遊びたい"]
        self.PLAYERS = ["さかかきばら", "kitagaw", "場代負け", "Toshi624", "バラク・オマタ", "鳥谷タカシ", "ニートしたい", "とぅーり王", "ソギモギ皇帝"]
        self.teams = {
            "そろそろプラスになるズ": ["kitagaw", "バラク・オマタ", "ソギモギ皇帝"],
            "AGE": ["場代負け", "とぅーり王", "ニートしたい"],
            "薄利多売": ["Toshi624", "さかかきばら", "鳥谷タカシ"],
        }
        self.update_book()

    def update_book(self):

        results_c5449 = fetch_lobby_log("C5449")
        results_c6529 = fetch_lobby_log("C6529")
        results_c8823 = fetch_lobby_log("C8823")
        results_c7510 = fetch_lobby_log("C7510")
        results_all = results_c8823 + results_c5449 + results_c6529 + results_c7510
        
        self.book_all = ResultBook.from_results(results_all, self.PLAYERS)
        self.book_season1 = self.book_all.filter_by_period((datetime(2020, 4,  1, 12, 00, tzinfo=self.JST), datetime(2020, 5, 23, 23, 59, tzinfo=self.JST)))
        self.book_season2 = self.book_all.filter_by_period((datetime(2020, 5, 24, 00, 00, tzinfo=self.JST), datetime(2020, 6, 30, 23, 59, tzinfo=self.JST)))
        self.book_season3 = self.book_all.filter_by_period((datetime(2020, 7,  1, 00, 00, tzinfo=self.JST), datetime(2020, 8, 15, 12, 00, tzinfo=self.JST)))
        self.book_season4 = self.book_all.filter_by_period((datetime(2020, 8, 15, 12, 00, tzinfo=self.JST), datetime.now(tz=self.JST)))
        self.book_today = self.book_all.filter_by_period((start_of_today(self.JST), datetime.now(tz=self.JST)))

        self.books = {
            "all"   : self.book_all,
            "1"     : self.book_season1,
            "2"     : self.book_season2,
            "3"     : self.book_season3,
            "4"     : self.book_season4,
            "today" : self.book_today
        }


    def summary(self,season):
        self.update_book()
        book = self.books[season]
        df = book.aggregate(player_num=3).sort_values("得点", ascending=False)
        df_summary = df[["名前", "回数", "得点"]]
        text = df_summary.to_string(
            index=False, 
            formatters={'名前':'{:<8}'.format, "回数":'{:>4}'.format, "得点":'{:>7}'.format})
        print(text)
        return text

    def rank(self,season):
        self.update_book()
        book = self.books[season]
        df = book.aggregate(player_num=3).sort_values("得点", ascending=False)
        df_rank = df[["名前", "順位分布", "平均順位"]]
        text = df_rank.to_string(
            index=False, 
            formatters={'名前':'{:<8}'.format, "順位分布":'{:>9}'.format, "平均順位":'{:>5.2f}'.format})
        print(text)
        return text

    def team(self,season):
        self.update_book()
        book = self.books[season]
        text = ""
        for name, players in self.teams.items():
            score = book.scores[players].fillna(0).values.sum()
            text += "{} : {}\n".format(name,score)
        print(text)
        return text

    def today(self,season):
        self.update_book()
        book = self.books["today"]
        df = book.aggregate(player_num=3).sort_values("得点", ascending=False)
        df_summary = df[["名前", "回数", "得点"]]
        text = df_summary.to_string(
            index=False, 
            formatters={'名前':'{:<8}'.format, "回数":'{:>4}'.format, "得点":'{:>7}'.format})
        print(text)
        return text

    def plot_summary(self,season):
        self.update_book()
        book = self.books[season]
        fig = book.plot_cumsum("scores")
        fig.savefig("scores.png")

    def plot_points_vs_games(self,season):
        self.update_book()
        book = self.books[season]




if __name__ == "__main__":
    # main()
    tools = Tools()
    tools.summary(season="4")
    tools.rank(season="4")
    tools.team(season="4")
    tools.summary(season="today")
    tools.summary(season="all")

    tools.plot_summary(season="4")