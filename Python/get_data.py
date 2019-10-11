import ftputil

password = 																																									"andy99.Huguet"

with ftputil.FTPHost("ftp.ipage.com", "andreuhuguet78654", password) as ftp_host:
	ftp_host.chdir("hackupc/imgs")
	names = ftp_host.listdir(ftp_host.curdir)
	for name in names:
		print(name)
		ftp_host.download_if_newer(name, f"../../Data/{name}")
		
	
