from datetime import timedelta

from dateutil.utils import today


class DateUtils:
    @staticmethod
    def get_date_range(no_of_days: int, date=None):
        if date is None:
            date = today()
            no_of_days = -no_of_days if no_of_days > 0 else no_of_days
        if no_of_days < 0:
            end_date = date
            start_date = end_date + timedelta(days=no_of_days)
        else:
            start_date = date
            end_date = start_date + timedelta(days=no_of_days)

        return start_date, end_date
