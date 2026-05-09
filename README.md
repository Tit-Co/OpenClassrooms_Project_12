# Back-end App - OpenClassrooms Project 12
**Develop a secured back-end architecture with Python and SQL**

---

## DESCRIPTION
### (Work In Progress)

This project was completed as part of the "Python Developer" path at OpenClassrooms.

The goal was to develop a secured back-end architecture, capable of:

- storing data in SQL database
- realizing CRUD operations on all the differents objects : Contract, Client, Event and Collaborator
- communicating with the user by CLI interface
- providing permission according to the user role

The application must:

- allow the user to create, update, delete, display and filter objects according to his permission

---

## PROJECT STRUCTURE
<p align="center">
    <img src="docs/structure.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

---

## INSTALLATION

- ### Clone the repository :

```
git clone https://github.com/Tit-Co/OpenClassrooms_Project_12.git
```

- ### Navigate into the project directory :
    `cd OpenClassrooms_Project_12`

- ### Create a virtual environment and dependencies :

1. #### With [uv](https://docs.astral.sh/uv/)

    `uv` is an environment and dependencies manager.
    
    - #### Install environment and dependencies
    
    `uv sync`

2. #### With pip

   - #### Install the virtual env :

    `python -m venv env`

   - #### Activate the virtual env :
    `source env/bin/activate`  
    Or  
    `env\Scripts\activate` on Windows  

3. #### With [Poetry](https://python-poetry.org/docs/)

    `Poetry` is a tool for dependency management and packaging in Python.
    
    - #### Install the virtual env :
    `py -3.14 -m venv env`
    
    - #### Activate the virtual env :
    `poetry env activate`

- ### Install dependencies 
  1. #### With [uv](https://docs.astral.sh/uv/)
      `uv sync` or `uv pip install -r requirements.txt`

  2. #### With pip
      `pip install -r requirements.txt` 

  3. #### With [Poetry](https://python-poetry.org/docs/)
      `poetry install`
  
     (NB : Poetry and uv will read the `pyproject.toml` file to know which dependencies to install)

---

## USAGE

### Launching server
- Open a terminal
- Go to project folder - example : `cd epic_events`
- Activate the virtual environment as described previously
- Create environment variables (to avoid to add raw DB details in the code)
  - With Power Shell :
    ```
    $env:DB_USERNAME = "epic_events_user"
    $env:DB_PASSWORD = "tgl_Prn_C1"
    $env:DATABASE = "epic_events"
    $env:HOST = "127.0.0.1"
    $env:PORT = "3307"
    ```
  - With Git Bash :
    ```
    export DB_USERNAME="epic_events_user"
    export DB_PASSWORD="tgl_Prn_C1"
    export DATABASE="epic_events"
    export HOST="127.0.0.1"
    export PORT="3307"
    ```

### Launching the APP
- Finally, launch the CLI app by typing commands : 
  - Examples
    - `python -m src.cli.main login`
    - `python -m src.cli.main collaborator create-collaborator`
    - `python -m src.cli.main event display-event`
    - `python -m src.cli.main client filter-client`
    - `python -m src.cli.main contract delete-contract`

---

## EXPLANATIONS OF WHAT THE APP DOES

### <u>Initialization</u>
- First the database is initialized and an admin manager is created. Only this first account can create the first collaborators.

### <u>Authentication</u>
- The user can log in the CLI by typing his e-mail and password

### <u>Creation</u>
- The user can create objects (Contract, Client, Event, Collaborator) by typing the proper command and according to his permission.
- Only managers can create some new collaborators and some new contracts.
- Only commercials can create some new clients or some new events.

### <u>Display</u>
- All user can display objects of any type.

### <u>Update</u>
- The user can update objects (Contract, Client, Event, Collaborator) by typing the proper command and according to his permission.
- Only technicians can update events.
- Only commercials can update clients.
- Only managers can update contracts and collaborators details

### <u>Deletion</u>
- The user can delete objects (Contract, Client, Event, Collaborator) by typing the proper command and according to his permission.
- Only managers can delete contracts, events and collaborators profile.
- Only commercials can delete clients.

### <u>Filtering</u>
- The user can filter objects (Contract, Client, Event, Collaborator) by typing the proper command and according to his permission.
- Only managers and technicians can filter events.
- Only commercials can filter contracts.
- All users can filter clients.

---

## CLI VIEWS EXAMPLES

- 
<p align="center">
    <img src="docs/screenshots/registration_screenshot.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

---

## PEP 8 CONVENTIONS

- Flake 8 report
<p align="center">
    <img src="docs/flake8_report.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

**Type the line below in the terminal to generate another report with [flake8-html](https://pypi.org/project/flake8-html/) tool :**

` flake8 --format=html --htmldir=flake8-report --max-line-length=119 --extend-exclude=env/`

---

## TESTS COVERAGE WITH UNITTEST

- Coverage report
<p align="center">
    <img src="docs/cov_report.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- **Type the lines below in the terminal to generate another coverage report with pytest**

    `python -m coverage run -m unittest discover -s src/tests`
    `python -m coverage html --omit=tests/*`

---

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## AUTHOR
**Name**: Nicolas MARIE  
**Track**: Python Developer – OpenClassrooms  
**Project 12 – Develop a secured back-end architecture with Python and SQL – April 2026**
