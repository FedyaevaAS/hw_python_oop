import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.datetime.now().date()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        total = 0
        for record in self.records:
            if record.date == self.today:
                total += record.amount
        return total

    def get_week_stats(self):
        total = 0
        for record in self.records:
            if self.today - dt.timedelta(days=7) <= record.date <= self.today:
                total += record.amount
        return total

    def get_remainder(self):
        remainder = self.limit - self.get_today_stats()
        return remainder


class Record:
    def __init__(self, amount, comment, date=None):
        date_format = '%d.%m.%Y'
        if date is None:
            self.date = dt.datetime.now().date()
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
        currency_dict = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        rate_dict = {'rub': 1, 'usd': self.USD_RATE, 'eur': self.EURO_RATE}
        remainder = round(self.get_remainder() / rate_dict[self.currency], 2)
        if remainder > 0:
            return (f'На сегодня осталось {remainder} '
                    f'{currency_dict[self.currency]}')
        elif remainder < 0:
            return ('Денег нет, держись: твой долг -' 
                    f' {abs(remainder)} {currency_dict[self.currency]}')
        else:
            return 'Денег нет, держись'
