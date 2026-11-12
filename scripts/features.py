import csv
from datetime import datetime
from pathlib import Path

INPUT = Path("data/transformed/events.csv")
OUTPUT = Path("data/features/events.csv")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with INPUT.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        if reader.fieldnames is None:
            raise ValueError("Missing CSV header")

        columns = reader.fieldnames + ["duration_minutes", "weekday"]

        with OUTPUT.open("w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=columns)
            writer.writeheader()

            count = 0

            for row in reader:
                seconds = int(row["duration_seconds"])

                row["duration_minutes"] = str(seconds / 60)

                event_date = datetime.strptime(row["date"], "%Y-%m-%d")
                row["weekday"] = event_date.strftime("%A")

                writer.writerow(row)
                count += 1

    print(f"Generated features for {count} rows -> {OUTPUT}")


if __name__ == "__main__":
    main()
