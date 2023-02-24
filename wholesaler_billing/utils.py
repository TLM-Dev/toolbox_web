from pathlib import Path
import paramiko
import os
from ftplib import FTP
from pathlib import Path

def sftp_download_files(host: str, user: str, passwd: str, remote_directory: str, local_directory: str, **kwargs) -> None:
    paramiko.util.log_to_file("paramiko_wholesaler_invoices.log")
    
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=passwd)

        sftp = ssh.open_sftp()
        sftp.chdir(remote_directory)

        for attr in sftp.listdir_attr(path=''):
            sftp.get(remotepath=attr.filename, localpath=f'{local_directory}/{attr.filename}')


def mkdir_p(sftp, remote_directory):
    """Change to this directory, recursively making new folders if needed.
    Returns True if any folders were created."""
    if remote_directory == '/':
        # absolute path so change directory to root
        sftp.chdir('/')
        return
    if remote_directory == '':
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_directory) # sub-directory exists
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip('/'))
        mkdir_p(sftp, dirname) # make parent directories
        sftp.mkdir(basename) # sub-directory missing, so created it
        sftp.chdir(basename)
        return True


def ftp_download_invoices(host: str, user: str, passwd: str, remote_directory: str, local_directory: str, year_month, **kwargs) -> None:
    with FTP(host) as ftp:
        ftp.login(user=user, passwd=passwd)
        ftp.cwd(f'{remote_directory}/{year_month}')
        for file in ftp.nlst():
            if "Invoice" in file:
                with open(os.path.join(local_directory, file), 'wb') as f:
                    print(f)
                    ftp.retrbinary('RETR ' + file, f.write)
    

def upload_multiple_sftp(host: str, user: str, passwd: str, remote_directory: str, local_directory: str,**kwargs) -> None:
    paramiko.util.log_to_file("paramiko_wholesaler_invoices.log")
    
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=passwd)

        sftp = ssh.open_sftp()
        mkdir_p(sftp=sftp, remote_directory=remote_directory)
        sftp.chdir(remote_directory)

        for file in os.listdir(local_directory):
            sftp.put(localpath=f"{local_directory}/{file}", remotepath=f'{remote_directory}/{file}')

def delete_everything(filename):
    os.remove(filename)


## /solid-exports/invoices/pdf/daisy-wc/2022-Sep