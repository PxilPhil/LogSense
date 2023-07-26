import requests

# List of CSV file paths you want to send
if __name__ == "__main__":
    url = "http://localhost:8000/data"
    files = {
        ('files', ('application', open('data/application/application_1690273216270.csv', 'rb'), 'text/csv')),
        ('files', ('connection', open('data/connection/connection_1690273226472.csv', 'rb'), 'text/csv')),
        ('files', ('resources', open('data/resource/resource_1690273226120.csv', 'rb'), 'text/csv')),
        ('files', ('network', open('data/network/networkInterfaces_1690273226232.csv', 'rb'), 'text/csv')),

    }
    response = requests.post(url, files=files)
    print(response.status_code)
    print(response.text)

