from turtle import down
from .utils import ftp_download_invoices, upload_multiple_sftp, sftp_download_files
from pathlib import Path
import os
from .models import WholesalerSFTPInfo

host = "ftp.telemasters.co.za"
user =  "daisywc@telemasters.co.za"
passwd = "z]Tj4[Yvt.we"
remote_directory =  "/solid-exports/invoices/pdf/daisy-wc/"



def run():
    out_server = WholesalerSFTPInfo.objects.get(pk=1)
        
    year_month = '2023-Feb' ## TODO Change to become an input OR a auto month thing
    nxc_year_month = '02-2023'
    out_year_month = '2023-02'

    sites = WholesalerSFTPInfo.objects.all().values()

    for ftp in sites:
        if ftp['is_wholesaler'] is True:
            
            # Defining the CDR directory from NextCloud
            nxc_dir = f"/var/www/nextcloud/data/pwxadmin/files/Telemasters/Catalytic/General/CDRs/2023/{nxc_year_month}/Final Billrun/VOICE/{ftp['company']}"
            
            print('Creating invoice directory')
            invoices_directory = f"{os.getcwd()}/{year_month}/{ftp['company']}/invoices/"
            Path(invoices_directory).mkdir(parents=True, exist_ok=True)

            print('Creating CDR directory')
            cdr_directory = f"{os.getcwd()}/{year_month}/{ftp['company']}/CDRs/"
            Path(cdr_directory).mkdir(parents=True, exist_ok=True)
            
            print('Downloading invoices')
            ftp_download_invoices(host=ftp['host'], user=ftp['username'], passwd=ftp['password'], remote_directory=ftp['import_directory'], local_directory=invoices_directory, year_month=year_month)

            print('Downloading CDRs')
            print(nxc_dir)
            sftp_download_files(host='192.168.1.20', user=out_server.username, passwd=out_server.password, remote_directory=nxc_dir, local_directory=cdr_directory)
           
            # ## Uploading the invoices onto SFTP site
            print('Uploading invoices onto SFTP site')
            upload_multiple_sftp(host=out_server.host, user=out_server.username, passwd=out_server.password, remote_directory=f"{ftp['export_directory']}/{year_month}/Invoices", local_directory=invoices_directory)

            # ## Uploading the CDRs onto the SFTP site
            print('Uploading CDRs onto SFTP site')
            upload_multiple_sftp(host=out_server.host, user=out_server.username, passwd=out_server.password, remote_directory=f"{ftp['export_directory']}/{year_month}/Itemized Billing", local_directory=cdr_directory)

        else: pass
    




if __name__ == '__main__':
    run()