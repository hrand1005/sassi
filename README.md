# sassi
sassi the scheduling assistant sends you reminders about your upcoming obligations.

# Setup
To set up for development, pip install the requirements:
```
pip3 install -r requirements.txt
```
Currently the app is hard-coded to use the provided configuration in `config.json`.
To run the app in development mode, run `./develop.sh`. You may also run the application
without any environment variables set with `python3 app.py` or `flask run`.

# Project Layout
This repo uses a relatively flat project layout. All routes (endpoints) are registered in 
the `.py` files in the root directory. `auth.py` contains endpoints and decorators for 
authentication and registration, and `events.py` defines endpoints for the `event` resource.
`models/` contains database document-models which double as classes for our MongoDB operations.
`templates/` define html templates used for rendering our views (used in the code by our route-decorated
functions) and `static/` contains the css file for styling our frontend.

Inspired by Flaskr tutorial.
