import os

def compare(a, b):
    """
    compare between to variable according to them type
    :param a: to compare with b
    :param b: to compare with a
    :return: 1 if a>b 0 if a==b and -1 if a<b
    """
    if a == b:
        return 0
    else:
        if a.isdigit() and b.isdigit():
            return 1 if float(a) - float(b) > 0 else -1
        else:
            try:
                return 1 if float(a) - float(b) > 0 else -1
            except:
                return 1 if a > b else -1


def value_as_number(value):
    """

    :param value: parameter to value in hash function
    :return: value as number if is number or the unicode of the first letter
    """
    try:
        return float(value)
    except:
        return ord(value[0])


class Heap:
    def __init__(self, file_name):
        """
        :param file_name: the name of the heap file to create. example: kiva_heap.txt
        """
        self.file_name = file_name
        f = open(file_name, 'w')
        f.close()

    def create(self, source_file):
        """
        The function create heap file from source file.
        :param source_file: the name of file to create from. example: kiva.txt
        """
        with open(source_file, 'r+') as source, open(self.file_name, 'w') as destination:
            for line in source:
                destination.write(line)

    def insert(self, line):
        """
        The function insert new line to heap file
        :param line: string reprsent new row, separated by comma. example: '653207,1500.0,USD,Agriculture'
        """
        with open(self.file_name, 'a+') as destination:
            destination.write(line + '\n')

    def delete(self, col_name, value):
        """
        The function delete records from the heap file where their value in col_name is value.
        Deletion done by mark # in the head of line.
        :param col_name: the name of the column. example: 'currency'
        :param value: example: 'PKR'
        """
        with open(self.file_name, 'r') as destination:
            title = destination.readline().strip().split(',')
            title_dict = {title[i]: i for i in range(title.__len__())}
        col_value = title_dict[col_name]

        tmp_name = 'tmp.txt'
        with open(self.file_name, 'r+') as origin, open(tmp_name, 'w') as tmp_file:
            for line in origin:
                splitted = line.strip().split(',')
                if str(value) == splitted[col_value] and not line.startswith('#'):
                    line = '#' + line[1:]
                tmp_file.write(line)

        self.create(tmp_name)
        os.remove(tmp_name)

    def update(self, col_name, old_value, new_value):
        """
        The function update records from the heap file where their value in col_name is old_value to new_value.
        :param col_name: the name of the column. example: 'currency'
        :param old_value: example: 'TZS'
        :param new_value: example: 'NIS'
        """
        with open(self.file_name, 'r') as destination:
            title = destination.readline().strip().split(',')
            title_dict = {title[i]: i for i in range(title.__len__())}

        tmp_name = 'tmp.txt'
        with open(self.file_name, 'r+') as origin, open(tmp_name, 'w') as tmp_file:
            for line in origin:
                splitted = line.strip().split(',')
                if str(old_value) == splitted[title_dict[col_name]] and not line.startswith('#'):
                    splitted[title_dict[col_name]] = new_value
                    line = ','.join(splitted) + '\n'
                tmp_file.write(line)

        self.create(tmp_name)
        os.remove(tmp_name)


