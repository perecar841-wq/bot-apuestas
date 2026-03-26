import requests
import time
import json
import os
import csv
import hashlib

TELEGRAM_TOKEN = "8653119493:AAE_hZmqjkox00pvBmZiQkmYWxryy_bGImU"
CHAT_ID = "1379756875"

CSV_MAIN = "juegos.csv"
CSV_STATS = "stats.csv"
HIST = "historial.json"

def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def load(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def uid(x):
    return hashlib.md5(x.encode()).hexdigest()

def load_stats():
    stats = {}
    if not os.path.exists(CSV_STATS):
        return stats

    with open(CSV_STATS, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            key = r["Home Team"] + " vs " + r["Away Team"]
            stats[key] = r
    return stats

def run():
    stats = load_stats()
    picks = []

    if not os.path.exists(CSV_MAIN):
        return picks

    with open(CSV_MAIN, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for r in reader:
            try:
                match = f"{r['Home Team']} vs {r['Away Team']}"

                odds = float(r["Moneyline 1"])
                prob = float(r["Probability 1"]) / 100
                public = float(r["Public % ML Team 1"])
                cash = float(r["ALL Cash % Team 1"])

                ev = (prob * odds) - 1
                sharp = public > 65 and cash < 50

                goals_edge = False
                corners_edge = False

                if match in stats:
                    avg_goals = float(stats[match]["Avg Goals"])

                    if avg_goals > 2.5:
                        goals_edge = True

                    if avg_goals > 2.8:
                        corners_edge = True

                score = 0
                if ev > 0.02: score += 1
                if sharp: score += 1
                if goals_edge: score += 1
                if corners_edge: score += 1

                if score >= 2:
                    picks.append(
                        f"{match}\nEV: {round(ev,3)}\nSharp: {sharp}\nGoles: {goals_edge}\nCorners: {corners_edge}"
                    )

            except:
                continue

    return picks[:5]

def main():
    hist = load(HIST)
    picks = run()

    for p in picks:
        h = uid(p)
        if h not in hist:
            send("🔥 PICK PRO\n\n" + p)
            hist[h] = True

    save(HIST, hist)

if __name__ == "__main__":
    while True:
        os.system("python stats_generator.py")
        main()
        time.sleep(600)
