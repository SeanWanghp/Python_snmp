- config.yaml:
  - ip dict
  - database config
  - python script macro parameter
  - FTP config
- Main.py:
  - script entry
- Prometheus.py:
  - define prometheus‘ Gauge and port
- Run_script.py:
  - define and run thread in a loop
- SSH.py:
  - get the login information from config.yaml and login to the remote server
- FetchData.py:
  - sort the fetch mode into 'debug' and 'normal'
- Service.py:
  - service layer is used for extending service(such as adding to database)
- Dao.py:
  - data access object: is used for the interaction with database
- AxosMethod.py:
  - the basic function of fetch data, including regular matching
- ecrack.py:
  - is used for dubug mode login by the username of 'calixsupport'
- Login.py:
  - the lowest level of command execution and other important methods
- FTP_server.py:
  - start FTP