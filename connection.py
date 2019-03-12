import csv


def append_item_to_csv(filepath, header, value):
    with open (filepath, "a+") as data_file:
        csv_writer = csv.DictWriter(data_file, fieldnames=header)
        csv_writer.writerow({header : value.get(header) for header in header })


def read_csv(filepath, header):
    with open(filepath, "r") as data_file:
        csv_reader = csv.DictReader(data_file, fieldnames=header)
        next(csv_reader)
        data = {}
        for row in csv_reader:
            data[row['id']]=[row[headers] for headers in header]

        return data


print(read_csv('sample_data/answer.csv', ['id', 'submission_time', 'vote_number', 'question_id', 'message']))


