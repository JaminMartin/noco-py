import json
import requests


def upload_attachment(path: str, noco_url: str,  base_id: str, table_id: str, table_header: str, api_token: str, ) -> dict:
    """
    Uploads a file to the NocoDB service.

    This function first uploads the file to the dbstorage and then moves it from there into the desired table with a second POST request.

    Parameters:
    path (str): The path of the file to be uploaded.
    noco_url (str): The URL of the NocoDB service.
    base_id (str): The ID of the base where the file will be uploaded.
    table_id (str): The ID of the table where the file will be moved.
    table_header (str): The header of the table where the file will be moved.
    api_token (str): The API token for authentication.

    Returns:
    
    dict: The response from the final POST request.

    """

    file_path = path


    headers = {
        "xc-token": f"{api_token}"
    }


    params = {
        "project_id": f"{base_id}"
    }

    print(file_path)


    files = {
        "json": (None, json.dumps(
            {"api": "xcAttachmentUpload", "project_id": f"{base_id}",
            "dbAlias": "db", "args": {}}), 'application/json'),
        "file": (file_path, open(file_path, 'rb'), 'application/octet-stream')
    }


    r = requests.post(
        f"{noco_url}/api/v1/db/storage/upload",
        files = files,
        headers = headers,
        params = params
    )

    print(r.status_code)
    jsonFilePayload = r.json()
    print(jsonFilePayload)



    headers = {
        "xc-token": f"{api_token}",
        'Content-Type': 'application/json'
    }


    url = f"{noco_url}/api/v1/db/data/noco/{base_id}/{table_id}"     


    payload = json.dumps({
        "title": "temp",
        f"{table_header}": jsonFilePayload,
    })


    r = requests.request("POST", url, headers = headers, data = payload)

    print(r.status_code)
    print(r.json())
