import requests


def post_request():
    for i in range(10):
        url = "http://127.0.0.1:8000/weather/add_data"
        params = {
            "id": 59999,
            "date": "2017-01-02",
            "precipitation": 20,
            "high_temperature": 25,
            "relative_humidity": 40,
            "evaporation": 20         
        }
        r = requests.post(url=url, params=params)
        print(f"{r.json()}\n")

def get_data():
    for i in range(10):
        url = "http://127.0.0.1:8000/weather/get_data"
        params = {
            "id": 59999,
            "year": "2017",
            "month": "01",
            "day": "02",  
        }
        r = requests.get(url=url, params=params)
        print(f"{r.json()}\n")
}
if __name__ == "__main__":
    post_request()
    get_data()