import sys
import json

from mock import Mock


def custom_command_line():
    args = sys.argv[1:]
    try:
        if args[0] == 'ticket_gen':
            if args[1] == '-n':
                activities_num = int(args[2])
                if args[3] == '-o':
                    file_name = args[4]
                    return activities_num, file_name
    except:
        print("Wrong command line format.\nThe right format should be \'ticket_gen -n (numbers) -o (JSON file name)\' ")


if __name__ == '__main__':
    activities_num, filename = custom_command_line()

    data = Mock(activities_num)
    data_dic = data.combine_data()

    with open(filename, 'w') as outfile:
        json_object = json.dump(data_dic, outfile)
