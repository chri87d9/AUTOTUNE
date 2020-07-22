#PWI4 configuration file for the NOVO telescope


# IP-address and port number for the telescope computer running PWI4
NOVO_tel_com_ip = "10.22.88.66"
NOVO_tel_com_port = 8220
#the IP_address and port numbers for the daemon. There are two port numbers, one for each thread.
NOVO_daemon_host = "localhost"
NOVO_daemon_port1 = "8000"
NOVO_daemon_port2 = "9000"

# Directory of the saved logfile and the process-ID 
NOVO_daemon_log = "/tmp/NOVO_daemon.log"
NOVO_daemon_pid = "/tmp/NOVO_daemon.pid"

#Technical settings for the NOVO telescope
NOVO_lower_limit = 16 #Lower limit in altitude for the telescope to slew to.
site = 3 #Mt. Kent Observatory
park_alt = 25 #parking altitude for the telescope
park_azm = 180 #parking azimuth for the telescope.

