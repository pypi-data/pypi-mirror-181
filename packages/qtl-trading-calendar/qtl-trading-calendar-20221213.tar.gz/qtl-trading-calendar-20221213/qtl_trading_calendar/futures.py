from datetime import date, time, datetime, timedelta
from pathlib import Path
import tomllib

from .utils import is_weekend


class FuturesTradingCalendar:

    def __init__(self):
        self.config = dict()
        self.init_config()

        # tips
        #   这里的日期为自然日，非交易结算日
        #   周末没有日盘与夜盘，程序逻辑排除
        self.start_date = self.config['start_date']
        self.end_date = self.config['end_date']

        # Special cases
        self.no_day_trading_dates = set(self.config['holiday_dates'])
        self.no_night_trading_dates = set(self.config['holiday_dates']) | set(self.config['no_night_trading_dates'])

    def init_config(self):
        config_file_path = Path(__file__).parent / 'data' / 'futures.toml'
        self.config = tomllib.loads(config_file_path.read_text(encoding='utf-8'))

    def check_date(self, d: date):
        if not (self.start_date <= d <= self.end_date):
            raise AttributeError('Out of Calendar Date Range...')

    def has_day_trading(self, d: date):
        self.check_date(d)
        if is_weekend(d):
            return False
        if d in self.no_day_trading_dates:
            return False
        return True

    def has_night_trading(self, d: date):
        self.check_date(d)
        if is_weekend(d):
            return False
        if d in self.no_night_trading_dates:
            return False
        return True

    def is_trading_day(self, d: date):
        return self.has_day_trading(d) or self.has_night_trading(d)

    def get_trading_day(self, dt: datetime):
        dt_date = dt.date()
        dt_time = dt.time()

        # 日盘
        if time(3, 0) <= dt_time < time(18, 0):
            if self.has_day_trading(dt_date):
                return dt_date
            else:
                return None

        # 夜盘，深夜
        elif dt_time >= time(18, 0):
            if self.has_night_trading(dt_date):
                return self.next_trading_day(dt_date)
            else:
                return None

        # 夜盘，凌晨
        elif dt_time < time(3, 0):
            d = dt_date - timedelta(days=1)
            if self.has_night_trading(d):
                return self.next_trading_day(d)
            else:
                return None

    def current_trading_day(self):
        now = datetime.now()
        return self.get_trading_day(now)

    def next_trading_day(self, d: date, n=1):
        count = 0
        while True:
            d = d + timedelta(days=1)
            if self.is_trading_day(d):
                count += 1
                if count >= n:
                    return d

    def previous_trading_day(self, d: date, n=1):
        count = 0
        while True:
            d = d - timedelta(days=1)
            if self.is_trading_day(d):
                count += 1
                if count >= n:
                    return d
