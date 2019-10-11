import ftputil
import os

DATA_PATH = "../../ImageData"

password = 																																									"andy99.Huguet"

def download_imgs():
	if not os.path.isdir(DATA_PATH):
		os.mkdir(DATA_PATH)

	with ftputil.FTPHost("ftp.ipage.com", "andreuhuguet78654", password) as ftp_host:
		ftp_host.chdir("hackupc/imgs")
		names = ftp_host.listdir(ftp_host.curdir)
		for name in names:
			if ftp_host.download_if_newer(name, os.path.join(DATA_PATH, name)):
				print(f"Downloading {name}")
			
		
