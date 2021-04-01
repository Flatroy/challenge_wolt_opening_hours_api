A program that takes JSON-formatted opening hours of a restaurant as an input and outputs hours in more human-readable
format.

# Local setup

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

# Local run (for development)

Set entrypoint and run the app

```
export FLASK_APP=opening_hours.py
python -m flask run
```

Navigate to `http://127.0.0.1:5000/shifts` for further instructions
