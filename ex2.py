import os


# return the n'th occurency of needle in haystack
def indexof(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + 1)
        n -= 1
    return start


def randomFileName(size=5):
    while True:
        try:
            filen = os.urandom(size)
            with open(str(filen) + '.txt', 'w'):
                return filen
        except:
            pass


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

        tmp_name = 'tmp.txt'
        with open(self.file_name, 'r+') as origin, open(tmp_name, 'w') as tmp_file:
            for line in origin:
                splitted = line.strip().split(',')
                if str(value) == splitted[title_dict[col_name]] and not line.startswith('#'):
                    line[0] = '#'
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


'''
heap = Heap('heap.txt')
heap.create('kiva_loans.txt')
heap.insert('653207,1500.0,NIS,Agriculture')
heap.update('currency','PKR','NIS')
heap.delete('currency','NIS')
'''


class SortedFile:

    def __init__(self, file_name, col_name):
        """
        :param file_name: the name of the sorted file to create. example: kiva_sorted.txt
        :param col_name: the name of the column to sort by. example: 'lid'
        """
        self.file_name = file_name
        self.col_name = col_name
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

        min_id = None
        with open(source_file, 'r') as destination:
            destination.seek(destination.readline().__len__() + 1)
            min_id = destination.readline().strip().split(',')[title_dict[self.col_name]]
            max_id = min_id
            for line in destination:
                line_id = line.split(',')[title_dict[self.col_name]]
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
            # destination.seek(os.path.getsize(self.file_name) / 2)
            # print(destination.readline())

    def insert(self, line):
        """
        The function insert new line to sorted file according to the value of col_name.
        :param line: string of row separated by comma. example: '653207,1500.0,USD,Agriculture'
        """
        with open(self.file_name, 'r') as destination:
            title = destination.readline().strip().split(',')
            title_dict = {title[i]: i for i in range(title.__len__())}
        tmp_name = 'tmp.txt'
        with open(self.file_name, 'r+') as source, open(tmp_name, 'w+') as destination:
            for _line in source:
                if _line.split(',')[title_dict[self.col_name]] <= line.split(',')[title_dict[self.col_name]]:
                    destination.write(_line)
                else:
                    destination.write(line)
        os.remove(tmp_name)

    def delete(self, value):
        """
        The function delete records from sorted file where their value in col_name is value.
        Deletion done by mark # in the head of line.
        :param value: example: 'PKR'
        """

    def update(self, old_value, new_value):
        """
        The function update records from the sorted file where their value in col_name is old_value to new_value.
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
                if str(old_value) == splitted[title_dict[self.col_name]] and not line.startswith('#'):
                    splitted[title_dict[self.col_name]] = new_value
                    line = ','.join(splitted) + '\n'
                tmp_file.write(line)

        self.create(tmp_name)
        os.remove(tmp_name)


# sf = SortedFile('SortedFile.txt', 'loan_amount')
# sf.create('kiva_loans.txt')
# sf.insert('653207,2.0,USD,Agriculture')
# sf.delete('625.0')
# sf.update('150.0', '12')


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

        with open(source_file, 'r+') as source, open(self.file_name, 'w+') as destination:
            for i in range(self.N):
                source.seek(0)
                source.seek(source.readline().__len__()+1)
                for count, line in enumerate(source):
                    if count>18:
                        break
                    ID_string = str(line.strip().split(',')[title_dict[col_name]])
                    print count
                    ID = int(ID_string) if ID_string.isdigit() else ord(ID_string[0])
                    if ID % self.N == i:
                        destination.write(ID_string + '|'+str(count+1)+ ',')
                destination.write('\n')



    def add(self, value, ptr):
        """
        The function insert <value|ptr> to hash table according to the result of the hash function on value.
        :param value: the value of col_name of the new instance.
        :param ptr: the row number of the new instance in the heap file.
        """


    def remove(self, value, ptr):
        """
        The function delete <value|ptr> from hash table.
        :param value: the value of col_name.
        :param ptr: the row number of the instance in the heap file.
        """


# heap = Heap("heap_for_hash.txt")
hash = Hash('hash_file.txt', 10)

# heap.create('kiva.txt')
hash.create('kiva_loans.txt', 'lid')

# heap.insert('653207,1500.0,USD,Agriculture')
# hash.add('653207','11')


def binarySearch(file_name, )
'''
key = '19999999999999999999999999999999999'
fp = open('stam.txt')
fp.seek(0)
begin = fp.readline().__len__()
fp.seek(0, 2)
end = fp.tell()

while (begin < end):
    fp.seek(begin + ((end - begin) / 2), 0)
    flag = False
    x = fp.read(1)
    while (x != '\n') and not flag:
        try:
            fp.seek(fp.tell() - 2, 0)
        except IOError:
            flag = True
        x = fp.read(1)
        if flag:
            fp.seek(0)
    if flag:
        s = fp.readline()
    place = fp.tell()
    line_key = fp.readline()

    first = float(key) if key.isdigit() else key
    second = float(line_key.strip()) if line_key.strip().isdigit() else line_key.strip()

    if (key == line_key.strip()):
        print 'falafel'
        break
    elif first > second:
        begin = place + 1
    else:
        end = place - 1
'''