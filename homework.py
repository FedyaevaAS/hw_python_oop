import datetime as dt


class Calculator:
    def __init__(self, limit: int) -> None:
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


class Record:
    def __init__(self, amount, comment, date = None) -> None:
        date_format = '%d.%m.%Y'
        if date == None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()
        self.amount = amount
        self.comment = comment


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remainder = self.limit - self.get_today_stats()
        if remainder > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remainder} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.84
    EURO_RATE = 86.45
    def get_today_cash_remained(self, currency):
        self.currency = currency
        currency_dict = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        exchange_dict = {'rub': 1, 'usd': CashCalculator.USD_RATE, 'eur': CashCalculator.EURO_RATE}
        remainder = round((self.limit - self.get_today_stats())/ exchange_dict[self.currency], 2)
        if remainder > 0:
            return f'На сегодня осталось {remainder} {currency_dict[self.currency]}'
        elif remainder < 0:
            return f'Денег нет, держись: твой долг - {abs(remainder)} {currency_dict[self.currency]}'
        else:
            return 'Денег нет, держись'