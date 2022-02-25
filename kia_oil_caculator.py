from subprocess import list2cmdline
import gspread
import pprint
from  datetime import datetime
MAX_ROW = 1000
pos2dis = {
    'Duke': 9.6*2,
    'liming': 8.5*2,
    'target': 8.4*2,
    'walmart': 3.5*2
}

p2miles = {
    'wl': 0.0,
    'guoguo': 0.0,
    'zq': 0.0,
    'fw': 0.0
}

if __name__ == '__main__':
    gc = gspread.service_account(filename='service_account.json')
    sh = gc.open("Ride").sheet1

    begin_date = input("Enter the begin time in this yyyy-MM-dd format: ")
    end_date = input("Enter the end time in this yyyy-MM-dd format: ")

    total_money = float(input("How Many money you want to amortize: "))
    list_of_lists = sh.get_all_values()

    try:
        base_date = datetime.strptime(begin_date, "%Y-%m-%d")
    except ValueError:
        print("This is not correct date string format, It should be YYYY-MM-DD")
    
    for i in range(2, len(list_of_lists)):
        cnt = 0
        if list_of_lists[i][6] >= begin_date and list_of_lists[i][6] < end_date:
            for j in range(2, 6):
                if list_of_lists[i][j] == "TRUE":
                    cnt = cnt + 1
            
            miles_avg = 0
            if list_of_lists[i][0] in pos2dis:
                miles_avg = pos2dis[list_of_lists[i][0]] / cnt
            else:
                miles_avg = float(list_of_lists[i][0]) / cnt
            
            p2miles['wl'] += miles_avg if list_of_lists[i][2]  == "TRUE" else 0
            p2miles['fw'] += miles_avg if list_of_lists[i][3]  == "TRUE" else 0
            p2miles['zq'] += miles_avg if list_of_lists[i][4]  == "TRUE" else 0
            p2miles['guoguo'] += miles_avg if list_of_lists[i][5]  == "TRUE" else 0


    headers = ['Name', 'Miles', 'Percentage', 'money']
    format_string = "{:<12}{:<24}{:<24}{:<24}"
    print(format_string.format(*headers))
    total_miles = sum(p2miles.values())
    for key, value in p2miles.items():
        item = [key, value, value/total_miles, total_money*(value/total_miles)]
        print(format_string.format(*item))

