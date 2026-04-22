# Back-end App - OpenClassrooms Project 12
**Develop a secured back-end architecture with Python and SQL**

---

## DESCRIPTION
### (Work In Progress)

This project was completed as part of the "Python Developer" path at OpenClassrooms.

The goal was to develop a secured back-end architecture, capable of:

- 

The application must:

-

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
- 
- Finally, launch the app : ``

### Launching the APP
- 

---

## EXPLANATIONS OF WHAT THE APP DOES

### <u></u>
- 

### <u></u>
- 

### <u></u>
- 

### <u></u>
- 

---

## TEMPLATES EXAMPLES

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
    <img src="docs/cov_report_functions.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- **Type the lines below in the terminal to generate another coverage report with pytest**

    `python -m coverage run -m unittest`
    `python -m coverage html --omit=tests/*`

---

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## AUTHOR
**Name**: Nicolas MARIE  
**Track**: Python Developer – OpenClassrooms  
**Project 12 – Develop a secured back-end architecture with Python and SQL – April 2026**
