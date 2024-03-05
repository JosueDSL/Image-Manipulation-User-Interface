# Image Manipulation 

## Features
* Image manipulation implemented through the views route
* Authentication route
* Protecting Routes with JSON Web Tokens (JWT)
* Image input validation

## Requirements
This project is installed within a virtual environment.

* Run the current venv as: `source venv/bin/activate` 
  or instanciate your own virtual enviroment by running: `python3 -m vevn venv` 

* Install all the project requirements by running: `pip3 install -r requirements.txt`

### Installation Instructions
In case you experience an issue installing the requirements.txt file you can manually install:
`pip3 install Flask==3.0.2 Flask-JWT-Extended==4.6.0 pillow==10.2.0`
Also consider the python version of this project is == 3.10.12 

## Usage
Run the flask application as follows:
* Navigate to the directory where your Flask application code is located using the terminal.
* Activate your virtual enviroment
* Run the following command to start the Flask application:
`python3 ./app.py`
* Reference the [Postman documentation](https://winter-resonance-429104.postman.co/workspace/Team-Workspace~6d41255b-83d1-482e-89c9-6284c7496940/collection/33375466-2b0e2b6d-c815-4d8f-a986-ef0b0a7e2947?action=share&creator=33375466) 
* Go to the `login` request endpoint, send a POST requests as especified in the API documentation to get the Bearer token and apply it to all the requests inside the Image-Manipulation folder

### General File Structure:
```bash
project/
├── venv/
│   ├── bin/
│   ├── include/
│   ├── lib/
│   └── ...
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── templates/
│       └── index.html #example
├── requirements.txt
└── run.py     # (app.py)
```

