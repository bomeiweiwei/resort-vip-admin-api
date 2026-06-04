from datetime import date, datetime, timedelta


def build_date_list(
    check_in_date: str | date,
    stay_days: int,
) -> list[str]:

    if isinstance(check_in_date, str):
        start_date = datetime.strptime(
            check_in_date,
            "%Y-%m-%d"
        ).date()
    else:
        start_date = check_in_date

    return [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(stay_days)
    ]