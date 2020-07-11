# python 3.7
import csv
import urllib3
import socket
import sched
import sys
import time
import pickle
from pathos.multiprocessing import ProcessingPool
from multiprocessing import Process, freeze_support

# Declaring Global Variables
port: int = 8484
http = urllib3.PoolManager()


def read_csv(csv_file="url_list.csv"):
    """
    :param csv_file: csv file name
    :return:list   of key value pair of data
    """

    with open(csv_file, newline='') as csvfile:
        url_data = csv.reader(csvfile, delimiter=',', quotechar='|')
        # Skipping the first line means header
        next(url_data)

        def map_pool(line):
            temp = {}
            url_name, url_val = line[0], line[1].strip()  # Removing space from url
            temp[url_name] = url_val
            return temp

        url_list = list(map(map_pool, url_data))

    return url_list


def url_status_checker(url_list):
    """
   :param url_list: dict of url name and url address
   :return:  it will return url  and url status as list
   """

    def map_pool_status(url_item):
        url_status_dict = {}
        url_name = next(iter(url_item))
        url_value = url_item[url_name]
        response = http.request('GET', url_value)
        url_status_dict[url_name] = response.status
        return url_status_dict

    return list(map(map_pool_status, url_list))


def main():
    sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', port)
    sock_obj.bind(server_address)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock_obj.listen(5)

    while True:
        # Wait for a connection
        print(sys.stderr, 'waiting for a connection')
        # Now our endpoint knows about the OTHER endpoint.
        client_socket, address = sock_obj.accept()
        print(f"Connection from {address} has been established.")
        sc = sched.scheduler(time.time, time.sleep)

        def do_something():
            list_url = read_csv("url_list.csv")
            data = url_status_checker(list_url)
            msg = pickle.dumps(data)
            print(msg)
            client_socket.send(msg)
            sc.enter(10, 1, do_something)

        sc.enter(10, 1, do_something)
        sc.run()


if __name__ == '__main__':
    #freeze_support()
    #read_csv()
    main()
