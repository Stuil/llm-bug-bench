from datetime import datetime

def parse_date(date_str):
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return {"year": dt.year, "month": dt.month, "day": dt.day}
        except ValueError:
            continue
    return None
