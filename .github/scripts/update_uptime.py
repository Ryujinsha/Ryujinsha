"""
Calculates uptime from a fixed birthdate and injects it into README.md.
The README must contain the markers:
  <!-- UPTIME_START --> ... <!-- UPTIME_END -->
"""

import re
from datetime import date

BIRTHDATE = date(2006, 1, 3) 


README_PATH = "README.md"


def calc_uptime(birth: date, today: date) -> str:
    years = today.year - birth.year
    months = today.month - birth.month
    days = today.day - birth.day

    if days < 0:
        months -= 1
        prev_month = today.replace(day=1)
        import calendar
        days_in_prev = calendar.monthrange(prev_month.year, prev_month.month - 1 or 12)[1]
        days += days_in_prev

    if months < 0:
        years -= 1
        months += 12

    return f"{years} years, {months} months, {days} days"


def main():
    today = date.today()
    uptime_str = calc_uptime(BIRTHDATE, today)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    updated = re.sub(
        r"(<!-- UPTIME_START -->).*?(<!-- UPTIME_END -->)",
        rf"\g<1>{uptime_str}\g<2>",
        content,
        flags=re.DOTALL,
    )

    if updated == content:
        print("No change needed.")
        return

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"Uptime updated to: {uptime_str}")


if __name__ == "__main__":
    main()
