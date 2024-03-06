# Image Manipulation User Interface

## Features
* User Interface using flask templates and flask-wtf forms for improved input validation
* Image manipulation implemented through the views route
* Routes authentication using flask-login
* Image input validation
* User Models and Forms

## Requirements
This project is installed within a virtual environment.

* Run the current venv as: `source venv/bin/activate` 
  or instanciate your own virtual enviroment by running: `python3 -m vevn venv` 

* Install all the project requirements by running: `pip3 install -r requirements.txt`

### Installation Instructions
In case you experience an issue installing the requirements.txt file you can manually install:
`pip3 install Flask==3.0.2 WTForms==3.1.2 SQLAlchemy==2.0.28 pillow==10.2.0`
Also consider the python version of this project is == 3.10.12 

## Usage
Run the flask application as follows:
* Navigate to the directory where your Flask application code is located using the terminal.
* Activate your virtual enviroment
* Run the following command to start the Flask application:
`python3 ./app.py`
* Navigate to the sign_up page using the following URI Format: `{base_url}/sign-up`  
* Sign Up - Create an account so you can access the protected routes

## Routes

### Auth Route
----------
#### Sign Up
- **URL**: `/sign-up`
- **Methods**: `GET`, `POST`
- **Description**: Allows users to register for a new account.
- **Parameters**:
  - `username` (string, required): User's desired username.
  - `email` (string, required): User's email address.
  - `password` (string, required): User's password.
- **Response**:
  - `200 OK`: Account created successfully.
  - `302 Found`: Redirects to the home page after successful registration.
- **Template**: `sign_up.html`

#### Login
- **URL**: `/login`
- **Methods**: `GET`, `POST`
- **Description**: Allows registered users to log in to their accounts.
- **Parameters**:
  - `username` (string, required): User's username.
  - `password` (string, required): User's password.
- **Response**:
  - `200 OK`: Logged in successfully.
  - `302 Found`: Redirects to the home page after successful login.
- **Template**: `login.html`

#### Logout
- **URL**: `/logout`
- **Methods**: `GET`
- **Description**: Allows logged-in users to log out of their accounts.
- **Response**: `302 Found`: Redirects to the login page after logout.
- **Template**: None

### Views Route
-------------

#### Home
- **URL**: `/`
- **Methods**: `GET`
- **Description**: Renders the home page.
- **Authentication**: Requires the user to be logged in.
- **Template**: `home.html`

#### Upload Image
- **URL**: `/upload-image`
- **Methods**: `GET`, `POST`
- **Description**: Allows users to upload images.
- **Parameters**:
  - `image` (file, required): Image file to be uploaded.
- **Response**: Redirects to the upload page with appropriate flash messages.
- **Template**: `upload_image.html`

#### List Images Page
- **URL**: `/list-images-page`
- **Methods**: `GET`, `POST`
- **Description**: Renders a page listing uploaded images.
- **Authentication**: Requires the user to be logged in.
- **Template**: `list_images.html`

#### List Images
- **URL**: `/list-images`
- **Methods**: `GET`
- **Description**: Lists uploaded images.
- **Authentication**: Requires the user to be logged in.
- **Response**: Returns a list of image filenames.
  
#### Delete Image
- **URL**: `/delete-image/<filename>`
- **Methods**: `POST`
- **Description**: Deletes the specified image.
- **Parameters**:
  - `filename` (string, required): Name of the image file to delete.
- **Response**: Redirects to the list images page with appropriate flash messages.

#### Download Image
- **URL**: `/download-image/<filename>`
- **Methods**: `GET`
- **Description**: Allows users to download the specified image.
- **Parameters**:
  - `filename` (string, required): Name of the image file to download.
- **Response**: Downloads the specified image file.
  
#### Modify Image Page
- **URL**: `/modify-image-page`
- **Methods**: `GET`
- **Description**: Renders a page to modify images.
- **Authentication**: Requires the user to be logged in.
- **Template**: `modify_image.html`

#### Modify Image
- **URL**: `/modify-image/<filename>`
- **Methods**: `POST`
- **Description**: Allows users to modify images.
- **Parameters**:
  - `filename` (string, required): Name of the image file to modify.
  - `width` (int, optional): New width of the image.
  - `height` (int, optional): New height of the image.
  - `rotate` (int, optional): Rotation angle of the image.
  - `contrast` (float, optional): Contrast level of the image.
- **Response**: Redirects to the modify image page with appropriate flash messages.

## Model Documentation

### User Model
- **Description**: Represents a user of the application.
- **Attributes**:
  - `id` (integer): Primary key identifying the user.
  - `username` (string, max length: 64): Unique username of the user.
  - `email` (string, max length: 120): Unique email address of the user.
  - `password_hash` (string, max length: 128): Hashed password of the user.
  - `date_created` (datetime): Date and time when the user account was created.
- **Methods**:
  - `set_password(password)`: Sets the password for the user after hashing it.
  - `check_password(password)`: Checks if the provided password matches the hashed password stored in the database.
- **Representation**: Returns a string representation of the user object containing the username.

## Forms Documentation

### RegistrationForm
- **Description**: Form for user registration.
- **Fields**:
  - `username` (StringField): User's desired username. Required. Length: 2-64 characters.
  - `email` (StringField): User's email address. Required. Length: 4-120 characters. Should be a valid email format.
  - `password` (PasswordField): User's password. Required. Length: 5-128 characters.
  - `password2` (PasswordField): Confirmation of the user's password. Required. Must match the password field.
- **Validators**:
  - `validate_username(username)`: Validates the uniqueness of the username. Raises a validation error if the username is already taken.
  - `validate_email(email)`: Validates the uniqueness of the email address. Raises a validation error if the email is already registered.
- **Submit Button**:
  - `submit` (SubmitField): Submits the registration form.

## Initialization Documentation / `__init__.py`

### create_app Function
- **Description**: Initializes and configures the Flask application.
- **Steps**:
  1. Creates a Flask app instance.
  2. Sets the secret key for session management.
  3. Configures the SQLite database.
  4. Initializes the SQLAlchemy extension for database operations.
  5. Configures the upload folder for image manipulation.
  6. Registers blueprints for different parts of the application.
  7. Imports models and creates the database if it doesn't exist.
  8. Configures the login manager for user authentication.

### create_database Function
- **Description**: Creates the SQLite database if it doesn't exist.
- **Steps**:
  1. Checks if the database file exists.
  2. If the database file doesn't exist, creates all tables defined in the models.

### Configuration
- **SECRET_KEY**: Unique key used for session management.
- **SQLALCHEMY_DATABASE_URI**: Path to the SQLite database file.
- **SQLALCHEMY_TRACK_MODIFICATIONS**: Configuration flag to suppress SQLAlchemy event system notifications.

### Blueprints
- **Views**: Contains routes and logic for rendering HTML templates.
- **Auth**: Handles user authentication and authorization.

### Models
- **User**: Represents a user of the application.

### Login Manager Configuration
- **login_view**: Specifies the view to redirect users to for login if they attempt to access a protected route without authentication.
- **user_loader**: Callback function to load a user object from the database based on the user's ID.

## Dependencies
- **Flask**: Web framework for building web applications in Python.
- **Flask-Login**: Provides user session management for Flask.
- **Flask-SQLAlchemy**: Flask extension for working with SQLAlchemy, a Python SQL toolkit.
- **os.path**: Module for manipulation of file paths.

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

