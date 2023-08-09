import os

import requests
import time



if __name__ == "__main__":
    ### 1 => first time !=0=> anything else
    run = 1

    if run == 1:
        ### user
        url = "http://localhost:8000/user/add_user"
        headers = {"Content-Type": "application/json"}
        data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "password": "password123"
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("User added successfully!")
        else:
            print(f"Failed to add user. Status code: {response.status_code}")
            print("Response content:", response.text)

        ### pc
        url = "http://localhost:8000/pc/add_pc"
        headers = {"Content-Type": "application/json"}
        data = {
            "user_id": "1",
            "hardware_uuid": "4C4C4544-0052-5210-8050-C8C04F385932",
            "client_name": "Test Client"
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Request successful!")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

        ###state
        url = "http://localhost:8000/data/initial"
        files = {
            ('files', ('client', open('data/client/client_1690439985645.csv', 'rb'), 'text/csv')),
            ('files', ('disk', open('data/disk/diskStores_1690439985646.csv', 'rb'), 'text/csv')),
            ('files', ('partition', open('data/partition/partitions_1690439985647.csv', 'rb'), 'text/csv')),
        }
        response = requests.post(url, files=files)
        print(response.status_code)
        print(response.text)


    url = "http://localhost:8000/data/?stateId=1"
    file_names = os.listdir("data/application")

    for file_name in file_names:
        file_path = os.path.join("data/application", file_name)
        files = {
            ('files', ('application', open(file_path, 'rb'), 'text/csv')),
            ('files', ('connection', open('data/connection/connection_1690273226472.csv', 'rb'), 'text/csv')),
            ('files', ('resources', open('data/resource/resource_1690273226120.csv', 'rb'), 'text/csv')),
            ('files', ('network', open('data/network/networkInterfaces_1690273226232.csv', 'rb'), 'text/csv')),
        }

        start_time = time.time()

        response = requests.post(url, files=files)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        print(response.status_code)
        print(response.text)



