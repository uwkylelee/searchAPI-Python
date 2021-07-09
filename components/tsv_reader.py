import csv
from components.print_log import print_log


def tsv_reader(tsv_file: str):
    print_log('Converting tsv file into dictionary format...')

    data: dict = {}
    f = open(tsv_file, 'r', encoding='utf-8')
    reader = csv.reader(f, delimiter='\t')

    for line in reader:
        if reader.line_num == 1:
            continue
        data[int(line[0])] = line[1]

    f.close()

    print_log('Successfully converted tsv file into dictionary!\n')
    return data
