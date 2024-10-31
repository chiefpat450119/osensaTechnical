import sys
from dotenv import load_dotenv
import os
import time
import requests


class Main:
	def __init__(self, args: list):
		self.args = args
		self.lat1 = None
		self.lon1 = None
		self.lat2 = None
		self.lon2 = None
		self.sampling_period = 5  # Default value in minutes
		self.sampling_rate = 1  # Default value, samples per minute
		self.api_token = os.getenv("API_TOKEN")
		self.base_url = "https://api.waqi.info/v2/"
		self.station_dict = {}  # Maps stations to a list of aqi values

	def get_args(self) -> bool:
		if len(self.args) < 4 or len(self.args) > 6:
			print("Invalid number of arguments, expected: lat1, lon1, lat2, lon2, sampling_period and sampling_rate")
			return False
		try:
			self.lat1 = float(self.args[0])
			self.lon1 = float(self.args[1])
			self.lat2 = float(self.args[2])
			self.lon2 = float(self.args[3])
			if len(self.args) > 4:
				self.sampling_period = float(self.args[4])
			if len(self.args) > 5:
				self.sampling_rate = float(self.args[5])
		except ValueError:
			print("Invalid arguments: lat1, lon1, lat2, lon2, sampling_period and sampling_rate must be numbers")
			return False
		if any([self.lat1 < -90,
				self.lat1 > 90,
				self.lon1 < -180,
				self.lon1 > 180,
				self.lat2 < -90,
				self.lat2 > 90,
				self.lon2 < -180,
				self.lon2 > 180,
				self.sampling_period <= 0,
				self.sampling_rate <= 0]):
			print("Invalid arguments")
			return False
		return True

	def run(self) -> int:
		if not self.get_args():
			return 1

		# Ceil so samples is at least 1
		total_samples = max(1, int(self.sampling_period * self.sampling_rate))

		for _ in range(total_samples):
			success = self.get_sample()
			if not success:
				return 1

			time.sleep(60 / self.sampling_rate)

		self.print_averages()
		return 0

	def get_sample(self)-> bool:
		# Add trailing zeros to lat and lon since this is required by the API
		lat1 = "{:.6f}".format(self.lat1)
		lon1 = "{:.6f}".format(self.lon1)
		lat2 = "{:.6f}".format(self.lat2)
		lon2 = "{:.6f}".format(self.lon2)

		latlng = f"{lat1},{lon1},{lat2},{lon2}"
		url = f"{self.base_url}map/bounds?token={self.api_token}&latlng={latlng}"
		response = requests.get(url)

		if response.status_code != 200:
			print(f"Error: {response.status_code}")
			return False

		data = response.json()
		if not data["data"]:
			print("No data found, no stations in specified region")
			return False

		for station in data["data"]:
			station_name = station["station"]["name"]
			if station_name not in self.station_dict:
				self.station_dict[station_name] = []
			aqi_string = station["aqi"]
			# Skip stations with no data
			if aqi_string == "-":
				continue
			self.station_dict[station_name].append(int(aqi_string))

		return True

	def print_averages(self) -> float:
		all_values = []
		print("PM2.5 values per station:")
		for station, aqi_values in self.station_dict.items():
			if not aqi_values:
				print(f"{station}: No data")
				continue
			avg = sum(aqi_values) / len(aqi_values)
			print(f"{station}: {avg:.2f}")
			all_values.extend(aqi_values)

		if not all_values:
			print("No stations with data found")
			return -1.0
		else:
			print("Overall average:")
			average = sum(all_values) / len(all_values)
			print(f"{average:.2f}")
			return average




if __name__ == "__main__":
	load_dotenv()
	arguments = sys.argv[1:]
	main = Main(arguments)
	sys.exit(main.run())
