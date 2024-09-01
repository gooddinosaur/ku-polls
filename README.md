## KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installation
1. Clone this repository.
   ```
   git clone https://github.com/gooddinosaur/ku-polls.git
   ```
2. Change directory into this repository.
   ```
   cd ku-polls
   ```
3. Create a virtual environment
   ```
   python -m venv venv
   ```
4. Activate the virtual environment
   ```
   venv/Scripts/activate
   ```
5. Install required packages.
   ```
   pip install -r requirements.txt
   ```
6. Run the migration.
   ```
   python manage.py migrate
   ```
7. Loading the data
   ```
   python manage.py loaddata data/<filename>
   ```
8. Start the server
   ```
   python manage.py runserver
   ```

## Running the Application
1. Start the server
   ```
   python manage.py runserver
   ```
2. Access the link : http://localhost:8000/

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20and%20Scope)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)
- [Iteration 2 Plan](../../wiki/Iteration%202%20Plan)
