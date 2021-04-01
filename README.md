A program that takes JSON-formatted opening hours of a restaurant as an input and outputs hours in more human-readable
format.

## Demo app

1. Open in the browser: https://py-opening-hours.herokuapp.com/
   -> This will show you following instructions. Just copy and run curl command.
2. Send POST request with JSON string to parse, e.g.

```
curl --header "Content-Type: application/json" --request POST --data '{ "monday":[ ], "tuesday":[ { "type":"open", "value":36000 }, { "type":"close", "value":64800 } ], "wednesday":[ ], "thursday":[ { "type":"open", "value":36000 }, { "type":"close", "value":64800 } ], "friday":[ { "type":"open", "value":36000 } ], "saturday":[ { "type":"close", "value":3600 }, { "type":"open", "value":36000 } ], "sunday":[ { "type":"close", "value":3600 }, { "type":"open", "value":43200 }, { "type":"close", "value":75600 } ] } ' https://py-opening-hours.herokuapp.com/shifts
```

The result will be as below:

```
Monday: Closed
Tuesday: 10 AM - 6 PM
Wednesday: Closed
Thursday: 10 AM - 6 PM
Friday: 10 AM - 1 AM
Saturday: 10 AM - 1 AM
Sunday: 12 PM - 9 PM
```

## Local setup

Setup environment

```
sudo pip3 install virtualenv
python3 -m virtualenv ./venv
source venv/bin/activate
```

Install dependencies

```
pip3 install -r requirements.txt
```

## Local run (for development)

Set entrypoint and run the app

```
export FLASK_APP=opening_hours.py
export FLASK_ENV=development
python -m flask run
```

Navigate to `http://127.0.0.1:5000/shifts` for further instructions

## Testing

To run unit tests use following command:

```
python -m unittest -v
```

## Notes on task

* What if day has only "close" time but no "open" time? Will that day be considered as Work day? For example:

```
	"friday" : [
		 {
			 "type" : "open",
			 "value" : 64800
		 }
	 ],
	 “saturday”: [
		 {
			 "type" : "close",
			 "value" : 3600
		 },
	],
```

-> We will assume such days as Saturday above aren't working days as "close" time counts to previous day shift.

* What if input
	* has mEssed weekdays? -> We will assume a program will use sorted primer for processing
	* has mIssed weekdays? -> We will assume a program will respond with proper error back to client, no shifts
	  processing if validation error

* Some corner cases not covered by current implementation (it's unclear from task description where the input will come
  from and if we guaranteed that the input data is correct):
	* shift opened on new day before closing shift from previous day OR missed closing shift from previous day
	* overlapping shifts (within the same day, for example)
