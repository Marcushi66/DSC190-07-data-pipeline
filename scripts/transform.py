import csv
from datetime import datetime
from pathlib import Path

INPUT = Path("data/clean/events.csv")
OUTPUT = Path("data/transformed/events.csv")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with INPUT.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        if reader.fieldnames is None:
            raise ValueError("Missing CSV header")

        columns = reader.fieldnames + ["date"]

        with OUTPUT.open("w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=columns)
            writer.writeheader()

            count = 0

            for row in reader:
                timestamp = datetime.fromisoformat(row["timestamp"])
                row["date"] = timestamp.strftime("%Y-%m-%d")

                writer.writerow(row)
                count += 1

    print(f"Transformed {count} rows -> {OUTPUT}")


if __name__ == "__main__":
    main()
