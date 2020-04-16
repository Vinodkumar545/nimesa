
from IPython import embed

from dateutil.parser import parse
import pytest
import json


@pytest.fixture(scope='class')
def data(request):

	with open('input_data.json', 'r') as readfile:
		data = json.load(readfile)

	return data


def test_to_verify_response_contains_4_days_of_data(data):
	days = set()
	for info in data['list']:
		d = parse(info['dt_txt'])
		days.add(d.day)

	if len(days) > 4:
		assert True
	else:
		assert False


def test_to_verify_hourly_forecast_interval(data):
	start_time = parse(data['list'][0]['dt_txt'])
	for i in range(1, len(data['list'])):
		end_time = parse(data['list'][i]['dt_txt'])

		# Verify forecast is in hourly interval
		if end_time.minute == 0 and end_time.second == 0:
			diff = end_time - start_time

			if diff.seconds == 3600:
				start_time = end_time

			else:
				print("One Hour is missed.")
				assert False
		else:
			print("Forecast isn't in hourly interval.")
			assert False


def test_to_verify_tempature_for_all_days(data):
	for info in data['list']:
		temp = info['main']['temp']
		temp_min = info['main']['temp_min']
		temp_max = info['main']['temp_max']

		if temp >= temp_min and temp <= temp_max:
			continue
		else:
			print('tempature less or more than min/max.')
			assert True


def test_to_verify_weather_description_for_id_500(data):
	for info in data['list']:
		if info['weather'][0]['id'] == 500:
			if info['weather'][0]['description'] == 'light rain':
				assert True
			else:
				assert False


def test_to_verify_weather_description_for_id_800(data):
	for info in data['list']:
		if info['weather'][0]['id'] == 800:
			if info['weather'][0]['description'] == 'clear sky':
				assert True
			else:
				assert False







