# OpenWeather API Requests
> This project aims to provide an API to retrieve some information from OpenWeather for desired cities.

## Example
1. Clone the current repository
```bash
$ git clone openweather-api-requests
$ cd openweather-api-requests
```

2. Build docker image and run it
```bash
$ sudo docker build -t openweather-api -f Dockerfile .
$ sudo docker run --name openweather-api --network host -d openweather-api
```

3. Make a request
```bash
$ curl -v -H "Content-Type: application/json" -X POST -d \
'{"city_ids": [3439525, 3439781, 3440645, 3442098, 3442778, 3443341], "api_key": "AAAAAAAAAAAAAAAAA"}' \
http://localhost:5000/getinfo
```

4. Get json files
```bash
$ sudo docker cp openweather-api:data data
```


Where:
- `city_ids`: List of ids for each city
- `api_key`: User key for OpenWeather API
    - You can find [here](https://openweathermap.org/appid) how to create an user api key.
 
 5. Get percentage of computed ids
 ```bash
 $ curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/getinfo
 ```
 ```
 > {"progress": 0.95}
 ```
