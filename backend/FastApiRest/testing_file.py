import requests

# List of CSV file paths you want to send
if __name__ == "__main__":
    url = "http://localhost:8000/data"
    files = {
        ('application', ('1.csv', open('C:/Users/philipp.borbely/Documents/LogSenseRepo/logsense/backend/FastApiRest/data/processes/process_1689237893216.csv', 'rb'), 'text/csv')),
        ('files', ('2.csv', open('C:/Users/philipp.borbely/Documents/LogSenseRepo/logsense/backend/FastApiRest/data/processes/process_1689237955009.csv', 'rb'), 'text/csv')),

    }
    response = requests.post(url, files=files)
    print(response.status_code)
    print(response.text)

