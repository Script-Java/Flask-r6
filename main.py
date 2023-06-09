from flask import Flask
from flask import render_template, request
from rainbowsix import R6tracker

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        platform = request.form.get("platform")
        r6 = R6tracker(username, platform)
        # R6 General Stats
        general = r6.general_info()
        ranked = r6.ranked_stats()
        # overall data
        player_tag = general["gamertag"]
        best_mmr = general["best_mmr"]
        level = general["level"]
        season_mmr = general["seasonal_mmr"]
        matches = general["total_matches"]
        wins = general["total_wins"]
        win_ratio = general["win_ratio"]
        kills = general["total_kills"]
        kd = general["player_kd"]
        pfp_src = general["pfp_src"]
        best_rank_src = general["best_rank_src"]
        best_rank = general["rank_title"]
        rp = general["rp"]
        rp_logo = general["rp_logo"]
        profile_views = general["profile_views"]
        
        r_wins = ranked["wins"]
        r_loss = ranked["losses"]
        r_matches = ranked["matches"]
        r_death = ranked["deaths"]
        r_kills  = ranked["kills"]
        r_win_ratio = ranked["win_ratio"]
        r_kd = ranked["kd"]
        r_kpm = ranked["kpm"]
        
        return render_template("result.html",
                               n=username,
                               player_tag=player_tag,
                               best_mmr=best_mmr,
                               level=level,
                               season_mmr=season_mmr,
                               matches=matches,
                               wins=wins,
                               win_ratio=win_ratio,
                               kills=kills,
                               kd=kd,
                               best_rank=best_rank,
                               best_rank_src=best_rank_src,
                               pfp_src=pfp_src,
                               rp=rp,
                               rp_logo=rp_logo,
                               profile_views=profile_views,
                               r_wins = r_wins,
                               r_loss = r_loss,
                               r_matches = r_matches,
                               r_death = r_death,
                               r_kills = r_kills,
                               r_win_ratio = r_win_ratio,
                               r_kd = r_kd,
                               r_kpm = r_kpm
                               )
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
