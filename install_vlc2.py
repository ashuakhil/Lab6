import requests
import hashlib
import subprocess
import os

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/'
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        file_content = response.text
        sha256_lines = file_content.split('\n')
        for line in sha256_lines:
            if 'vlc-3.0.17.4-win64.exe' in line:
                expected_sha256 = line.split()[0]
                return expected_sha256
    

def download_installer():
    url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        installer_data = response.content
        return installer_data
   

def installer_ok(installer_data, expected_sha256):
    if installer_data is not None:
        computed_sha256 = hashlib.sha256(installer_data).hexdigest()
        return computed_sha256 == expected_sha256
    print(computed_sha256)
    


def save_installer(installer_data):
   temp_folder = os.getenv('TEMP')
   installer_path = os.path.join(temp_folder, 'vlc-3.0.17.4-win64.exe')
   with open(installer_path, 'wb') as file:
        file.write(installer_data)
   return installer_path  

def run_installer(installer_path):
    installer_path = 'vlc-3.0.17.4-win64.exe'
    subprocess.run([installer_path, '/L=1033', '/S'])

def delete_installer(installer_path):
    os.remove(installer_path)

if __name__ == '__main__':
    main()