class SortedFile:

    def __init__(self, file_name, col_name):
        """
        :param file_name: the name of the sorted file to create. example: kiva_sorted.txt
        :param col_name: the name of the column to sort by. example: 'lid'
        """
        self.file_name = file_name
        self.col_name = col_name
        self.col_value = None
        f = open(file_name, 'w')
        f.close()

    def create(self, source_file):
        """
        The function create sorted file from source file.
        :param source_file: the name of file to create from. example: kiva.txt
        """
        with open(source_file, 'r') as destination:
            title = destination.readline().strip().split(',')
            title_dict = {title[i]: i for i in range(title.__len__())}
        self.col_value = title_dict[self.col_name]

        min_id = None
        with open(source_file, 'r') as destination:
            destination.seek(destination.readline().__len__() + 1)
            min_id = destination.readline().strip().split(',')[self.col_value]
            max_id = min_id
            for line in destination:
                line_id = line.split(',')[self.col_value]
                min_id = min(min_id, line_id)
                max_id = max(max_id, line_id)

        current_id = min_id

        with open(source_file, 'r+') as source, open(self.file_name, 'w+') as destination:
            destination.write(','.join(title) + '\n')
            while True:
                source.seek(0)
                source.seek(source.readline().__len__() + 1)
                next_min_id = max_id
                for line in source:
                    line_id = line.strip().split(',')[title_dict[self.col_name]]
                    if line_id == str(current_id):
                        destination.write(line)
                    else:
                        if current_id < line_id < next_min_id:
                            next_min_id = line_id

                if current_id == max_id:
                    break
                current_id = next_min_id


    def insert(self, line):
        """
        The function insert new line to sorted file according to the value of col_name.
        :param line: string of row separated by comma. example: '653207,1500.0,USD,Agriculture'
        """

        tmp_name = 'tmp.txt'
        flag = True
        with open(self.file_name, 'r+') as source, open(tmp_name, 'w+') as destination:
            title = source.readline()
            destination.write(title)
            for _line in source:
                if flag:
                    if compare(_line.strip().split(',')[self.col_value],
                               line.strip().split(',')[self.col_value]) != 1:
                        destination.write(_line)
                    else:
                        destination.write(line + "\n")
                        destination.write(_line)
                        flag = False
                else:
                    destination.write(_line)
        with open(tmp_name, 'r+') as source, open(self.file_name, 'w') as destination:
            for line in source:
                destination.write(line)
        os.remove(tmp_name)

    def delete(self, value):
        """
        The function delete records from sorted file where their value in col_name is value.
        Deletion done by mark # in the head of line.
        :param value: example: 'PKR'
        """
        begin, end = self.binary_search(value)
        if begin == 0 and end == 0:
            return
        tmp_name = 'tmp.txt'
        with open(self.file_name, 'r+') as origin, open(tmp_name, 'w') as destination:
            origin.seek(0, 2)
            EOF = origin.tell()
            origin.seek(0)
            while origin.tell() < begin and origin.tell() < EOF:
                destination.write(origin.readline())
            origin.seek(end)
            while origin.tell() < EOF:
                destination.write(origin.readline())
        with open(self.file_name, 'w+') as origin, open(tmp_name, 'r') as destination:
            for _line in destination:
                origin.write(_line)
        os.remove(tmp_name)

    def update(self, old_value, new_value):
        """
        The function update records from the sorted file where their value in col_name is old_value to new_value.
        :param old_value: example: 'TZS'
        :param new_value: example: 'NIS'
        """
        if old_value == new_value:
            return

        tmp_name = 'tmp.txt'
        with open(self.file_name, 'r+') as origin, open(tmp_name, 'w') as destination:
            origin.seek(0, 2)
            EOF = origin.tell()
            origin.seek(0)
            begin, end = self.binary_search(old_value)
            if begin == 0 and end == 0:
                return
            flag = False
            destination.write(origin.readline())
            line_size = origin.readline().__len__()
            origin.seek(-line_size -1, 1)
            line = origin.readline()
            if compare(old_value, new_value) == 1:
                while origin.tell() < EOF and compare(origin.readline().strip().split(',')[self.col_value],
                                                      new_value) != 1:
                    origin.seek(-line_size-1, 1)
                    destination.write(origin.readline())
                place = origin.tell()
                origin.seek(begin)
                while origin.tell() <= end:
                    line = origin.readline()
                    splitted = line.strip().split(',')
                    splitted[self.col_value] = new_value
                    destination.write(','.join(splitted) + '\n')
                origin.seek(place)
                while origin.tell() < begin:
                    destination.write(origin.readline())
                origin.seek(end)
                while origin.tell() < EOF:
                    destination.write(origin.readline())

            if compare(old_value, new_value) == -1:
                while origin.tell() < EOF and origin.tell() < begin:
                    destination.write(origin.readline())
                origin.seek(end)
                while origin.tell() < EOF and compare(origin.readline().strip().split(',')[self.col_value],
                                                      new_value) != 1:
                    origin.seek(-line_size-1, 1)
                    destination.write(origin.readline())
                place = origin.tell()
                origin.seek(begin)
                while origin.tell() <= end:
                    line = origin.readline()
                    splitted = line.strip().split(',')
                    splitted[self.col_value] = new_value
                    destination.write(','.join(splitted) + '\n')
                origin.seek(place)
                while origin.tell() < EOF:
                    destination.write(origin.readline())

        with open(self.file_name, 'w+') as origin, open(tmp_name, 'r') as destination:
            for _line in destination:
                origin.write(_line)
        os.remove(tmp_name)

    # if value not exist
    def binary_search(self, value):
        '''

        :param value: the value we want to search
        :return: the start and the end of the block that contain the value in the sorted file
        '''
        with open(self.file_name, 'r+') as origin:
            origin.seek(0)
            title_len = origin.readline().__len__() + 1
            origin.seek(title_len)
            SOF = origin.tell()
            line_size = origin.readline().__len__() + 1
            origin.seek(0, 2)
            EOF = origin.tell()
            num_of_lines = (origin.tell() - title_len) / line_size
            origin.seek(0)
            origin.readline()
            isFound = False
            num_of_lines = num_of_lines / 2
            preLine = num_of_lines
            while not isFound and SOF <= origin.tell() < EOF and preLine>0:
                origin.seek(num_of_lines * (line_size) + title_len)
                line = origin.readline()
                if line.strip().split(',')[self.col_value] == value:
                    isFound = True
                    break
                elif compare(line.strip().split(',')[self.col_value], value) == -1:
                    num_of_lines = num_of_lines + preLine / 2
                    preLine = preLine/2
                else:
                    num_of_lines = num_of_lines - preLine / 2
                    preLine = preLine/2
            if not isFound:
                return 0,0
            place = origin.tell()
            begin = place
            origin.readline()
            while origin.tell() > SOF:
                origin.seek(origin.tell() - 2 * line_size)
                line = origin.readline()
                if line.strip().split(',')[self.col_value] != value:
                    begin = origin.tell()
                    break
            origin.seek(place)
            while origin.tell() < EOF:
                line = origin.readline()
                if line.strip().split(',')[self.col_value] != value:
                    end = origin.tell() - line_size
                    break
                if origin.tell()==EOF:
                    end = origin.tell()

            return begin, end



