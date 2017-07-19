#!/usr/bin

import os
import optparse
import sys

def main():
	parser = optparse.OptionParser("usage %prog [-i] [-r] [-s] [-u <ssid>] [-p <password_for_hotspot>]")
	parser.add_option('-i', dest='install_mode', action='store_true',help='Install mode will modify and download necessary files')
	parser.add_option('-r', dest='run_mode', action='store_true',help='Run mode starts the hotspot')
	parser.add_option('-s', dest='stop_mode', action='store_true',help='Stop mode stops the hotspot')
	parser.add_option('-u', dest='ssid', type='string',help='Specify SSID')
	parser.add_option('-p', dest='password', type='string',help='Specify password for hotspot')
	(options, args) = parser.parse_args()
	imode = options.install_mode
	rmode = options.run_mode
	smode = options.stop_mode
	modeSelected = 0
	if ((imode == True) & (rmode == True)) | ((imode == True) & (smode == True)) | ((rmode == True) & (smode == True)):
		print "\n[-] This tool can only run one mode at a time.\n    Please choose 1 mode.\n"
	elif imode == True:
		modeSelected = modeSelected + 1
		install()
	elif rmode == True:
		modeSelected = modeSelected + 1
		start()
	elif smode == True:
		modeSelected = modeSelected + 1
		stop()
	if ((options.ssid != None) & (options.ssid != " ")) | ((options.password != None) & (options.password != " ")):
		if (options.ssid != None) & (options.password != None):
			HotSpotCredentials(options.ssid, options.password)
		elif options.ssid == None:
			HotSpotCredentials("admin", options.password)
		else:
			HotSpotCredentials(options.ssid, "admin")
	elif modeSelected != 0:
		print ""
	else:
		print "[-] Error in creating credentials.\n    Please try again."

def install():
	SudCommand = 0
	textToEdit1 = ["/etc/udhcpd.conf",
				"start 192.168.42.2\n",
				"end 192.168.42.20\n",
				"interface wlan0\n",
				"remaining yes\n",
				"opt dns 8.8.8.8 4.2.2.2\n",
				"opt subnet 255.255.255.0\n",
				"opt router 192.168.42.1\n",
				"opt lease 864000\n"]
	textToEdit2 = ["/etc/default/udhcpd",
				'#DHCPD_ENABLED="no"\n',
				'#DHCPD_OPTS="-S"']
	textToEdit3 = ["/etc/network/interfaces",
				"source-directory /etc/network/interfaces.d\n",
				"auto lo\n",
				"iface lo inet loopback\n\n",
				"auto eth0\n",
				"iface eth0 inet dhcp\n\n",
				"#allow-hotplug wlan0\n",
				"iface wlan0 inet static\n",
				"    address 192.168.42.1\n",
				"    netmask 255.255.255.0\n",
				"    wireless-power off\n\n",
				"iface default inet dhcp\n",
				"up iptables-restore < /etc/iptables.ipv4.nat"]
	textToEdit5 = ["/etc/default/hostapd",'DAEMON_CONF="/etc/hostapd/hostapd.conf"']
	
	ShellCommands(SudCommand)
	SudCommand = SudCommand + 1

	CreateFiles(textToEdit1)
	CreateFiles(textToEdit2)

	ShellCommands(SudCommand)
	SudCommand = SudCommand + 1

	CreateFiles(textToEdit3)
	HotSpotCredentials("admin", "Admin_Password")
	CreateFiles(textToEdit5)

	ShellCommands(SudCommand)
	SudCommand = SudCommand + 1
	ShellCommands(SudCommand)

def HotSpotCredentials(ssid, password):
	textToEdit4 = ["/etc/hostapd/hostapd.conf",
				"interface=wlan0\n",
				"driver=nl80211\n",
				"ssid=",ssid,"\n", ###############
				"hw_mode=g\n",
				"channel=6\n",
				"macaddr_acl=0\n",
				"auth_algs=1\n",
				"ignore_broadcast_ssid=0\n",
				"wpa=2\n",
				"wpa_passphrase=",password,"\n", ###############
				"wpa_key_mgmt=WPA-PSK\n",
				"rsn_pairwise=CCMP"]
	CreateFiles(textToEdit4)
	print "\n\n[*] Updating Credentials.\n"
	print "\n[*] Credentials for hotspot:\n          SSID: ",ssid,"\n          Password: ",password,"\n"

def CreateFiles(textToEdit):
	i = 1
	file = open(textToEdit[0],"w")
	while i<len(textToEdit):
		file.write(textToEdit[i])
		i=i+1
	file.close()

def ShellCommands(SudCommand):
	if SudCommand == 0:
		os.system("sudo apt-get install hostapd udhcpd")
	elif SudCommand == 1:
		os.system("sudo ifconfig wlan0 192.168.42.1")
	elif SudCommand == 2:
		os.system("sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'")
		os.system("sudo echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf")
	elif SudCommand == 3:
		os.system("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
		os.system("sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT")
		os.system("sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT")
		os.system('sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"')
		#os.system("sudo echo 'up iptables-restore < /etc/iptables.ipv4.nat'>> /etc/network/interfaces")
def start():
	os.system("sudo /etc/init.d/hostapd start")
	os.system("sudo /etc/init.d/udhcpd start")

def stop():
	os.system("sudo /etc/init.d/hostapd stop")
	os.system("sudo /etc/init.d/udhcpd stop")

if __name__ == "__main__":
	main()