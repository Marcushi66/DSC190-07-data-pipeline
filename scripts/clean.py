import csv
from datetime import datetime
from pathlib import Path

INPUT = Path("data/raw/events.csv")
OUTPUT = Path("data/clean/events.csv")

COLUMNS = ["user_id", "timestamp", "event_type", "duration_seconds"]

VALID_EVENTS = {"click", "login", "purchase", "scroll", "view"}

TIME_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
)


def normalize_timestamp(value: str) -> str | None:
    for fmt in TIME_FORMATS:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue

    return None


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    clean_rows: list[dict[str, str]] = []

    with INPUT.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        if not reader.fieldnames or any(
            col not in reader.fieldnames for col in COLUMNS
        ):
            raise ValueError("Missing required CSV columns")

        for raw in reader:
            if any(
                raw.get(col) is None or not raw[col].strip()
                for col in COLUMNS
            ):
                continue

            row = {col: raw[col].strip() for col in COLUMNS}

            if row["event_type"] not in VALID_EVENTS:
                continue

            try:
                seconds = int(row["duration_seconds"])
            except ValueError:
                continue

            if seconds <= 0:
                continue

            timestamp = normalize_timestamp(row["timestamp"])

            if timestamp is None:
                continue

            row["timestamp"] = timestamp
            row["duration_seconds"] = str(seconds)
            clean_rows.append(row)

    with OUTPUT.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(clean_rows)

    print(f"Cleaned {len(clean_rows)} rows -> {OUTPUT}")


if __name__ == "__main__":
    main()
