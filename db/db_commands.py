import pandas
from datetime import datetime


def get_data():
    """
    Фукнция получает данные из .xlsx файла, передает эти данные функциям-конвертаторам, после чего
    формирует из валидных данных список кортежей
    :return: список кортежей (дата, число)
    """
    data_list = []
    delta_list = []
    excel_data = pandas.read_excel('testData.xlsx', sheet_name='Лист1')
    data = pandas.DataFrame(excel_data)
    for date, delta in data.values:
        data_list.append(date_conversion(date))
        delta_list.append(delta_conversion(delta))
    return list(zip(data_list, delta_list))


def date_conversion(date):
    """
    Функция конвертирует дату из одного формата в другой. Если дата приходит изначально
    в нужном формате, тогда она просто возвращается
    :param date: дата в формате %d.%m.%Y
    :return: дата в формате %Y-%m-%d
    """
    try:
        date_object = datetime.strptime(date, '%d.%m.%Y')
        valid_date = date_object.strftime('%Y-%m-%d')
    except ValueError:
        return date
    return valid_date


def delta_conversion(delta):
    """
    Функция принимает на вход строку, удаляет лишние символы, заменяет символ ',' на '.'
    :param delta: строка с необработанным числом
    :return: число с плавающей точкой
    """
    valid_delta = str(delta).replace('`', '').replace(',', '.')
    return float(valid_delta)
