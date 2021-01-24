# OpenWeather API Requests
> This project aims to provide an API to retrieve some information from OpenWeather for desired cities.

## Example
1. Clone the current repository
```bash
$ git clone https://github.com/matheus-asilva/openweather-api-requests.git
$ cd openweather-api-requests
```

2. Build docker image
```bash
$ sudo docker build -t openweather-api -f Dockerfile .
```

3. Make a request
```bash
$ curl -i -H "Content-Type: application/json" -X POST -d \
'{"city_ids": [3439525, 3439781, 3440645, 3442098, 3442778, 3443341], "api_key": "AAAAAAAAAAAAA"}' \
http://127.0.0.1:5000/getinfo
```
Where:
- `city_ids`: List of ids for each city
- `api_key`: User key for OpenWeather API
    - You can find [here](https://openweathermap.org/appid) how to create an user api key.
 
 4. Get percentage of computed ids
 ```bash
 $ curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/getinfo
 ```
 ```
 > {"progress": 0.95}
 ```
 ---

