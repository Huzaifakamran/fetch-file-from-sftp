import paramiko
import os
import gzip
import shutil

# Define your SFTP server credentials and settings
sftp_host = ''
sftp_port = 
sftp_username = ''
sftp_password = ''

# Define local and remote file paths
local_directory = 'D:\\TMC\\Telenor\\Shell Script\\python_script\\'
remote_directory_path = '/backup/'  

try:
    transport = paramiko.Transport((sftp_host, sftp_port))
    transport.connect(username=sftp_username, password=sftp_password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print("Connection successfully established ...")
    sftp.chdir(remote_directory_path)
    directory_structure = sftp.listdir_attr()
    print("Directory structure:")
    for attr in directory_structure:
        print(attr.filename, attr)
    
    # Upload a file to the remote server
    # sftp.put(local_file_path, remote_file_path)
    # print(f"File {local_file_path} uploaded to {remote_file_path}")

    
    for attr in directory_structure:
        if attr.filename.endswith('.gz'):
            remote_file_path = os.path.join(remote_directory_path, attr.filename)
            local_file_path = os.path.join(local_directory, attr.filename)
            
            print(f"Downloading {attr.filename} ...")
            sftp.get(remote_file_path, local_file_path)
            print(f"File {attr.filename} downloaded to {local_file_path}")
            
            unzipped_file_path = local_file_path.rstrip('.gz')
            with gzip.open(local_file_path, 'rb') as f_in:
                with open(unzipped_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"File {local_file_path} unzipped to {unzipped_file_path}")
            
            # Optionally, remove the .gz file after extraction
            os.remove(local_file_path)
            print(f"Removed the .gz file: {local_file_path}")

    # Close the SFTP session
    sftp.close()
    transport.close()
    print("SFTP operations completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