class Hash:
    def __init__(self, file_name, N=5):
        """
        :param file_name: the name of the hash file to create. example: kiva_hash.txt
        :param N: number of buckets/slots.
        """
        self.file_name = file_name
        self.N = N
        f = open(file_name, 'w')
        f.close()

    def create(self, source_file, col_name):
        """
        :param source_file: name of file to create from. example: kiva.txt
        :param col_name: the name of the column to index by example: 'lid'
        Every row will represent a bucket, every tuple <value|ptr> will separates by comma.
        Example for the first 20 instances in 'kiva.txt' and N=10:
        653060|11,
        653091|17,653051|1,
        653052|18,653062|14,653082|9,
        653063|4,653053|2,
        653054|16,653084|5,
        653075|15,
        653066|19,
        653067|7,
        653088|12,653048|10,653078|8,1080148|6,653068|3,
        653089|13,
        """
        with open(source_file, 'r') as destination:
            title = destination.readline().strip().split(',')
            title_dict = {title[i]: i for i in range(title.__len__())}
        col_value = title_dict[col_name]

        with open(source_file, 'r+') as source, open(self.file_name, 'w+') as destination:
            for i in range(self.N):
                source.seek(0)
                source.seek(source.readline().__len__() + 1)
                current_line = '\n'
                for count, line in enumerate(source):
                    ID_string = str(line.strip().split(',')[col_value])
                    ID = value_as_number(ID_string)
                    if ID % self.N == i:
                        current_line = (ID_string + '|' + str(count + 1) + ',') + current_line
                destination.write(current_line)

    def add(self, value, ptr):
        """
        The function insert <value|ptr> to hash table according to the result of the hash function on value.
        :param value: the value of col_name of the new instance.
        :param ptr: the row number of the new instance in the heap file.
        """
        tmp_name = 'tmp.txt'
        with open(self.file_name, 'r+') as source, open(tmp_name, 'w+') as destination:
            for counter, line in enumerate(source):
                ID = value_as_number(value)
                if ID % self.N == counter:
                    destination.write(str(value) + '|' + str(ptr) + ',' + line)
                else:
                    destination.write(line)
        with open(self.file_name, 'w') as source, open(tmp_name, 'r+') as destination:
            for line in destination:
                source.write(line)
        os.remove(tmp_name)
    def remove(self, value, ptr):
        """
        The function delete <value|ptr> from hash table.
        :param value: the value of col_name.
        :param ptr: the row number of the instance in the heap file.
        """
        tmp_name = 'tmp.txt'
        with open(self.file_name, 'r+') as source, open(tmp_name, 'w+') as destination:
            for counter, line in enumerate(source):
                ivalue = value_as_number(value)
                if ivalue % self.N == counter:
                    splitted = line.strip().split(',')
                    try:
                        splitted.remove(value + '|' + ptr)
                    except:
                        pass
                    destination.write(','.join(splitted) + '\n')
                else:
                    destination.write(line)
        with open(self.file_name, 'w') as source, open(tmp_name, 'r+') as destination:
            for line in destination:
                source.write(line)
        os.remove(tmp_name)



