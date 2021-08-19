import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        date = dt.date.today()
        total = sum(record.amount for record in self.records 
                if record.date == date)
        return total

    def get_week_stats(self):
        date = dt.date.today()
        date_week_ago = date - dt.timedelta(days=7)
        total = sum(record.amount for record in self.records
                if date_week_ago <= record.date <= date)
        return total

    def get_remainder(self):
        remainder = self.limit - self.get_today_stats()
        return remainder


class Record:
    def __init__(self, amount, comment, date=None):
        date_format = '%d.%m.%Y'
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()
        self.amount = amount
        self.comment = comment


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remainder = self.get_remainder()
        if remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {remainder} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.84
    EURO_RATE = 86.45

    def get_today_cash_remained(self, currency):
        self.currency = currency
        currency_dict = {'rub': ('руб', 1), 
                         'usd': ('USD', self.USD_RATE), 
                         'eur': ('Euro', self.EURO_RATE)}
        currency_label, rate = currency_dict[currency]
        remainder = round(self.get_remainder() / rate, 2)
        abs_remainder = abs(remainder)
        if remainder > 0:
            return (f'На сегодня осталось {remainder} '
                    f'{currency_label}')
        elif remainder < 0:
            return ('Денег нет, держись: твой долг - '
                    f'{abs_remainder} {currency_label}')
        else:
            return 'Денег нет, держись'
