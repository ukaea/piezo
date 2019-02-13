#!~/piezo_web_app/venv/bin/python
python -m pytest --cov-config=.coveragerc --cov-report html --cov-report term --cov=PiezoWebApp/src PiezoWebApp/tests/
