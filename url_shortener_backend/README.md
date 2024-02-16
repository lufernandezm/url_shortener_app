# URL Shortener Backend Application

## Prerequisites

Before you begin, ensure you have Python 3.8 or higher installed on your machine. You can verify your Python version by running:

#### `python --version`

### Setting Up the Development Environment

Navigate to the url_shortener_backend directory where the backend application is located:
#### ` cd url_shortener_app/url_shortener_backend`

1. Create a new Virtual Environment 
    #### `python -m venv venv`

2. Activate the Virtual Environment

- On Windows:
    #### `.\venv\Scripts\activate`

- On macOS and Linux:
    #### `source venv/bin/activate`

You should now see (venv) before your command prompt, indicating that the virtual environment is active.

3. Install Dependencies

Before installing dependencies, ensure you are in the url_shortener_backend directory

Then run:
#### `pip install -r requirements.txt`

### Running the Application

Before running the Application, navigate to the src directory where the code is located:

#### ` cd url_shortener_app/url_shortener_backend/app`

To run the FastAPI application, use the following command:
#### `uvicorn main:app --reload`

The --reload flag enables hot reloading, which automatically restarts the server upon code changes.