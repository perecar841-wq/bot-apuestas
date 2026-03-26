import csv

OUTPUT = "stats.csv"

def generate():
    with open(OUTPUT, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Home Team",
            "Away Team",
            "Avg Goals"
        ])

        sample = [
            ("Real Madrid", "Barcelona", 2.9),
            ("Liverpool", "Chelsea", 2.7),
            ("Bayern", "Dortmund", 3.1)
        ]

        for row in sample:
            writer.writerow(row)

    print("stats.csv generado")

if __name__ == "__main__":
    generate()
