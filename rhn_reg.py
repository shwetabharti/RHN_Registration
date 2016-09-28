#!/usr/bin/python
import xmlrpclib
import socket
import os
#
SERVER_URL = "http://rhn_server_hostname/rpc/api"
SERVER_LOGIN = "login_id_of_rhn_server_linux_OS"
SERVER_PASSWORD = "password_of_rhn_server_linux_OS"
H_NAME = (socket.gethostname())
#
# Function to check if the system is registered with RHN Satellite 6 or not
def rhn6Check():
	if os.path.isfile("/etc/rhsm/ca/katello-server-ca.pem"):
		rhnCleanSystem()
	else:
        	print("System was not registered with RHN Satellite 6.")

# Function to clean the RHN Satellite 6 registeration locally
def rhnCleanSystem():
	print("This machine is already found registerd with RHN Satellite 6")
	print("Removing the RHN Satellite 6 subscription information locally")
	os.system("/usr/sbin/subscription-manager clean && /bin/rpm -e katello-ca-consumer-crhxxxx0.ccsrm.in-1.0-1.noarch")
# Function to Check the registeration of client in existing RHN 
def rhnCheckSystem():
	client = xmlrpclib.Server(SERVER_URL, verbose=0)
	SESSION_KEY = client.auth.login(SERVER_LOGIN, SERVER_PASSWORD)
	REG_INFO = client.system.getId(SESSION_KEY,H_NAME)
	print("\nMachine registered with below information at RHN: ")
	print(REG_INFO)
	client.auth.logout(SESSION_KEY)
# Function to call registerSystem function if system is not registerd with existing RHN
def rhnRegisterSystem():
	client = xmlrpclib.Server(SERVER_URL, verbose=0)
	SESSION_KEY = client.auth.login(SERVER_LOGIN, SERVER_PASSWORD)
	REG_INFO = client.system.getId(SESSION_KEY,H_NAME)
	print("\nListing any information found for this machine on the RHN Satellite 5.7:")
	print(REG_INFO)
	client.auth.logout(SESSION_KEY)
	DATA_CNT = len(REG_INFO)
	if DATA_CNT > 0:
		print("\nEntry for this machine is already found in RHN Satellite 5.7, kindly contact the RHN Satellite Admin to re-register.")
	else:
		print("Found no information for this machine on RHN Satellite 5.7\n")
		registerSystem()
# Function to register the system with existing RHN 
def registerSystem():
	CNT = raw_input("Do you want to register this machine with RHN satellite 5.7? (y/n): ")
	if CNT == "y":
		print("Downloading Certificate...")
		os.system("/usr/bin/wget -P /usr/share/rhn/ http://crhxxxx0.ccsrm.in/pub/RHN-ORG-TRUSTED-SSL-CERT &>/dev/null && echo 'Download Completed' || echo 'Download failed'")
		print("Running register command. Please wait...")
		os.system("/usr/sbin/rhnreg_ks --activationkey='1-um2p_rhel_activation_key' --serverUrl=https://crhxxxx0.ccsrm.in/XMLRPC  --sslCACert=/usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT --username='rhnadmin' --password='password@123' --force")
		rhnCheckSystem()
		rhnActionEnable()
	else:
		print ("\nScript exiting without registering the system.")
def rhnActionEnable():
	print("\nEnabling RHN Actions for uploading files and executing the remote commands")
	os.system("/usr/bin/yum install rhncfg-actions.noarch &>/dev/null && /usr/bin/rhn-actions-control --enable-all && /usr/bin/rhn-actions-control --report || echo 'Action Failed'")
	print("")
# Calling the functions
rhn6Check()
rhnRegisterSystem()
