@echo off

set original_path=%cd%

cd..

set root_path=%cd%

call %root_path%\venv\Scripts\activate.bat

@REM make messages for all languages
echo making messages for all languages...
py manage.py makemessages -l en --ignore=venv/*
py manage.py makemessages -l fi --ignore=venv/*
py manage.py makemessages -l sv --ignore=venv/*
py manage.py makemessages -l ru --ignore=venv/*

@REM compile messages
echo compiling messages...
py manage.py compilemessages --ignore=venv/*

echo done

echo closing in 10 seconds...
timeout 10