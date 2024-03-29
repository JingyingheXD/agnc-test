import sys
import json

from mock import Mock
from create_db import create_db
from query_ticket_lifecycle import query_ticket_lifecycle


def custom_command_line():
    args = sys.argv[1:]
    try:
        if args[0] == 'ticket_gen':
            if args[1] == '-n':
                tickets_num = int(args[2])
                if args[3] == '-o':
                    file_name = args[4]
                    return tickets_num, file_name
    except:
        print("Wrong command line format.\nThe right format should be \'ticket_gen -n (numbers) -o (JSON file name)\' ")


def export_JSON():
    tickets_num, filename = custom_command_line()
    data = Mock(tickets_num)
    data_dic = data.generate_data()

    with open(filename, 'w') as outfile:
        json_object = json.dump(data_dic, outfile)


if __name__ == '__main__':
    export_JSON()
    create_db()
    query_ticket_lifecycle()
