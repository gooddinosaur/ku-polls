# Installation Instructions
To set up the project, follow these steps:
1. **Clone the repository**
   ```
   git clone https://github.com/gooddinosaur/ku-polls.git
   ```
2. **Change directory into the repository**
   ```
   cd ku-polls
   ```
3. **Create a virtual environment**
   ```
   python -m venv venv
   ```
4. **Activate the virtual environment**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. **Install required packages**
  ```
  pip install -r requirements.txt
  ```
6. **Set env variables**
   - On Windows:
     ```
     copy sample.env .env
     ```
   - On macOS/Linux:
     ```
     cp sample.env .env
     ```
Note: After copying, ensure that you update the .env file with any environment-specific values as necessary.
7. **Create migrations for any changes in the models**
  ```
  python manage.py makemigrations
  ```
8. **Run migrations to apply changes to the database**
  ```
  python manage.py migrate
  ```
9. **Run tests**
  ```
  python manage.py test
  ```
10. **Load data**
  ```
  python manage.py loaddata data/<filename>
  ```
  ```
  python manage.py loaddata data/users.json
  python manage.py loaddata data/polls-v4.json
  python manage.py loaddata data/votes-v4.json
  ```
11. **Start the server**
  ```
  python manage.py runserver
  ```
12. **Access the application** at [http://localhost:8000/](http://localhost:8000/)