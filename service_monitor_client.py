import argparse
import pickle
import socket
import sys, traceback
import os
import pprint
import logging
from datetime import datetime

# Setting of log file
log_filename = "logs/service_monitor_client_output.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(filename=log_filename, filemode='a',
                    format='%(asctime)s %(msecs)d- %(process)d- %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S %p',
                    level=logging.DEBUG)

# Connecting same port as where our service binds
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=8484)
parser.add_argument('-host', '--hostname', default='localhost')

args = parser.parse_args()

# Declaring Global Variables
port = int(args.port)
host_name = args.hostname

pp = pprint.PrettyPrinter(indent=8)
server_address = (host_name, port)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_obj.connect(server_address)


def main():
    while True:
        try:
            msg = sock_obj.recv(10000000)
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M")
            pp.pprint(f"{'*' *30} Summary as of : {dt_string} :{'*' *30}")
            os.system('cls' if os.name == 'nt' else 'clear')
            data = pickle.loads(msg)
            pp.pprint(f"{'*' *30} Summary of Last 1 hour Services(URL) {'*' *30}")
            pp.pprint(data)
            logging.info(f'The summary data: {data}')

        except Exception as e:
            print(f"ERROR{e}")
            traceback.print_exc(file=sys.stdout)
            logging.error(f'The summary data: {traceback.print_exc(file=sys.stdout)}')
        finally:
            pp.pprint(f"{'*' * 30} Completed {'*' * 30}")


if __name__ == '__main__':
    main()
