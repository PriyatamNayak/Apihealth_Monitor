# Apihealth_Monitor

	This script is written in python3.7

	it supports python3.7 and above

	purpose: This will monitor the url status

	Have used python socket model to bind with port and send the data

How to run:

	 i)Please install the required library mentioned in requirements.txt by running ( pip install -r requirements.txt)
	 
	 ii) Run the  below command
		   python service_monitor.py
		   note: it will bind to default port 8484 and will  load the urls from "url_list.csv"
		   
	 iii) This will be the main process to check the url status in every 10 minutes (it is the socket server process which will send data)
	 
	 iv) you can give the url name and value in "url_list.csv" file
	 
	 v)After this process ready ,follow the below steps
	 
	 vi) To view the summary you can run the client service_monitor_client.py which will recieve data every 1 hour
	    
		note: if you are running clinet script in different host wrt to service_monitor.py then provide the hostname with -host parameter
		 example: if service_monitor.py is running on 10.20.30.50
		 and you want to run client.py other than  10.20.30.52
		 then run as 
		 
		 python service_monitor_client.py -host 10.20.30.50 -p 8484

	   if same host:  run the client service use the below command
	   
		  python service_monitor_client.py
	  
	 viii) you can also change the port using "-p" in both the script
	 
	 ix) Note: the port will be same both the scripts
	 
	  x) you can also change the default file path with -f option ,use help command to know how to use the script
	  
	 xi) if you are facing any issue, Plaese send me a mail (prisankunyk@gmail.com)
	  
  github link: https://github.com/PriyatamNayak/Apihealth_Monitor.git
  
CI/CD:

tools needed
	1)bitbucket

	2)sonarqube

	3)jenkin

	4) any deployment server or container or cloud ( here we are choosing vm)


		i) bit bucket as code repository

		ii) After commit , raise a pull request to merge your code with integration branch or master branch

		iii) after reviewer approval and merge the code with integration branch

		iv) it will trigger the jenkin pipeline job

		v) this pipline consists below steps

			a) run the unit test cases with help of SonarQube 
			
			b) if test case passed ,SonarQube also checks the code smells, and security vulnerabilities
			
			c) if it passed above steps
			
			d) jenkin build the source code and produce tar file and upload to some secure central repository for build code
			
			e) then jenkin pipeline login to vm using the encrypted credentials
			
			f) deploy the code using unix script provided in jenkin pipeline
			
		vi) pipiline will start the service using "start_service.sh" script
		vii) pipiline will send the mail about buld deployment status
		viii)Done
	
	
	