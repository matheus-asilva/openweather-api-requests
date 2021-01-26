import asyncio                                        # Build Asynchronous I/O
import httpx                                          # Make an Asynchronous Client for HTTP requests
from flask import Flask                               # Build project API
from flask_restful import Resource, Api, reqparse     # Extension for Flask that adds support for quickly building REST APIs with minimal code
import pytz                                           # Handle with timezone
from datetime import datetime as dt                   # Compute datetime of API execution
import json                                           # Store data in JSON file
import time                                           # Compute time spent to make an request call

app = Flask(__name__)
api = Api(app)

async def get_city_info(city_ids: list, api_key: str) -> None:
    """Make an request in the OpenWeatherAPI and saves data in JSON file

    Parameters:
    city_ids (list): List of city ids from OpenWeather
    api_key (str): API's USER ID provided from OpenWeather

    Returns:
    Error message if request fails

    """

    # Transforms list of ids into a string containing each id separated by commas
    request_ids = ",".join([str(i) for i in city_ids])
    
    # Create an async client to make a request to OpenWeather using `request_ids` and `api_key`
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api.openweathermap.org/data/2.5/group?id={request_ids}&appid={api_key}&units=metric")

        # If the response is successful store its information, else returns the error code
        if response.status_code == 200:
            # Get request data
            response_dict = response.json()
            # Use Sao Paulo/Brazil timezone
            datetime = dt.now(pytz.timezone("America/Sao_Paulo"))

            # For each city, save its information into a JSON file
            for city in response_dict["list"]:
                data = {
                    "user_id": api_key,
                    "datetime": datetime,
                    "data": {
                        "city_id": city["id"],
                        "temperature": city["main"]["temp"],
                        "humidity": city["main"]["humidity"]
                    }
                }

                # Set filename with city id and datetime of request 
                filename = "{city_id}_{datetime}.json".format(city_id=data["data"]["city_id"], datetime=datetime.strftime("%Y%m%d_%H%m%S"))

                # Save data to JSON file
                with open(f"data/{filename}", 'w') as fp:
                    json.dump(data, fp, indent=4, sort_keys=True, default=str)
        else:
            message = f"ERROR {response.status_code}"
            print(message)
            return message

class GetInfo(Resource):
    """API Class responsible to get information from OpenWeatherAPI
    """
    def __init__(self):
        """Constructor method
        """
        # Configure required parameters to post request
        self._required_keys = {"city_ids": list, "api_key": str}
        self.reqparse = reqparse.RequestParser()
        for key, value in self._required_keys.items():
            self.reqparse.add_argument(
                key, type = value, required = True, location = 'json',
                help = 'No {} provided'.format(key))
        super(GetInfo, self).__init__()

    async def main(self):
        """Method to make async requests.
        Since OpenWeather only accepts 20 cities per request we need to split city ids list to handle with batches of 20 ids
        """

        # Variables to store information to compute percentage of completed ids
        global total_cities
        global cities_left

        # Get parameters from parser
        args = self.reqparse.parse_args()

        # Save number of ids
        total_cities = len(args.city_ids)
        cities_left = len(args.city_ids)
        
        # Compute request for batches of 20 ids each
        task_list = []
        i = 0
        max_ids_per_request = 20
        
        while True:
            s0 = i * max_ids_per_request
            s1 = min(len(args.city_ids), (i + 1) * max_ids_per_request)
            task_list.append(get_city_info(args.city_ids[s0:s1], args.api_key))
            i += 1

            if s1 == len(args.city_ids):
                break
        await asyncio.gather(*task_list)

    def post(self):
        """Method to create post route
        """
        start_time = time.monotonic()
        # Begins asynchronous requests
        asyncio.run(self.main())
        return f"Time Taken: {time.monotonic() - start_time} seconds"
    
    def get(self):
        """Method to create get route
        """
        return {"progress": cities_left / total_cities}

# Creates an endpoint
api.add_resource(GetInfo, '/getinfo')

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