# timing:

def writeToCSV(name, time_for_create, time_for_insert, time_for_update, time_for_delete):
    import csv
    try:
        my_file = open('times_for_' + name + '.csv', 'wb')
        cwriter = csv.writer(my_file, delimiter=',')
        cwriter.writerow(['index', 'create time', 'insert time', 'update time', 'delete time'])
        for j in range(50):
            cwriter.writerow([str(j), str(time_for_create[j]), str(time_for_insert[j]), str(time_for_update[j]), str(time_for_delete[j])])
        my_file.close()
    except IOError:
        print('Error printing to file, ' + name)


def writeHashToCSV(name, time_for_create_lid, time_for_insert_lid, time_for_delete_lid, time_for_create_loan_amount, time_for_insert_loan_amount, time_for_delete_loan_amount, time_for_create_sector, time_for_insert_sector, time_for_delete_sector):
    import csv
    try:
        my_file = open('times_for_' + name + '.csv', 'wb')
        cwriter = csv.writer(my_file, delimiter=',')
        cwriter.writerow(['hashing by lid', '', '', '', '', 'hashing by loan_amount', '', '', '', '', 'hashing by sector', '', '', ''])
        cwriter.writerow(['index', 'create time', 'insert time', 'delete time', '', 'index', 'create time', 'insert time', 'delete time', '', 'index', 'create time', 'insert time', 'delete time'])
        for j in range(50):
            cwriter.writerow([str(j), str(time_for_create_lid[j]), str(time_for_insert_lid[j]), str(time_for_delete_lid[j]), '', str(j), str(time_for_create_loan_amount[j]), str(time_for_insert_loan_amount[j]), str(time_for_delete_loan_amount[j]), '', str(j), str(time_for_create_sector[j]), str(time_for_insert_sector[j]), str(time_for_delete_sector[j])])
        my_file.close()
    except IOError:
        print('Error printing to file, ' + name)

import timeit

file_name = 'fixed_kiva_loans_1000_first_rows.txt'
file_50_rows = 'fixed_kiva_loans_extra_50_rows.txt'
line_insert = ''


print 'analizing hash 10'
print 'hashing by lid'
# times for hash 10 lid
hash_10_time_for_create_lid = []
hash_10_time_for_insert_lid = []
hash_10_time_for_delete_lid = []

