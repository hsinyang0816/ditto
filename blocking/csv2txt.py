import csv
import argparse

def csv2txt(csv_file, txt_file):
    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        list_of_column_names = []
        for row in csv_reader:
            list_of_column_names.append(row)
            break
        with open(txt_file, 'w') as output_file:
            for row in csv_reader:
                for idx, value in enumerate(row):
                    if idx > 0:
                        output_file.write(f"COL {list_of_column_names[0][idx]} VAL {value} ")
                output_file.write(f"\n")
        output_file.close()
    csv_file.close()
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str)
    parser.add_argument("--txt", type=str)

    hp = parser.parse_args()
    csv2txt(hp.csv, hp.txt)