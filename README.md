# deep-code-bench

Each instructions section below will assume you are starting in the repo root.

# Framework Installation

- Create the venv: `python3 -m venv venv`
- Activate the venv: `source venv/bin/activate`
- Install the python package:
    - `cd framework`
    - `pip install -e .`

# Activate the Environment

`source venv/bin/activate`

Always do this in the repo root before running any python scripts.

# Project Setup

## Project directory

`python framework/scripts/init_project_dir.py --project-dir projects/your_project`

## Project config

- Edit the settings in `projects/your_project/config/settings.yaml`
- Create project in firebase and add a web app. If you don't know how to do this, ask ChatGPT.
- Get your firebase credentials from the firebase console (Project Settings -> General -> Scroll Down)
- Edit the firebase credentials in `projects/your_project/config/firebase_credentials.yaml`

## Project init

- `python framework/scripts/init_firebase_react_app.py --project-dir projects/your_project`
- `cd projects/your_project/app`
- `npm install`

# Run the App

- `cd projects/your_project/app`
- `npm start`

# Deploy the App

- `cd projects/your_project/app`
- `firebase login` (if not already logged-in)
- `firebase deploy`