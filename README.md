# Jobs Parser
![Generic badge](https://img.shields.io/badge/version-1.0.0-green.svg) ![Generic badge](https://img.shields.io/badge/python-3.8-blue.svg) ![Generic badge](https://img.shields.io/badge/coverage-85%25-green.svg) 

 - Jobs Parser that search job vacancies by a keyword (e.g python).
 - Check all pages
 - Count words "python", "linux", "flask" mentioned on each vacancy page
 - Calculate average number of occurrence each word found

## Features:
 - Uses cash.

## Installing
**Python 3.8 or higher is required**


````
# Linux
git clone https://github.com/Gliger13/jobs_parser.git
cd jobs_parser
python setup.py install
````

## How to run
Simple application that check first __**3**__ pages of 'https://rabota.by/search/vacancy?text=Python' and print:
 - average number of occurrence of words 'python', 'linux', 'flask'
 - number of occurrence of words 'python', 'linux', 'flask'
````
# Linux
python jobs_parser/app.py
````

## Author

Made by Andrei Zaneuski (@Gliger13), Belarus, Minsk as Task
