from functions import *
import pytest
import pandas as pd


def test_correct_input():
    simple = "join SmallTable1.csv SmallTable2.csv key2to1 inner"
    with_spaces = "join       aaaaaaa            bssssss           ssssc     dsaasaa"
    complex = "join C:/file C://file2 length join3"
    default = "join kk ff aa"

    assert enter_input(simple) == ('SmallTable1.csv', 'SmallTable2.csv', 'key2to1', 'inner')
    assert enter_input(with_spaces) == ('aaaaaaa', 'bssssss', 'ssssc', 'dsaasaa')
    assert enter_input(complex) == ('C:/file', 'C://file2', 'length', 'join3')
    assert enter_input(default) == ('kk', 'ff', 'aa', 'inner')


def test_input_eception():
    wrong_num_of_elements = "join abamza  aa"
    wrong_command = "hjoin a b c d"

    with pytest.raises(NameError):
        enter_input(wrong_num_of_elements)
    with pytest.raises(Exception):
        enter_input(wrong_command)


def test_reading_file():
    file_name1 = 'SmallTable1.csv'
    file_name2 = 'SmallTable2.csv'

    assert read_headers(file_name1, file_name2) == (
        ['key2to1', 'key1to2', 'some_column'], ['key1to2', 'key2to1', 'some_column2'])
    assert read_headers(file_name2, file_name1) == (
        ['key1to2', 'key2to1', 'some_column2'], ['key2to1', 'key1to2', 'some_column'])


def test_check_column_numbers():
    header1 = ['column1', 'column4', 'column8']
    header2 = ['column8', 'column1', 'column0', 'col3']
    fake_column_name = 'some_column11'
    column1 = 'column1'
    column2 = 'column8'

    with pytest.raises(Exception):
        check_column_numbers(header1, header2, fake_column_name)

    assert check_column_numbers(header1, header2, column1) == (0, 1)
    assert check_column_numbers(header2, header1, column1) == (1, 0)
    assert check_column_numbers(header1, header2, column2) == (2, 0)
    assert check_column_numbers(header2, header1, column2) == (0, 2)


def test_write_table():
    file_name1 = 'SmallTable1.csv'
    file_name2 = 'SmallTable2.csv'
    i1 = iter(write_table(file_name1))
    i2 = iter(write_table(file_name2))

    assert next(i1)[0] == 'key2to1'
    assert next(i1)[1] == 'NULL'

    assert next(i2) == ['key1to2', 'key2to1', 'some_column2']
    assert next(i2) == ['1', 'NULL', 'kk']


def test_inner_joiner():
    file_path1 = 'SmallTable1.csv'
    file_path2 = 'SmallTable2.csv'

    header1, header2 = read_headers(file_path1, file_path2)
    result = check_column_numbers(header1, header2, 'key2to1')
    for i in inner_joiner(result[0], result[1], file_path1, file_path2):
        assert i[result[0]] == i[result[1] + len(header1)]


def test_joiners():
    file_path1 = 'SmallTable1.csv'
    file_path2 = 'SmallTable2.csv'
    column = 'key2to1'
    column2 = 'key1to2'

    header1, header2 = read_headers(file_path1, file_path2)
    result = check_column_numbers(header1, header2, column)
    result2 = check_column_numbers(header1, header2, column2)

    a = pd.read_csv(file_path1, encoding='UTF=16')
    b = pd.read_csv(file_path2, encoding='UTF=16')

    merged_left = a.merge(b, on=column, how='left')
    merged_right = a.merge(b, on=column, how='right')
    merged_inner = a.merge(b, on=column, how='inner')
    merged_full = a.merge(b, on=column, how='outer')

    merged_left2 = a.merge(b, on=column2, how='left')
    merged_right2 = a.merge(b, on=column2, how='right')
    merged_inner2 = a.merge(b, on=column2, how='inner')
    merged_full2 = a.merge(b, on=column2, how='outer')


    num0 = 0
    for num, i in enumerate(left_joiner(result[0], result[1], file_path1, file_path2, header2)):
        num0 = num
    assert num0 == len(merged_left)

    for num, i in enumerate(right_joiner(result[0], result[1], file_path1, file_path2, header1)):
        num0 = num
    assert num0 == len(merged_right)

    for num, i in enumerate(inner_joiner(result[0], result[1], file_path1, file_path2)):
        num0 = num
    assert num0 == len(merged_inner)

    for num, i in enumerate(full_joiner(result[0], result[1], file_path1, file_path2, header1, header2)):
        num0 = num
    assert num0 == len(merged_full)

    for num, i in enumerate(left_joiner(result2[0], result2[1], file_path1, file_path2, header2)):
        num0 = num
    assert num0 == len(merged_left2)

    for num, i in enumerate(right_joiner(result2[0], result2[1], file_path1, file_path2, header1)):
        num0 = num
    assert num0 == len(merged_right2)

    for num, i in enumerate(inner_joiner(result2[0], result2[1], file_path1, file_path2)):
        num0 = num
    assert num0 == len(merged_inner2)

    for num, i in enumerate(full_joiner(result2[0], result2[1], file_path1, file_path2, header1, header2)):
        num0 = num
    assert num0 == len(merged_full2)