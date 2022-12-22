import csv
import operator


class FileManager:
    @staticmethod
    def read_from_csv_file(path):
        file = open(path)
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()
        return rows

    @staticmethod
    def write_new_row_in_csv_file(path, row: list[str]):
        filename = path
        content_rows = FileManager.read_from_csv_file(path)
        with open(filename, 'w', newline="") as file:
            csvwriter = csv.writer(file)  # 1. create a csvwriter object
            content_rows.append(row)
            csvwriter.writerows(content_rows)  # 2. write the list

    @staticmethod
    def override_csv_file(path, rows: list[list[str]]):
        filename = path
        with open(filename, 'w', newline="") as file:
            csvwriter = csv.writer(file)  # 1. create a csvwriter object
            csvwriter.writerows(rows)  # 2. write the list

    @staticmethod
    def sort_csv_file_by_column_values(path, column_index, delimiter=','):
        li = []

        # Open csv file
        with open(path, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=delimiter, skipinitialspace=True)

            # Create a list of all rows such that the marks column is an integer
            for item in reader:
                # Save marks value as an integer, leave other values as is
                l = [int(value) if idx == column_index else value for idx, value in enumerate(item)]
                li.append(l)
            FileManager.override_csv_file(path, sorted(li, key=operator.itemgetter(1), reverse=True))

