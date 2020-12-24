import glob
from dataclasses import dataclass, fields
import json
import hashlib


@dataclass
class ThirdTableEntity:
    access_id: str
    strange_number: str
    attr_type: str
    attr: str


@dataclass
class ForthTableEntity:
    content_id: str
    access_id: str


@dataclass
class FifthTableEntity:
    content_id: str
    code: str
    name: str
    type: int
    start_date_time: str
    end_date_time: str
    creator: str
    create_date_time: str
    modifier: str
    modify_date_time: str


@dataclass
class SixthTableEntity:
    content_id: str
    strange_number: str
    attr_type: str
    attr: str


@dataclass
class SeventhTableEntity:
    category_id: str
    code: str
    content_id: str
    seq_num: str
    date: str


@dataclass
class EighthTableEntity:
    category_id: str
    name: str


def calc_hash(data: str):
    return hashlib.md5(data.encode()).hexdigest()[:10]


class TableGenerator:
    def __init__(self, data_file_mask='data/*.txt'):
        self.data_files = glob.glob(data_file_mask)
        self.data_files.sort()

    def parse_third_table(self):
        with open(self.data_files[2]) as file:
            data = file.read()
            return [ThirdTableEntity(*[x.strip() for x in ('100001000000000' + x).split('|')[0:4]]) for x in
                    data.split('100001000000000') if x.count('|') == 3]

    def parse_forth_table(self):
        with open(self.data_files[3]) as file:
            return [ForthTableEntity(*x.split('|')[0].split('-')[0:2]) for x in file.readlines() if '-' in x if x]

    def parse_fifth_table(self):
        with open(self.data_files[4]) as file:
            data = file.read().replace('\n', '')
            return [FifthTableEntity(*[x.strip() for x in x.split('|')[0:10]]) for x in data.split(' ' * 80) if
                    x.count('|') == 9]

    def parse_sixth_table(self):
        with open(self.data_files[5]) as file:
            data = file.read()
            return [SixthTableEntity(*[x.strip() for x in ('100001000000000' + x).split('|')[0:4]]) for x in
                    data.split('100001000000000') if x.count('|') == 3]

    def parse_seventh_table(self):
        with open(self.data_files[6]) as file:
            return [SeventhTableEntity(*x.split('|')) for x in file.readlines()]

    def parse_eighth_table(self):
        with open(self.data_files[7]) as file:
            return [EighthTableEntity(*((lambda t: [t[0], t[3]])(x.split('|')))) for x in file.readlines()]


HASHES = {}
AUTHOR_KEY_HASH = calc_hash('author')

if __name__ == '__main__':
    print('Started...')

    generator = TableGenerator()
    third_table = generator.parse_third_table()

    forth_table = generator.parse_forth_table()
    fifth_table = generator.parse_fifth_table()
    sixth_table = generator.parse_sixth_table()

    print('Parsing finished...')

    forth_table_cached = {a.access_id: a.content_id for a in forth_table}
    fifth_table_cached = {a.content_id: a for a in fifth_table}

    data_cache = {}

    sizes_cache = {}

    for sixth_item in sixth_table:
        if sixth_item.attr_type not in data_cache:
            data_cache[sixth_item.attr_type] = {sixth_item.content_id: sixth_item.attr}
            HASHES[sixth_item.attr_type] = calc_hash(sixth_item.attr_type)
        else:
            data_cache[sixth_item.attr_type][sixth_item.content_id] = sixth_item.attr

    for fifth_item in fifth_table:
        for attr_type in fields(fifth_item):
            attr_name = attr_type.name
            if (attr_name != "content_id") and (attr_name not in data_cache):
                data_cache[attr_name] = {fifth_item.content_id: getattr(fifth_item, attr_name)}
                HASHES[attr_name] = calc_hash(attr_name)
            elif attr_name != "content_id":
                data_cache[attr_name][fifth_item.content_id] = getattr(fifth_item, attr_name)

    for third_item in third_table:
        if third_item.attr_type == 'FILE_SIZE':
            sizes_cache[third_item.access_id] = third_item.attr
        else:
            if third_item.attr_type not in data_cache:
                if third_item.access_id in forth_table_cached:
                    data_cache[third_item.attr_type] = {forth_table_cached[third_item.access_id]: third_item.attr}
                else:
                    data_cache[third_item.attr_type] = {third_item.access_id: third_item.attr}
                HASHES[third_item.attr_type] = calc_hash(third_item.attr_type)
            else:
                if third_item.access_id in forth_table_cached:
                    data_cache[third_item.attr_type][forth_table_cached[third_item.access_id]] = third_item.attr
                else:
                    data_cache[third_item.attr_type][third_item.access_id] = third_item.attr

    print('Caching finished...')

    result = "{"

    for i, table_item in enumerate(forth_table):

        if table_item.content_id not in fifth_table_cached:
            # print(f'Unknown id: {table.content_id}')
            continue

        fifth_table_item = fifth_table_cached[table_item.content_id]
        params_dict = {
            AUTHOR_KEY_HASH: calc_hash(fifth_table_item.creator)
        }
        for cache_type in data_cache:
            if table_item.content_id in data_cache[cache_type]:
                params_dict[HASHES[cache_type]] = calc_hash(data_cache[cache_type][table_item.content_id])


        if table_item.access_id in sizes_cache:
            params_dict['size'] = str(int(sizes_cache[table_item.access_id]) // 1000)
        else:
            continue
            # print(f'Unable to find size for {table_item.content_id}')
        result += f'"{calc_hash(fifth_table_item.name)}": {json.dumps(params_dict)}'

        if i != len(forth_table) - 1:
            result += ',\n'

    result += '}'
    with open('table.json', 'w') as table_file:
        table_file.write(result)
