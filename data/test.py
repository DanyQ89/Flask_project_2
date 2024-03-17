import csv

with open('file.csv', encoding='utf8') as file:
    data = csv.reader(file, delimiter='РАЗДЕЛИТЕЛЬ ПОЛЕЙ')
    data = [list(map([round(float(g)) for g in i], i)) for i in data]

with open('file_1.csv', 'w', encoding='utf8') as file_out:
    for i in data:
        file_out.write(i)