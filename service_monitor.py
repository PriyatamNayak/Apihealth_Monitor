# python 3.7
import argparse
import concurrent.futures
import csv
from datetime import datetime
import logging
import socket
import sched
import sys
import time
import os
import pickle
import urllib3

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=8484)
parser.add_argument('-f', '--file_path', default="url_list.csv")
parser.add_argument('-o', '--output_file_path', default="output/output.txt")
args = parser.parse_args()

# Declaring Global Variables
port = int(args.port)
input_file = args.file_path
output_file = args.output_file_path
http = urllib3.PoolManager()
monitor_data = []
now = datetime.now()

no_of_services_up_counter = 0
no_of_services_down_counter = 0
name_of_services_down_list = []

log_filename = "logs/service_monitor_output.log"
output = "output/output.txt"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
os.makedirs(os.path.dirname(output), exist_ok=True)
logging.basicConfig(filename=log_filename, filemode='a',
                    format='%(asctime)s %(msecs)d- %(process)d- %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S %p',
                    level=logging.DEBUG)


def read_csv(csv_file=input_file):
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
            try:
                if ''.join(line).strip():  # skipping blank lines
                    url_name, url_val = line[0], line[1].strip()  # Removing space from url
                    temp[url_name] = url_val
            except Exception as e:
                print("Ignoring Exception")
                print(f'{e} data: {line}')
                return []
            return temp

        url_list = list(map(map_pool, url_data))

    return url_list


def url_status_checker(url_list):
    """
   :param url_list: dict of url name and url address
   :return:  it will return url  and url status as list
   """

    def map_pool_status(url_item):
        global no_of_services_up_counter
        global no_of_services_down_counter
        global name_of_services_down_list

        url_status_dict = {}
        url_name = next(iter(url_item))
        url_value = url_item[url_name]
        try:
            response = http.request('GET', url_value, timeout=5)
            url_status_dict[url_name] = response.status
            if response.status == 200:
                no_of_services_up_counter = no_of_services_up_counter + 1
            else:
                no_of_services_down_counter = no_of_services_down_counter + 1
                name_of_services_down_list.append(f'{url_name}:{response.status}')

        except urllib3.exceptions.MaxRetryError:
            url_status_dict[url_name] = "503"
            no_of_services_down_counter = no_of_services_down_counter + 1
            name_of_services_down_list.append(f'{url_name}:503')
        except:
            url_status_dict[url_name] = "700"  # customized error code
            no_of_services_down_counter = no_of_services_down_counter + 1
            name_of_services_down_list.append(f'{url_name}:700')
        finally:
            return url_status_dict

    # Used ThreadPool as it is IO based task GIL will not impact this but have to test with large data for benchmark
    # We can use multiprocessing pool(here ProcessPoolExecutor) to remove impact of GIL
    # thread pool automatic take care of threading.lock to avoid dead lock condition and count
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        result = list(map(map_pool_status, url_list))
    # Let's put the whole status  to a log file ,for debugging
    logging.info(f'Data {result}')
    global no_of_services_up_counter
    global no_of_services_down_counter
    global name_of_services_down_list
    summary_of_last_10_list = []
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    summary_of_last_10_list.append(f"Summary of service status around: {dt_string}")
    summary_of_last_10_list.append("-"*50)
    summary_of_last_10_list.append("-" * 50)
    summary_of_last_10_list.append(f"Total number service(URL) are UP and Running: {no_of_services_up_counter}")
    summary_of_last_10_list.append(f"Total Number of service(URL) is Down: {no_of_services_down_counter}")
    summary_of_last_10_list.append(f"List of name URL was down: {name_of_services_down_list}")
    summary_of_last_10_list.append("-"*50)
    summary_of_last_10_list.append("-" * 50)
    no_of_services_up_counter = 0
    no_of_services_down_counter = 0
    name_of_services_down_list = []
    logging.info(f'The summary data: {summary_of_last_10_list}')
    return summary_of_last_10_list


def run():
    """
    purpose: it is the main process to run the program
    :return: None
    """
    sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', port)
    sock_obj.bind(server_address)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    logging.info(f'starting up on  port {server_address}')
    sock_obj.listen(5)

    while True:
        # Wait for a connection
        print(sys.stderr, 'waiting for a connection')
        # Now our endpoint knows about the OTHER endpoint.
        client_socket, address = sock_obj.accept()
        print(f"Connection from {address} has been established.")
        # We are scheduling it instead of using Sleep method
        sc = sched.scheduler(time.time, time.sleep)

        def url_status_check():
            global monitor_data
            list_url = read_csv(input_file)
            data = url_status_checker(list_url)
            monitor_data.append(data)
            sc.enter(600, 1, url_status_check)

        def send_monitor_data():
            """
            :return:
            """
            global monitor_data
            # Make sure we are taking last 1 hour data , so we are taking last 6 data from data list
            temp = monitor_data[-6:]
            # We are making empty, as we need to store max 1 hour data
            monitor_data = []
            msg = pickle.dumps(temp)
            client_socket.send(msg)
            logging.info(f'The monitoring data: {temp}')
            # Saving the results
            with open(output_file, 'w') as f:
                for item in temp:
                    f.write("%s\n" % item)
            # running every 60 minutes
            sc.enter(3600, 2, send_monitor_data)

        sc.enter(600, 1, url_status_check)
        sc.enter(3600, 2, send_monitor_data)

        sc.run()


if __name__ == '__main__':
    run()
