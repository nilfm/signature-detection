import ftputil
import os

DATA_PATH = "../../Data"

password = 																																									"andy99.Huguet"

if not os.path.isdir(DATA_PATH):
	os.mkdir(DATA_PATH)

with ftputil.FTPHost("ftp.ipage.com", "andreuhuguet78654", password) as ftp_host:
	ftp_host.chdir("hackupc/imgs")
	names = ftp_host.listdir(ftp_host.curdir)
	for name in names:
		print(name)
		ftp_host.download_if_newer(name, os.path.join(DATA_PATH, name))
		
	
