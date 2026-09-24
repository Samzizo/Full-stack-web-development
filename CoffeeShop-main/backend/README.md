# Full Stack Coffe Shop Project

This application is a drink menu , through which it is possible to discover what the cafe offers of drinks

The task for the project was to create an API and Auth suite for implementing the following functionality:

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

##### The application must:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing dring

## Getting Started

### Installing Dependencies :ok_hand:

Developers using this project should already have:

1. [python3](https://www.python.org/downloads/) and:
   - [Flask](http://flask.pocoo.org/): 
   is a lightweight backend microservices framework. Flask is required to handle requests and responses.
   - [SQLAlchemy](https://www.sqlalchemy.org/):
   is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
   - [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.
2. pip
3. node
4. npm installed
5. ionic


### Backend Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:

```bash

pip install -r requirements.txt

```
## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

Base URL: Currently this application is hosted locally. The backend is hosted at `http://127.0.0.1:5000/`

### Frontend

This frentend use **ionic**
It watches for changes in your source files and automatically reloads with the updated build. By default, ionic serve boots up a development server on all network interfaces and prints the external address(es) on which your app is being served. It also broadcasts your app to the Ionic DevApp on your network.

Install ionic with the commands bellow:

```npm install -g cordova
npm install -g ionic
npm install -g @angular/cli
npm install --save-dev @angular-devkit/build-angular
```
Run your frontend with these commands:

```ionic repair
ionic serve
```
The frontend is hosted at `http://127.0.0.1:8100/`

### Postman tests

- `get:drinks`:
```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "red",
                    "parts": 1
                }
            ],
            "title": "black coffee"
        },
        {
            "id": 5,
            "recipe": [
                {
                    "color": "#744d25",
                    "parts": 1
                }
            ],
            "title": "Nescafe"
        },
        {
            "id": 6,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        },
        {
            "id": 7,
            "recipe": [
                {
                    "color": "#ffffe6",
                    "parts": 1
                },
                {
                    "color": "#c68c53",
                    "parts": 1
                },
                {
                    "color": "#4d3319",
                    "parts": 1
                }
            ],
            "title": "capuccino"
        },
        {
            "id": 8,
            "recipe": [
                {
                    "color": "#ffb84d",
                    "parts": 1
                },
                {
                    "color": "#ff9900",
                    "parts": 1
                }
            ],
            "title": "orange jus"
        },
        {
            "id": 9,
            "recipe": [
                {
                    "color": "#ffff99",
                    "parts": 1
                },
                {
                    "color": "#dfff80",
                    "parts": 1
                },
                {
                    "color": "#d2ff4d",
                    "parts": 1
                }
            ],
            "title": "Lemon"
        },
        {
            "id": 10,
            "recipe": [
                {
                    "color": "#1a0f00",
                    "parts": 1
                }
            ],
            "title": "double expresso"
        }
    ],
    "success": true
}
```
**Manager**
`get:drinks-detail`: status 200
    
```  {
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "red",
                    "name": "beans",
                    "parts": 1
                }
            ],
            "title": "black coffee"
        },
        {
            "id": 3,
            "recipe": [
                {
                    "color": "black",
                    "name": "only beans",
                    "parts": 3
                }
            ],
            "title": "double expresso"
        },
        {
            "id": 5,
            "recipe": [
                {
                    "color": "#744d25",
                    "name": "coffe",
                    "parts": 1
                }
            ],
            "title": "Nescafe"
        },
        {
            "id": 6,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        },
        {
            "id": 7,
            "recipe": [
                {
                    "color": "#ffffe6",
                    "name": "milk",
                    "parts": 1
                },
                {
                    "color": "#c68c53",
                    "name": "cacao",
                    "parts": 1
                },
                {
                    "color": "#4d3319",
                    "name": "coffee",
                    "parts": 1
                }
            ],
            "title": "capuccino"
        },
        {
            "id": 8,
            "recipe": [
                {
                    "color": "#ffb84d",
                    "name": "water",
                    "parts": 1
                },
                {
                    "color": "#ff9900",
                    "name": "orange",
                    "parts": 1
                }
            ],
            "title": "orange jus"
        },
        {
            "id": 9,
            "recipe": [
                {
                    "color": "#ffff99",
                    "name": "jus",
                    "parts": 1
                },
                {
                    "color": "#dfff80",
                    "name": "",
                    "parts": 1
                },
                {
                    "color": "#d2ff4d",
                    "name": "",
                    "parts": 1
                }
            ],
            "title": "Lemon"
        }
    ],
    "success": true
}
```

`post:drinks`: status 200

``` {
    "drinks": {
        "id": 9,
        "recipe": {
            "color": "blue",
            "name": "Water",
            "parts": 1
        },
        "title": "Water3"
    },
    "success": true
}
```
`patch:drinks`: status 200
```{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "green",
                    "name": "milk and beans",
                    "parts": 2
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}
```
`delete:drinks`: status 200
```
{
    "delete": 1,
    "success": true
}
```

**Brista**
    - `get:drinks-detail`: status 200
    - `post:drinks`: status 401 UNAUTHORIZED
    - `patch:drinks`: status 401 UNAUTHORIZED
    - `delete:drinks`: status 401 UNAUTHORIZED

## Authors

**Odai Alsalieti** :blush: authored the API **(auth.py)**, test suite **(api.py)**, and this **README**.
All other project files, including the models and frontend, were created by **Udacity** as a project template for the **Full Stack Web Developer Nanodegree**.
