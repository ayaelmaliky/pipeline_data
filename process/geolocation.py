import requests
from requests import Response

def get_geolocation(ip):
   response: Response = requests.get(f"https://ipwho.is/{ip}")
   if response.status_code == 200:
      return response.json()


if __name__ == "__main__":
    print(get_geolocation("109.199.110.135"))
    