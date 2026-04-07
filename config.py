from datetime import datetime, timezone

def is_tradable(m):
    if not m.get("active"):
        return False
    if m.get("closed"):
        return False
    if not m.get("accepting_orders"):
        return False

    end = m.get("end_date_iso")
    if not end:
        return False

    end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    return end_dt > now