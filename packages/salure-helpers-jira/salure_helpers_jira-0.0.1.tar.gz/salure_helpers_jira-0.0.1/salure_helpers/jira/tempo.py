import json
import requests


class Tempo:
    def __init__(self, access_token: str):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def get_tempo_hours(self, from_date: str = None, to_date: str = None) -> json:
        """
        This function gets hours from Tempo for max 8 backs week
        :param from_date:
        :param to_date:
        :return: json response with results
        """
        total_response = []
        got_all_results = False
        no_of_loops = 0

        while not got_all_results:
            parameters = {"from": f"{from_date}", "to": f"{to_date}",
                          "limit": 1000,
                          "offset": 1000 * no_of_loops}
            response = requests.get('https://api.tempo.io/core/3/worklogs', headers=self.headers, params=parameters)
            if response.status_code == 200:
                response_json = response.json()
                no_of_loops += 1
                got_all_results = False if int(response_json['metadata']['count']) == 1000 else True
                total_response += response_json['results']
            else:
                raise ConnectionError(f"Error getting worklogs from Tempo: {response.status_code, response.text}")

        if self.debug:
            print(f"Received {len(total_response)} lines from Tempo")

        return total_response
