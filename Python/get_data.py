import ftputil
import os

PATH_DATA = "../../ImageData"

password = 																																									"andy99.Huguet"

def download_imgs():
	if not os.path.isdir(PATH_DATA):
		os.mkdir(PATH_DATA)

	with ftputil.FTPHost("ftp.ipage.com", "andreuhuguet78654", password) as ftp_host:
		ftp_host.chdir("hackupc/imgs")
		names = ftp_host.listdir(ftp_host.curdir)
		for name in names:
			if not name.lower().startswith('jordi') and name[0] != '_' and ftp_host.download_if_newer(name, os.path.join(PATH_DATA, name)):
				print(f"Downloading {name}")
			

if __name__ == '__main__':
	download_imgs()
