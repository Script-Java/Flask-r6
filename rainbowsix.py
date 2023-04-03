from bs4 import BeautifulSoup
import requests
from io import BytesIO
import pandas as pd


class R6tracker:
    # grabs name and plat form
    # creates a connection with the website
    def __init__(self, name, platform):
        self.name = name
        self.platform = platform
        self.r6_website = f"https://r6.tracker.network/profile/{platform}/{name}"
        self.response = requests.get(self.r6_website)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def general_info(self):
        # user name
        # gamer Tag
        player_tag = self.soup.find("span", {"class": "trn-profile-header__name"}).string
        stat_value_div = self.soup.findAll("div", {"class": "trn-defstat__value-stylized"})
        stat_value = []
        for stat_value_data in stat_value_div:
            if stat_value_data["class"] == "trn-defstat__value-stylized" or "trn-defstat__value":
                stat_value.append(stat_value_data.string)
        best_mmr = stat_value[0]
        player_level = stat_value[1]
        avg_seasonal_mmr = stat_value[2]
        total_matches = self.soup.find("div", {"class": "trn-card__header-subline"}).string
        total_wins = self.soup.find("div", {"data-stat": "PVPMatchesWon"}).string
        player_win_ratio = self.soup.find("div", {"data-stat": "PVPWLRatio"}).string
        player_total_kills = self.soup.find("div", {"data-stat": "PVPKills"}).string
        player_kd = self.soup.find("div", {"data-stat": "PVPKDRatio"}).string

        # retiving user PFP
        # Grab the image container
        # Then find the img element inside it and with that access the src
        user_profile_img_container = self.soup.find("div", {
            "class": "trn-profile-header__avatar trn-roundavatar trn-roundavatar--white"})
        user_profile = user_profile_img_container.find("img", recursive=False)
        user_pfp_link = user_profile["src"]

        # user PFP optional
        # grabs link and converts into readable data
        response = requests.get(user_pfp_link)

        # pfp Ready.......

        # Find Rank Banner
        # gets best rank
        best_rank_container = self.soup.find("div",
                                             {"class": "trn-card__content trn-card--light trn-defstats-flex pt8 pb8"})
        rank_el = best_rank_container.find("img", recursive=False)
        rank_name = rank_el["title"]
        rank_src = user_profile["src"]
        
        profile_views_span = self.soup.find("span", {"class":"trn-profile-header__views trn-text--dimmed"})
        profile_views = profile_views_span.string
        
        rp_div = self.soup.find("div", {"style":"font-family: Rajdhani; font-size: 3rem;"})
        rp = rp_div.string
        
        rp_banner_container = self.soup.find("div", {"style":"display: flex; align-items: center; line-height: 1; font-weight: 700;"})
        rp_banner_el = rp_banner_container.find("div", {"style":"width: 50px; margin-right: 14px;"})
        rp_banner = rp_banner_el.find("img", recursive=False)
        
        # The rank Img rady.......
        # creating a Dict to store and return all values
        stats_stored = {
            "gamertag": player_tag.strip(),
            "rp":rp.strip(),
            "rp_logo":rp_banner["src"],
            "profile_views": profile_views,
            "best_mmr": best_mmr.strip(),
            "level": player_level.strip(),
            "seasonal_mmr": avg_seasonal_mmr.strip(),
            "total_matches": total_matches.strip(),
            "total_wins": total_wins.strip(),
            "win_ratio": player_win_ratio.strip(),
            "total_kills": player_total_kills.strip(),
            "player_kd": player_kd.strip(),
            "pfp_src": user_pfp_link.strip(),
            "rank_title": rank_name.strip(),
            "best_rank_src": rank_src.strip()
        }
        return stats_stored
        # function to grab top3 operators

    def top_3_ops(self):
        # Div surrounding the container
        top3_container_parent = self.soup.find("div", {"class": "trn-defstat mb0 top-operators"})
        top3_container = top3_container_parent.find("div", {"class": "trn-defstat__value"})
        ops_img_el = top3_container.findAll("img", recursive=False)
        top3_list = []
        top3_src = []
        for img in ops_img_el:
            op_img_src = img["src"]
            op_title_name = img["title"]
            top3_list.append(op_title_name)
            top3_src.append(op_img_src)
        top3_stored = {
            "op_names": top3_list,
            "op_img_src": top3_src
        }
        return top3_stored

    def ranked_stats(self):
        ranked_wins = self.soup.find("div", {"data-stat": "RankedWins"}).string
        ranked_loss = self.soup.find("div", {"data-stat": "RankedLosses"}).string
        ranked_matches = self.soup.find("div", {"data-stat": "RankedMatches"}).string
        ranked_deaths = self.soup.find("div", {"data-stat": "RankedDeaths"}).string
        ranked_kills = self.soup.find("div", {"data-stat": "RankedKills"}).string
        ranked_win_ratio = self.soup.find("div", {"data-stat": "RankedWLRatio"}).string
        ranked_kd = self.soup.find("div", {"data-stat": "RankedKDRatio"}).string
        ranked_kill_per_match = self.soup.find("div", {"data-stat": "RankedKillsPerMatch"}).string
        ranked_stored = {
            "wins": ranked_wins.strip(),
            "losses": ranked_loss.strip(),
            "matches": ranked_matches.strip(),
            "deaths": ranked_deaths.strip(),
            "kills": ranked_kills.strip(),
            "win_ratio": ranked_win_ratio.strip(),
            "kd": ranked_kd.strip(),
            "kpm": ranked_kill_per_match.strip()
        }
        return ranked_stored

    # def mmr_history(self):
    #    url = self.r6_website + "/mmr-history"
    #    response = requests.get(url)
    #    soup = BeautifulSoup(response.content, "html.parser")
    #    table = soup.find("table", {"class":"trn-table"})
    #    tbody = table.find("tbody", recursive=False)
    #    for tr in tbody:
    #        mmr_date = tr.find("div", {"class":"trn-text--dimmed"})
    #        print(mmr_date)
