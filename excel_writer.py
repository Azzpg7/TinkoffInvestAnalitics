import xlsxwriter
from decimal import Decimal


def format_worksheet(worksheet, bold):

    worksheet.set_column(0, 0, 42)
    worksheet.set_column(1, 1, 5)
    worksheet.set_column(3, 3, 15)
    worksheet.set_column(4, 4, 7)
    worksheet.set_column(5, 5, 23)
    worksheet.set_column(6, 6, 12)

    worksheet.write(0, 0, 'Name', bold)
    worksheet.write(0, 1, 'Ticker', bold)
    worksheet.write(0, 2, 'Currency', bold)
    worksheet.write(0, 3, 'Average_position', bold)
    worksheet.write(0, 4, 'Balance', bold)
    worksheet.write(0, 5, 'Expected_yield_in_currency', bold)
    worksheet.write(0, 6, 'Value_in_RUB', bold)
    worksheet.write(0, 7, 'Part_in_%', bold)


def write_table(client, positions, portfolio_total_value, total_pay_in, america_value_in_rub, russia_value_in_rub, others_value_in_rub, stocks_value_in_rub, bonds_value_in_rub, cash_value_in_rub):
    workbook = xlsxwriter.Workbook('Portfolio.xlsx')  # Creating table
    worksheet = workbook.add_worksheet('Positions')  # Creating worksheet
    bold = workbook.add_format({'bold': 1})

    format_worksheet(worksheet, bold)

    cur_row = 1

    currency_format = workbook.add_format({'num_format': '0.00'})
    for position in positions:
        worksheet.write(cur_row, 0, position.name)
        if position.ticker != 'USD000UTSTOM':
            worksheet.write(cur_row, 1, position.ticker)
        worksheet.write(
            cur_row, 2, position.currency)
        worksheet.write_number(
            cur_row, 3, position.average_position, currency_format)
        worksheet.write_number(cur_row, 4, position.balance)
        color_format = workbook.add_format(
            {'num_format': '[Red]0.00'}) if position.expected_yield < 0 else workbook.add_format({'num_format': '[Green]0.00'})
        worksheet.write_number(
            cur_row, 5, position.expected_yield, color_format)
        worksheet.write_number(
            cur_row, 6, position.value_in_rub, currency_format)
        worksheet.write_number(cur_row, 7, Decimal('100') *
                               position.value_in_rub/portfolio_total_value, currency_format)
        cur_row += 1

    worksheet.write(cur_row, 0, 'Русские деревянные')
    worksheet.write(cur_row, 2, 'RUB')
    worksheet.write(cur_row, 6, client.get_portfolio_currencies(
    ).payload.currencies[1].balance)
    worksheet.write(cur_row, 7, Decimal('100')*client.get_portfolio_currencies(
    ).payload.currencies[1].balance/portfolio_total_value, currency_format)

    cur_row += 3
    worksheet.write(cur_row, 0, "America_part_in_%", bold)
    worksheet.write_number(cur_row, 1, Decimal(
        '100')*america_value_in_rub/portfolio_total_value, currency_format)
    cur_row += 1

    worksheet.write(cur_row, 0, "Russia_part_in_%", bold)
    worksheet.write_number(cur_row, 1, Decimal(
        '100')*russia_value_in_rub/portfolio_total_value, currency_format)
    cur_row += 1

    worksheet.write(cur_row, 0, "OtherWorld_part_in_%", bold)
    worksheet.write_number(cur_row, 1, Decimal(
        '100')*others_value_in_rub/portfolio_total_value, currency_format)
    cur_row += 2

    worksheet.write(cur_row, 0, "Stocks_part_in_%", bold)
    worksheet.write_number(cur_row, 1, Decimal(
        '100')*stocks_value_in_rub/portfolio_total_value, currency_format)
    cur_row += 1

    worksheet.write(cur_row, 0, "Bonds_part_in_%", bold)
    worksheet.write_number(cur_row, 1, Decimal(
        '100')*bonds_value_in_rub/portfolio_total_value, currency_format)
    cur_row += 1

    worksheet.write(cur_row, 0, "Cash_part_in_%", bold)
    worksheet.write_number(cur_row, 1, Decimal(
        '100')*cash_value_in_rub/portfolio_total_value, currency_format)
    cur_row += 1

    cur_row += 3

    worksheet.write(cur_row, 0, "Total_value", bold)
    cur_row += 1
    worksheet.write_number(cur_row, 0, portfolio_total_value, currency_format)
    cur_row += 1

    worksheet.write(cur_row, 0, "Total_pay_in", bold)
    cur_row += 1
    worksheet.write_number(cur_row, 0, total_pay_in, currency_format)
    cur_row += 1

    worksheet.write(cur_row, 0, "Profit_in_%", bold)
    cur_row += 1
    profit = Decimal('100') * (portfolio_total_value -
                               total_pay_in)/(total_pay_in)
    color_format = color_format = workbook.add_format(
        {'num_format': '[Red]0.00'}) if profit < 0 else workbook.add_format({'num_format': '[Green]0.00'})
    worksheet.write_number(cur_row, 0, profit, color_format)

    workbook.close()
