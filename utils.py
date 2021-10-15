from datetime import datetime
from pycbrf.toolbox import ExchangeRates
from decimal import Decimal
from classes import Position

# Write tickers that you refer to America
# 'USD000UTSTOM' is USD ticker
america_tickers = ['FXIM', 'TECH', 'SBSP',
                   'TSPX', 'TBIO', 'VTBH', 'USD000UTSTOM']
# Write tickers that you refer to Russia
russian_tickers = ['SBMX', 'FXRU', 'VTBB', 'TMOS', 'TBRU']
# Write tickers that you refer to Otherworld
otherworld_tickers = ['FXDM', 'FXRW', 'VTBE', 'FXDE', 'FXWO', 'FXCN']
# Write tickers that you refer to stocks
stocks_tickers = ['FXDM', 'FXIM', 'FXRW', 'SBMX', 'VTBE',
                  'FXDE', 'TECH', 'SBSP', 'FXWO', 'TMOS', 'TSPX', 'TBIO', 'FXCN']
# Write tickers that you refer to bonds
bonds_tickers = ['FXRU', 'VTBB', 'VTBH', 'TBRU']


def get_current_date(time_zone) -> str:
    now = time_zone.localize(datetime.now()).strftime("%Y-%m-%d")
    return now


def get_usd_course(date: datetime) -> Decimal:
    rates = ExchangeRates(date)
    return rates['USD'].value


def get_portfolio_total_value(client, positions) -> Decimal:
    america_value_in_rub = Decimal('0')
    russia_value_in_rub = Decimal('0')
    others_value_in_rub = Decimal('0')
    stocks_value_in_rub = Decimal('0')
    bonds_value_in_rub = Decimal('0')
    cash_value_in_rub = Decimal('0')
    portfolio_total_value = Decimal('0')

    rub_in_portfolio = client.get_portfolio_currencies(
    ).payload.currencies[1].balance  # 1 is index of rubs
    portfolio_total_value += rub_in_portfolio
    russia_value_in_rub += rub_in_portfolio
    cash_value_in_rub += rub_in_portfolio
    for position in positions:
        portfolio_total_value += position.value_in_rub
        if(position.ticker == 'USD000UTSTOM'):
            cash_value_in_rub += position.value_in_rub
        if(position.ticker in america_tickers):
            america_value_in_rub += position.value_in_rub
        if(position.ticker in russian_tickers):
            russia_value_in_rub += position.value_in_rub
        if(position.ticker in otherworld_tickers):
            others_value_in_rub += position.value_in_rub
        if(position.ticker in stocks_tickers):
            stocks_value_in_rub += position.value_in_rub
        if(position.ticker in bonds_tickers):
            bonds_value_in_rub += position.value_in_rub

    return portfolio_total_value, america_value_in_rub, russia_value_in_rub, others_value_in_rub, stocks_value_in_rub, bonds_value_in_rub, cash_value_in_rub


def get_portfolio_positions(raw_positions, usd_course):
    portfolio_positions = []
    for position in raw_positions:
        current_position = Position()
        current_position.name = str(position.name)
        current_position.ticker = str(position.ticker)
        current_position.currency = str(
            position.average_position_price.currency.value)
        current_position.average_position = Decimal(
            str(position.average_position_price.value))
        current_position.balance = Decimal(str(position.balance))
        current_position.expected_yield = Decimal(
            str(position.expected_yield.value))
        current_ticker_cost = current_position.average_position * \
            current_position.balance + current_position.expected_yield
        if current_position.currency == 'USD':
            current_ticker_cost *= usd_course
        current_position.value_in_rub = current_ticker_cost
        portfolio_positions.append(current_position)
    return portfolio_positions


def get_total_pay_in(raw_operations):
    total_pay_in = Decimal('0')
    for operation in raw_operations:
        if operation.operation_type.value == "PayIn":
            if operation.currency.value == 'USD':
                usd_course_on_this_date = get_usd_course(operation.date)
                total_pay_in += Decimal(str(operation.payment)
                                        ) * usd_course_on_this_date
            else:
                total_pay_in += Decimal(str(operation.payment))
    return total_pay_in


# def write_operations_in_csv(raw_operations):
#     csv_rows = []
#     csv_rows.append(",".join([
#         "date",
#         "comission_value",
#         "currency",
#         "figi",
#         "instrument_type",
#         "operation_type",
#         "payment",
#         "price",
#         "quantity",
#         "status"
#     ]))

#     for operation in raw_operations:
#         csv_rows.append(",".join(map(str, [
#             operation.date,
#             operation.commission.value if operation.commission else '',
#             operation.currency.value,
#             operation.figi or '',
#             operation.instrument_type.value if operation.instrument_type else '',
#             operation.operation_type.value,
#             operation.payment,
#             operation.price or '',
#             operation.quantity or '',
#             operation.status.value
#         ])))
#         csv_rows.append("\n")
#     with open("operations.csv", "w") as f:
#         f.write("\n".join(csv_rows))
