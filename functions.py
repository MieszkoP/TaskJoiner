import re
import csv

def enter_input(a):
    '''A function that takes the commands entered and turns them into a list '''
    if len(re.findall("join\s+\S+\s+\S+\s+\S+\s+\S+", a))>0:
        b = re.findall("join\s+\S+\s+\S+\s+\S+\s+\S+", a)[0]
        default_join = False
    elif len(re.findall("join\s+\S+\s+\S+\s+\S+", a))>0:
        b = re.findall("join\s+\S+\s+\S+\s+\S+", a)[0]
        default_join = True
    else:
        raise NameError(
            'The command should look like this: join file_path file_path column_name join_type(left, right, inner or full)')
    if b != a:
        raise NameError(
            'The command should look like this: join file_path file_path column_name join_type(left, right, inner or full)')
    inputs = re.findall("\S+", b)
    file_path1 = inputs[1]
    file_path2 = inputs[2]
    column_name = inputs[3]
    join_type = 'inner'
    if not default_join:
        join_type = inputs[4]
    return file_path1, file_path2, column_name, join_type

def read_headers(file_name1, file_name2): #Reads headers
    with open(file_name1, 'r', encoding="UTF-16") as file:
        csvreader = csv.reader(file)
        header1 = next(csvreader)

    with open(file_name2, 'r', encoding="UTF-16") as file:
        csvreader = csv.reader(file)
        header2 = next(csvreader)
    return header1, header2


def check_column_numbers(header1, header2, column_name): #Checks which column is in which position
    if column_name not in header1 or column_name not in header2:
        raise Exception('No such column!')
    return header1.index(column_name), header2.index(column_name)

def write_table(file_name): #Wypisuje elementy tabeli
    with open(file_name, 'r', encoding="UTF-16") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            yield row

def inner_joiner(column_index_first_table, column_index_sec_table, file_name1, file_name2): #Zwraca iterator po wierszach inner join
    with open(file_name1, 'r', encoding="UTF-16") as file1:
        csvreader = csv.reader(file1)
        for row1 in csvreader:
            with open(file_name2, 'r', encoding="UTF-16") as file2:
                csvreader2 = csv.reader(file2)
                for row2 in csvreader2:
                    if row1[column_index_first_table] == row2[column_index_sec_table] and row1[column_index_first_table] != 'NULL':
                        yield (row1 + row2)


def left_joiner(column_index_first_table, column_index_sec_table, file_name1, file_name2, header2): #Zwraca iterator po wierszach left join
    with open(file_name1, 'r', encoding="UTF-16") as file1:
        csvreader = csv.reader(file1)
        for row1 in csvreader:
            with open(file_name2, 'r', encoding="UTF-16") as file2:
                csvreader2 = csv.reader(file2)
                was = False
                for row2 in csvreader2:
                    if row1[column_index_first_table] == row2[column_index_sec_table] and row1[column_index_first_table] != 'NULL':
                        yield (row1 + row2)
                        was = True
                if not was:
                    yield (row1 + ['NULL'] * len(header2))


def right_joiner(column_index_first_table, column_index_sec_table, file_name1, file_name2, header1):
    for i in inner_joiner(column_index_first_table, column_index_sec_table, file_name1, file_name2):
        yield i
    with open(file_name2, 'r', encoding="UTF-16") as file2:
        csvreader2 = csv.reader(file2)
        for i, row2 in enumerate(csvreader2):
            if i != 0:
                with open(file_name1, 'r', encoding="UTF-16") as file1:
                    csvreader1 = csv.reader(file1)
                    was = False
                    for row1 in csvreader1:
                        if row1[column_index_first_table]==row2[column_index_sec_table] and row2[column_index_sec_table] != 'NULL':
                            was = True
                    if not was:
                        yield (['NULL']*len(header1)+row2)


def full_joiner(column_index_first_table, column_index_sec_table, file_name1, file_name2, header1, header2):
    for i in left_joiner(column_index_first_table, column_index_sec_table, file_name1, file_name2, header2):
        yield i
    with open(file_name2, 'r', encoding="UTF-16") as file2:
        csvreader2 = csv.reader(file2)
        for i, row2 in enumerate(csvreader2):
            if i != 0:
                with open(file_name1, 'r', encoding="UTF-16") as file1:
                    csvreader1 = csv.reader(file1)
                    was = False
                    for row1 in csvreader1:
                        if row1[column_index_first_table]==row2[column_index_sec_table] and row2[column_index_sec_table] != 'NULL':
                            was = True
                    if not was:
                        yield ['NULL'] * len(header1) + row2


def script_reader(file_path1, file_path2, column_name, join_type):
    """Tool to generate the iterable"""
    header1, header2 = read_headers(file_path1, file_path2)
    result = check_column_numbers(header1, header2, column_name)
    if join_type=='full' or join_type=='FULL':
        return full_joiner(result[0], result[1], file_path1, file_path2, header1, header2)
    if join_type=='left' or join_type=='LEFT':
        return left_joiner(result[0], result[1], file_path1, file_path2, header2)
    if join_type=='right' or join_type=='RIGHT':
        return right_joiner(result[0], result[1], file_path1, file_path2, header1)
    if join_type=='inner' or join_type=='INNER':
        return inner_joiner(result[0], result[1], file_path1, file_path2)
    else:
        raise NameError("Unknown join type")