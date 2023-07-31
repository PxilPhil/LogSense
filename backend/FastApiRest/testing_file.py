import os

import requests
import time



"""
if __name__ == "__main__":
    url = "http://localhost:8000/data/initial"

    files = {
        ('files', ('client', open('data/client/client_1690439985645.csv', 'rb'), 'text/csv')),
        ('files', ('disk', open('data/disk/diskStores_1690439985646.csv', 'rb'), 'text/csv')),
        ('files', ('partition', open('data/partition/partitions_1690439985647.csv', 'rb'), 'text/csv')),
    }
    response = requests.post(url, files=files)
    print(response.status_code)
    print(response.text)
"""

if __name__ == "__main__":
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



