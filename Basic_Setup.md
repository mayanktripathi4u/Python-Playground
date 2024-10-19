# Basic Setup for Flask App
## Steps to Creating Application:
1. Create Project Folder
    1.1 Open Project Folder in Visual Studio Code
2. Setup Python Virtual Environment
    I am using generic virtual env. created my self at GitHub Repo root level.
```bash
cd /Users/<MACHINE_NAME>/Desktop/Apps/GitHub_Repo/

python3 -m venv .venv
source .venv/bin/activate
```
3. Install Flask
```bash
pip install pandas numpy 
pip install Flask
pip install Flask-RESTful
pip install Flask-WTF
pip install flask-mysql
pip install SQLAlchemy
pip install seaborn
pip install flask_mysqldb
pip install bcrypt

#pip install --upgrade Flask-SQLAlchemy SQLAlchemy


pip freeze > requirements.txt
```
4. Install Dependencies
    4.1 Set environment variables
5. Create Flask Entry File
    5.1 Import flask
    5.2 Define flask object
6. Create Routes
7. Run Flask Application