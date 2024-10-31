# Technical Take-Home for OSENSA

Run `pip install -r requirements.txt`  
Execute with `python main.py lat1 lon1 lat2 lon2 [sampling_period] [sampling_rate]`
### Assumptions

- Program is intended to run for n minutes and get real-time samples from the API
- The "aqi" field in the JSON response is the PM2.5 value.
- The API key is stored in a .env file in the project root directory, under a key named API_TOKEN
- User may enter invalid arguments on the command line, in which case the program will exit with an error message
- Sampling period and sampling rate are optional, default to 5 and 1 respectively

### Edge cases

- The program will exit with a "No data found" message if there are no stations in the given region
- Stations with no data are not included in the average
- The program will exit with a "No stations with data found" message if there are no stations with AQI data in the given
  region

### Design
- Implemented as a `Main` class for ease of sharing data between methods
- Split functionality into helper methods for better readability, maintainability, and testability
- Unit tests for `get_args` and `print_averages` methods defined in `test/test_main.py`
