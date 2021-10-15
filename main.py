import excel_writer
from utils import*

import tinvest
from datetime import datetime
from pytz import timezone

file_in = open('my_account.txt', 'r')
TOKEN = file_in.readline()[:-1]
tzstr = file_in.readline()[:-1]
file_in.close()

my_tz = timezone(tzstr)

client = tinvest.SyncClient(TOKEN)
response = client.get_portfolio()
raw_positions = response.payload.positions
usd_course = get_usd_course(get_current_date(my_tz))
from_ = my_tz.localize(datetime(2000, 1, 1, 0, 0))
to = my_tz.localize(datetime.now())
raw_operations = client.get_operations(from_, to).payload.operations


if __name__ == '__main__':
    portfolio_positions = get_portfolio_positions(raw_positions, usd_course)
    portfolio_total_value, america_value_in_rub, russia_value_in_rub, others_value_in_rub, stocks_value_in_rub, bonds_value_in_rub, cash_value_in_rub = get_portfolio_total_value(client,
                                                                                                                                                                                  portfolio_positions)
    total_pay_in = get_total_pay_in(raw_operations)

    excel_writer.write_table(
        client, portfolio_positions, portfolio_total_value, total_pay_in, america_value_in_rub, russia_value_in_rub, others_value_in_rub, stocks_value_in_rub, bonds_value_in_rub, cash_value_in_rub)
