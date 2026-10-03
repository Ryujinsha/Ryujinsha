"""
Calculates uptime from a fixed birthdate and patches the Uptime line in README.md.
Matches the line:   Uptime:     ........ X years, X months, X days
No HTML markers needed in the README.
"""

import re
import calendar
from datetime import date

BIRTHDATE = date(2006, 1, 3)

README_PATH = "README.md"

# Matches the uptime line inside the code block, capturing the prefix
UPTIME_PATTERN = re.compile(
    r"(  Uptime:\s+\.+\s+)\d+ years, \d+ months, \d+ days"
)


def calc_uptime(birth: date, today: date) -> str:
    years = today.year - birth.year
    months = today.month - birth.month
    days = today.day - birth.day

    if days < 0:
        months -= 1
        days_in_prev = calendar.monthrange(
            today.year, today.month - 1 if today.month > 1 else 12
        )[1]
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

    updated = UPTIME_PATTERN.sub(rf"\g<1>{uptime_str}", content)

    if updated == content:
        print("No change needed.")
        return

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"Uptime updated to: {uptime_str}")


if __name__ == "__main__":
    main()
