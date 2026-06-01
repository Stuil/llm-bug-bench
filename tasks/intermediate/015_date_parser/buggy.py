def parse_date(date_str):
    parts = date_str.split("-")
    if len(parts) != 3:
        return None
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    return {"year": year, "month": month, "day": day}
