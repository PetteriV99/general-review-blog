# Geneal Review Blog <br>
General review blog is a web application that offers its users the ability to rate and discuss all kinds of things.
To join, you must first register an user and we will send you a confirmation via email. 
After confirming your account you can start by creating more reviews or commenting on
reviews made by other people.

### How it was made
General review blog was made using Flask and Python.
Programs that were used: PyCharm, VS Code, PgAdmin and Postman.


### Developer instructions: <br>
1. Make new database with PgAdmin <br>
2. Assign user for database <br>
3. In config.py Change SQLALCHEMY_DATABASE_URI username and password <br>
4. Write in terminal: <br>
      flask db init <br>
      flask db migrate <br>
      flask db upgrade <br>
5. Add virtual environment variables for MAILGUN_DOMAIN and MAILGUN_API_KEY (resources/user) <br>
6. Run app.py <br>

