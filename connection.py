import csv


def append_item_to_csv(filepath, header, value):
    with open (filepath, "a+") as data_file:
        csv_writer = csv.DictWriter(data_file, fieldnames=header)
        csv_writer.writerow({header : value.get(header) for header in header })


def read_csv(filepath, header):
    with open(filepath, "r") as data_file:
        csv_reader = csv.DictReader(data_file, fieldnames=header)
        for row in csv_reader:
            print(row)

        #readed = {row[0][0][1]: row.get() for row in csv_reader}
        # :
        #     stories[row['id']] = [
        #         row['id'], row['title'], row['user_story'], row['acceptance_criteria'], row['business_value'],
        #         row['estimation'], row['status']
        print(readed)


read_csv('sample_data/answer.csv', ['id', 'submission_time', 'vote_number', 'question_id', 'message'])


