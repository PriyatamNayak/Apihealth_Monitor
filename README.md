# Apihealth_Monitor

This script is written in python3.7
it supports python3.7 and above

purpose: This will monitor the url status

Have used python socket model to bind with port and send the data

how to run:
 i)Please install the required library mentioned in requirements.txt
 ii) Run the  below command
       python service_monitor.py
	   note: it will bind to default port 8484 and will  load the urls from "url_list.csv"
	   
 iii) This will be the main process to check the url status in every 10 minutes (it is the socket server process which will send data)
 
 iv) you can give the url name and value in "url_list.csv" file
 v) To view the result you can run the client service_monitor which will recieve data every 1 hour
 vi) to run the client service use the below command
    python service_monitor_client.py
  
  vii) you can also chnage the port using "-p" in both the script
  viii) Note: the port will be same both the scripts
  ix) you can also change the default file path with -f option ,use help command to know how to use the script
  x) if you are facing any issue, Plaese send me a mail (prisankunyk@gmail.com)
  
  github link: https://github.com/PriyatamNayak/Apihealth_Monitor.git