hash_10 = Hash('hash_10.txt', 10)
for i in range(50):
    hash_10_time_for_create_lid.append(timeit.timeit("hash_10.create('" + file_name + "', 'lid')", number=1, setup="from __main__ import hash_10, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[0]
        hash_10_time_for_insert_lid.append(timeit.timeit("hash_10.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_10, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[0]
        hash_10_time_for_delete_lid.append(timeit.timeit("hash_10.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_10, file_name"))
    test.close()
except IOError:
    print 'error deleting'

print 'hashing by loan amount'
# times for hash 10 loan amount
hash_10_time_for_create_loan_amount = []
hash_10_time_for_insert_loan_amount = []
hash_10_time_for_delete_loan_amount = []

hash_10 = Hash('hash_10.txt', 10)
for i in range(50):
    hash_10_time_for_create_loan_amount.append(timeit.timeit("hash_10.create('" + file_name + "', 'loan_amount')", number=1, setup="from __main__ import hash_10, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[1]
        hash_10_time_for_insert_loan_amount.append(timeit.timeit("hash_10.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_10, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[1]
        hash_10_time_for_delete_loan_amount.append(timeit.timeit("hash_10.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_10, file_name"))
    test.close()
except IOError:
    print 'error deleting'


print 'hashing by sector'
# times for hash 10 sector
hash_10_time_for_create_sector = []
hash_10_time_for_insert_sector = []
hash_10_time_for_delete_sector = []

hash_10 = Hash('hash_10.txt', 10)
for i in range(50):
    hash_10_time_for_create_sector.append(timeit.timeit("hash_10.create('" + file_name + "', 'sector')", number=1, setup="from __main__ import hash_10, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[3]
        hash_10_time_for_insert_sector.append(timeit.timeit("hash_10.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_10, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[3]
        hash_10_time_for_delete_sector.append(timeit.timeit("hash_10.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_10, file_name"))
    test.close()
except IOError:
    print 'error deleting'

writeHashToCSV('hash_10', hash_10_time_for_create_lid, hash_10_time_for_insert_lid, hash_10_time_for_delete_lid, hash_10_time_for_create_loan_amount, hash_10_time_for_insert_loan_amount, hash_10_time_for_delete_loan_amount, hash_10_time_for_create_sector, hash_10_time_for_insert_sector, hash_10_time_for_delete_sector)

print 'analizing hash 100'
print 'hashing by lid'
# times for hash 100 lid
hash_100_time_for_create_lid = []
hash_100_time_for_insert_lid = []
hash_100_time_for_delete_lid = []

hash_100 = Hash('hash_100.txt', 100)
for i in range(50):
    hash_100_time_for_create_lid.append(timeit.timeit("hash_100.create('" + file_name + "', 'lid')", number=1, setup="from __main__ import hash_100, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[0]
        hash_100_time_for_insert_lid.append(timeit.timeit("hash_100.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_100, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[0]
        hash_100_time_for_delete_lid.append(timeit.timeit("hash_100.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_100, file_name"))
    test.close()
except IOError:
    print 'error deleting'

print 'hashing by loan amount'
# times for hash 100 loan amount
hash_100_time_for_create_loan_amount = []
hash_100_time_for_insert_loan_amount = []
hash_100_time_for_delete_loan_amount = []

hash_100 = Hash('hash_100.txt', 100)
for i in range(50):
    hash_100_time_for_create_loan_amount.append(timeit.timeit("hash_100.create('" + file_name + "', 'loan_amount')", number=1, setup="from __main__ import hash_100, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[1]
        hash_100_time_for_insert_loan_amount.append(timeit.timeit("hash_100.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_100, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[1]
        hash_100_time_for_delete_loan_amount.append(timeit.timeit("hash_100.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_100, file_name"))
    test.close()
except IOError:
    print 'error deleting'


print 'hashing by sector'
# times for hash 100 sector
hash_100_time_for_create_sector = []
hash_100_time_for_insert_sector = []
hash_100_time_for_delete_sector = []

hash_100 = Hash('hash_100.txt', 100)
for i in range(50):
    hash_100_time_for_create_sector.append(timeit.timeit("hash_100.create('" + file_name + "', 'sector')", number=1, setup="from __main__ import hash_100, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[3]
        hash_100_time_for_insert_sector.append(timeit.timeit("hash_100.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_100, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[3]
        hash_100_time_for_delete_sector.append(timeit.timeit("hash_100.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_100, file_name"))
    test.close()
except IOError:
    print 'error deleting'

writeHashToCSV('hash_100', hash_100_time_for_create_lid, hash_100_time_for_insert_lid, hash_100_time_for_delete_lid, hash_100_time_for_create_loan_amount, hash_100_time_for_insert_loan_amount, hash_100_time_for_delete_loan_amount, hash_100_time_for_create_sector, hash_100_time_for_insert_sector, hash_100_time_for_delete_sector)

print 'analizing hash 1000'
print 'hashing by lid'
# times for hash 1000 lid
hash_1000_time_for_create_lid = []
hash_1000_time_for_insert_lid = []
hash_1000_time_for_delete_lid = []

hash_1000 = Hash('hash_1000.txt', 1000)
for i in range(50):
    hash_1000_time_for_create_lid.append(timeit.timeit("hash_1000.create('" + file_name + "', 'lid')", number=1, setup="from __main__ import hash_1000, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[0]
        hash_1000_time_for_insert_lid.append(timeit.timeit("hash_1000.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_1000, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[0]
        hash_1000_time_for_delete_lid.append(timeit.timeit("hash_1000.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_1000, file_name"))
    test.close()
except IOError:
    print 'error deleting'

print 'hashing by loan amount'
# times for hash 1000 loan amount
hash_1000_time_for_create_loan_amount = []
hash_1000_time_for_insert_loan_amount = []
hash_1000_time_for_delete_loan_amount = []

hash_1000 = Hash('hash_1000.txt', 1000)
for i in range(50):
    hash_1000_time_for_create_loan_amount.append(timeit.timeit("hash_1000.create('" + file_name + "', 'loan_amount')", number=1, setup="from __main__ import hash_1000, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[1]
        hash_1000_time_for_insert_loan_amount.append(timeit.timeit("hash_1000.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_1000, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[1]
        hash_1000_time_for_delete_loan_amount.append(timeit.timeit("hash_1000.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_1000, file_name"))
    test.close()
except IOError:
    print 'error deleting'


print 'hashing by sector'
# times for hash 1000 sector
hash_1000_time_for_create_sector = []
hash_1000_time_for_insert_sector = []
hash_1000_time_for_delete_sector = []

hash_1000 = Hash('hash_1000.txt', 1000)
for i in range(50):
    hash_1000_time_for_create_sector.append(timeit.timeit("hash_1000.create('" + file_name + "', 'sector')", number=1, setup="from __main__ import hash_1000, file_name"))


try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        insert_val = line_insert.strip().split(',')[3]
        hash_1000_time_for_insert_sector.append(timeit.timeit("hash_1000.add('" + str(insert_val) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_1000, file_name"))
    test.close()
except IOError:
    print 'error inserting'

try:
    test = open(file_50_rows, 'r')
    for num, row in enumerate(test, 1):
        line_insert = row[:-1]
        delete_key = line_insert.strip().split(",")[3]
        hash_1000_time_for_delete_sector.append(timeit.timeit("hash_1000.remove('" + str(delete_key) + "', '" + str(num + 1000) + "')", number=1, setup="from __main__ import hash_1000, file_name"))
    test.close()
except IOError:
    print 'error deleting'

writeHashToCSV('hash_1000', hash_1000_time_for_create_lid, hash_1000_time_for_insert_lid, hash_1000_time_for_delete_lid, hash_1000_time_for_create_loan_amount, hash_1000_time_for_insert_loan_amount, hash_1000_time_for_delete_loan_amount, hash_1000_time_for_create_sector, hash_1000_time_for_insert_sector, hash_1000_time_for_delete_sector)

print 'done'
