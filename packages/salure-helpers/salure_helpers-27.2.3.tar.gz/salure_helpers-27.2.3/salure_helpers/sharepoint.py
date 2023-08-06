import os
import requests
import json
from io import BytesIO
from salure_helpers import SalureConnect


class Sharepoint:
    def __init__(self, salureconnect_connection: SalureConnect, label: str, site: str, site_id: str, json_subset: int, debug: bool = False):
        """
        :param salureconnect_connection: salureconnect connection object for retrieving credentials
        :param label: label of the sharepoint system in salureconnect
        :param site: base url of the sharepoint site
        :param site_id: site id of the sharepoint site
        :param json_subset: fill in the part of the json that needs to be accessed to get the wanted drive id, accompanying the drive you are looking for
        :param debug: set to True to enable debug logging
        """
        self.json_subset = json_subset
        self.salureconnect_connection = salureconnect_connection
        credentials = self.salureconnect_connection.get_system_credential(system='sharepoint', label=label)
        if debug:
            print(f"credentials: {credentials}")
        self.access_token = credentials['access_token']
        self.salureconnect_system_id = credentials['id']
        self.site = site
        self.site_id = site_id
        self.debug = debug
        if self.debug:
            print(f"site: {self.site}, site_id: {self.site_id}, json_subset: {self.json_subset}, credentials: {credentials}, salureconnect_system_id: {self.salureconnect_system_id}")

    def _get_headers(self):
        access_token = self.salureconnect_connection.refresh_system_credential(system='sharepoint', system_id=self.salureconnect_system_id)['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        if self.debug:
            print(headers)

        return headers

    def get_driveid(self):
        """
        This method is used to derive the driveid to which the files have to be uploaded. Needed in the upload url for file upload.
        :return: returns the needed driveid
        """
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.site_id}/drives'
        if self.debug:
            print(f"url: {url}")
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        drive_id = response.json()['value'][self.json_subset]['id']
        if self.debug:
            print(f"drive_id: {drive_id}")

        return drive_id

    def upload_file(self, local_file_path: str, remote_file_path: str):
        """
        This method performs the actual file upload to the formerly derived site + drive.
        local_file_path: local path of the file you want to upload
        remote_file_path: remote path of the folder and filename where you want to place the file
        """
        drive_id = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.site_id}/drives/{drive_id}/root:/{remote_file_path}:/createUploadSession'
        if self.debug:
            print(f"url: {url}")
        headers = self._get_headers()
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        upload_url = response.json()['uploadUrl']
        if self.debug:
            print(f"upload_url: {upload_url}")
        with open(f'{local_file_path}', 'rb') as file_input:
            file_bytes = os.path.getsize(f'{local_file_path}')
            headers_upload = {'Content-Type': 'application/json',
                              'Content-Length': f'{file_bytes}',
                              'Content-Range': f'bytes 0-{file_bytes - 1}/{file_bytes}'}
            response_upload = requests.put(url=upload_url, headers=headers_upload, data=file_input)
            response_upload.raise_for_status()

    def open_file(self, remote_file_path: str) -> bytes:
        """
        Get a file from sharepoint as a bytesstream
        remote_file_path: filepath on sharepoint
        :return: bytes of file object
        """
        drive_id = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.site_id}/drives/{drive_id}/root:/{remote_file_path}'
        if self.debug:
            print(f"url: {url}")
        headers = self._get_headers()
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        download_url = response.json()['@microsoft.graph.downloadUrl']
        if self.debug:
            print(f"download_url: {download_url}")
        response_download = requests.get(url=download_url, headers=headers)
        response_download.raise_for_status()

        return response_download.content

    def download_file(self, local_file_path: str, remote_file_path: str):
        """
        This method downloads a file from sharepoint to the local machine.
        local_file_path: local folder where the file will be downloaded to
        remote_file_path: remote path of the file on sharepoint
        """
        driveid = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.site_id}/drives/{driveid}/root:/{remote_file_path}'
        headers = self._get_headers()
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        download_url = response.json()['@microsoft.graph.downloadUrl']
        response_download = requests.get(url=download_url, headers=headers)
        response_download.raise_for_status()
        with open(file=f'{local_file_path}', mode='wb') as f:
            f.write(BytesIO(response_download.content).read())

    def download_files(self, local_folder_path: str, remote_folder_path: str):
        """
        This method downloads a file from sharepoint to the local machine.
        local_folder_path: local folder where the files will be downloaded to
        remote_folder_path: remote path of the folder you want to get on sharepoint
        """
        driveid = self.get_driveid()
        folder_content = self.list_dir(remote_folder_path=remote_folder_path)
        if self.debug:
            print(f"folder_content: {folder_content}")
        filecount = 0
        for file in folder_content:
            url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.site_id}/drives/{driveid}/root:/{remote_folder_path}{file["name"]}'
            if self.debug:
                print(f"url: {url}")
            headers = self._get_headers()
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            download_url = response.json()['@microsoft.graph.downloadUrl']
            response_download = requests.get(url=download_url, headers=headers)
            with open(file=f'{local_folder_path}{file["name"]}', mode='wb') as f:
                f.write(BytesIO(response_download.content).read())
            filecount += 1
        print(f'{filecount} files downloaded')

    def list_dir(self, remote_folder_path: str) -> json:
        """
        Fetch the contents of the API and return the "children"
        which has the information of all the items under that folder
        remote_folder_path: folder path you want to list
        :return: all the contents of the folder items
        """
        drive_id = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.site_id}/drives/{drive_id}/root:/{remote_folder_path}?expand=children'
        if self.debug:
            print(f"url: {url}")
        response = requests.get(url, headers=self._get_headers(), timeout=120)
        response.raise_for_status()

        return response.json()['children']

    def remove_file(self, remote_file_path: str):
        """
        Remove a file from Sharepoint
        remote_file_path: complete path including filename
        :return: response from Sharepoint
        """
        drive_id = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.site_id}/drives/{drive_id}/root:/{remote_file_path}'
        if self.debug:
            print(f"url: {url}")
        response = requests.delete(url=url, headers=self._get_headers())
        response.raise_for_status()

    def remove_files(self, remote_folder_path: str):
        """
        Remove a file from Sharepoint
        remote_folder_path: folder path that you want to empty
        """
        drive_id = self.get_driveid()
        folder_content = self.list_dir(remote_folder_path=remote_folder_path)
        for file in folder_content:
            url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.site_id}/drives/{drive_id}/root:/{remote_folder_path}{file["name"]}'
            if self.debug:
                print(f"url: {url}")
            response = requests.delete(url=url, headers=self._get_headers())
            response.raise_for_status()
