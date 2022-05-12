import sqlite3
import json
from flask import Flask
from flask import render_template, request, redirect, url_for
import requests
import datetime
import logging

app = Flask(__name__)
route = r"C:\Users\Chapa\Desktop\DevOps\FlightsProjDB.db"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: - > %(levelname)s - > %(message)s', filename='../venv/main.log')


@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/signup')  # signup
def user_signup():
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def user_login(i=any):
    user = request.args.to_dict()
    login_info = {}
    try:
        conn = sqlite3.connect(route)
        x = conn.execute(
            f"SELECT * FROM Users WHERE full_name = \"{user.get('full_name')}\" AND password = \"{user.get('password')}\" AND real_id = \"{user.get('real_id')}\"")
        if x != None:
            login_info = {'id_AI': i[0], 'full_name': i[1], 'password': i[2], 'real_id': i[3]}
            return redirect('main')
            conn.close()
    except Exception:
        return render_template('login.html')


@app.route('/main', methods=['GET', 'POST'])  # page after log in / sign up
def main_page():
    # users_lst = []
    # conn = sqlite3.connect(route)
    # x = conn.execute("SELECT * FROM Users")
    # for i in x:
    #    user = {'id_AI': i[0], 'full_name': i[1], 'password': i[2], 'real_id': i[3]}
    #    users_lst.append(user)
    # for user in users_lst:
    #    if request.form['real_id'] == user.get('real_id'):
    #        lst_of_tickets = []
    #        tickets = conn.execute(f"SELECT * FROM Tickets WHERE user_id ={user.get('id_AI')}")
    #        for i in tickets:
    #            ticket= {'ticket_id': i[0], 'user_id': i[1], 'flight_id': i[2]}
    #            lst_of_tickets.append(ticket)
    #            conn.close()
    #        #     logging.debug(f'Getting user  by ID')
    #            return f'{lst_of_tickets}'
    conn = sqlite3.connect(route)
    x = conn.execute(f"SELECT * FROM Users")
    if request.method == 'POST':
        for i in x:
            user = {'id_AI': i[0], 'full_name': i[1], 'password': i[2], 'real_id': i[3]}
            username = i[1]
            password = i[2]
        print(username, password)
        u1 = request.form['full_name']
        p1 = request.form['password']
        if u1 == username and p1 == password:
            return 'hello'
    conn.close()


# *  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
# USERS_FUNCTIONS START


@app.route('/users', methods=['GET'])
def get_users():
    users_lst = []
    conn = sqlite3.connect(route)
    x = conn.execute("SELECT * FROM Users")
    for i in x:
        user = {'id_AI': i[0], 'full_name': i[1], 'password': i[2], 'real_id': i[3]}
        users_lst.append(user)
    conn.close()
    logging.debug('Getting all users')
    return json.dumps(users_lst)


@app.route('/users/<int:id>')
def get_user_by_id(id):
    try:
        conn = sqlite3.connect(route)
        x = conn.execute(f"SELECT * FROM Users WHERE id_AI ={id}")
        for i in x:
            user = {'id_AI': i[0], 'full_name': i[1], 'password': i[2], 'real_id': i[3]}
        conn.close()
        logging.debug(f'Getting user {id} by ID')
        return user
    except Exception:
        return f'User not found', 404


@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = request.get_json()  # POSTMAN
        if not validate_user_post(user):
            return 'bad input', 400
        conn = sqlite3.connect(route)
        conn.execute(f"INSERT INTO Users (full_name, password, real_id) \
        VALUES (\"{user['full_name']}\",\"{user['password']}\",\"{user['real_id']}\")")
        conn.commit()
        conn.close()
        logging.debug('Posted new user')
        return 'Posted new user'
    except:
        user = request.form.to_dict()  # SIGN UP FORM
        if not validate_user_post(user):
            return 'bad input', 400
        conn = sqlite3.connect(route)
        insert_user_query = f"INSERT INTO Users (full_name, password, real_id) \
                VALUES (\"{user['full_name']}\",\"{user['password']}\",\"{user['real_id']}\")"
        conn.execute('INSERT INTO Users (full_name, password, real_id) VALUES ("vered vered","123456Bb","123")')
        conn.commit()
        conn.close()
        logging.debug('Posted new user')
        return 'Posted new user'
    else:
        return 'Could not post user'
        logging.debug(f"Could not post user")


def validate_user_post(user_input):
    if user_input.get('full_name') and user_input.get('password') and user_input.get('real_id'):
        return True
    return False


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        update_user = request.get_json()
        update_statement = ''
        if update_user.get('password'):
            update_statement += f"password = \"{update_user.get('password')}\""
        if update_user.get('full_name'):
            if update_statement != "":
                update_statement += f",full_name = \"{update_user.get('full_name')}\""  # note the comma
            else:
                update_statement = f"full_name = \"{update_user.get('full_name')}\""
        if update_user != None:
            conn = sqlite3.connect(route)
            conn.execute(f"UPDATE Users SET {update_statement} WHERE id_AI = {id}")
            conn.commit()
            conn.close()
        logging.debug(f"User {id} info updated")
        return f"User {id} info updated"
    except Exception:
        return f"Could not update user {id} info"


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user_by_id(id):
    try:
        conn = sqlite3.connect(route)
        x = conn.execute(f"DELETE FROM Users WHERE id_AI ={id}")
        conn.commit()
        conn.close()
        logging.debug(f"User {id} deleted")
        return 'User deleted'
    except Exception:
        return f'Failed to delete user', 400


# USERS_FUNCTIONS END
# *  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
# *  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
# FLIGHTS_FUNCTIONS START


@app.route('/flights', methods=['GET'])
def get_flights():
    flights_lst = []
    conn = sqlite3.connect(route)
    x = conn.execute("SELECT * FROM Flights")
    for i in x:
        flight = {'flight_id': i[0], 'remaining_seats': i[1], 'origin_country_id': i[2], 'dest_country_id': i[3],
                  'timestamp': i[4]}
        flights_lst.append(flight)
    conn.close()
    logging.debug('Getting all flights')
    return f"{flights_lst}"


@app.route('/flights/<int:id>')
def get_flight_by_id(id):
    try:
        conn = sqlite3.connect(route)
        x = conn.execute(f"SELECT * FROM Flights WHERE flight_id ={id}")
        for i in x:
            flight = {'flight_id': i[0], 'remaining_seats': i[1], 'origin_country_id': i[2], 'dest_country_id': i[3],
                      'timestamp': i[4]}
        conn.close()
        logging.debug(f'Getting flight {id} by ID')
        return flight
    except Exception:
        return f'Flight not found', 404


@app.route('/flights', methods=['POST'])
def create_flight():
    try:
        flight = request.get_json()
        if not validate_flight_post(flight):
            return 'bad input', 400
        conn = sqlite3.connect(route)
        conn.execute(f"INSERT INTO Flights (remaining_seats, origin_country_id, dest_country_id, timestamp) \
        VALUES ({flight['remaining_seats']},{flight['origin_country_id']},{flight['dest_country_id']}, \"{datetime.datetime.now()}\")")
        conn.commit()
        conn.close()
        logging.debug('Posted new flight')
        return json.dumps(flight)
    except Exception as error:
        print(error)
        return f"Could not post flight"


def validate_flight_post(flight_input):
    if flight_input.get('remaining_seats') and flight_input.get('origin_country_id') and flight_input.get(
            'dest_country_id'):
        return True
    return False


@app.route('/flights/<int:id>', methods=['PUT'])
def update_flight(id):
    try:
        update_flight = request.get_json()
        update_statement = ''
        if update_flight.get('origin_country_id'):
            update_statement += f"origin_country_id = {update_flight.get('origin_country_id')}"
        if update_flight.get('remaining_seats'):
            if update_statement != "":
                update_statement += f",remaining_seats = {update_flight.get('remaining_seats')}"  # note the comma
            else:
                update_statement = f"remaining_seats = {update_flight.get('remaining_seats')}"
        if update_flight.get('dest_country_id'):
            if update_statement != "":
                update_statement += f",dest_country_id = {update_flight.get('dest_country_id')}"  # note the comma
            else:
                update_statement = f"dest_country_id = {update_flight.get('dest_country_id')}"
        if update_flight != None:
            conn = sqlite3.connect(route)
            conn.execute(f"UPDATE Flights SET {update_statement} WHERE flight_id = {id}")
            conn.commit()
            conn.close()
            logging.debug(f"Flight {id} info updated")
        return f"Flight {id} info updated"
    except Exception:
        return f"Could not update flight {id}"


@app.route('/flights/<int:id>', methods=['DELETE'])
def delete_flight_by_id(id):
    try:
        conn = sqlite3.connect(route)
        x = conn.execute(f"DELETE FROM Flights WHERE flight_id ={id}")
        conn.commit()
        conn.close()
        logging.debug(f"Flight {id} deleted")
        return 'Flight deleted'
    except Exception:
        return f'Failed to delete flight', 400


# FLIGHTS_FUNCTIONS END
# *  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
# *  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
# TICKETS_FUNCTIONS START


@app.route('/tickets', methods=['GET'])
def get_tickets():
    tickets_lst = []
    conn = sqlite3.connect(route)
    x = conn.execute("SELECT * FROM Tickets")
    for i in x:
        ticket = {'ticket_id': i[0], 'user_id': i[1], 'flight_id': i[2]}
        tickets_lst.append(ticket)
    conn.close()
    logging.debug('Getting all tickets')
    return json.dumps(tickets_lst)


@app.route('/tickets/<int:id>')
def get_ticket_by_id(id):
    try:
        conn = sqlite3.connect(route)
        x = conn.execute(f"SELECT * FROM Tickets WHERE ticket_id ={id}")
        for i in x:
            ticket = {'ticket_id': i[0], 'user_id': i[1], 'flight_id': i[2]}
        conn.close()
        logging.debug(f'Getting ticket {id} by ID')
        return ticket
    except Exception:
        return f'ticket not found', 404


@app.route('/tickets', methods=['POST'])
def create_ticket():
    try:
        ticket = request.get_json()
        if not validate_ticket_post(ticket):
            return 'bad input', 400
        conn = sqlite3.connect(route)
        conn.execute(f"INSERT INTO Tickets (user_id, flight_id) VALUES ({ticket['user_id']}, {ticket['flight_id']})")
        # seats = conn.execute(f'Select remaining_seats from Flights where flight_id = {ticket["flight_id"]}')
        # conn.execute( f'UPDATE Flights set remaining_seats = {seats - 1} WHERE flight_id = {ticket["flight_id"]}')  # Could not execute
        conn.commit()
        conn.close()
        logging.debug('Posted new ticket')
        return json.dumps(ticket)
    except Exception:
        return f"Could not post ticket"


def validate_ticket_post(ticket_input):
    if ticket_input.get('user_id') and ticket_input.get('flight_id'):
        return True
    return False


@app.route('/tickets/<int:id>', methods=['DELETE'])
def delete_ticket_by_id(id):
    try:
        ticket = request.get_json()
        conn = sqlite3.connect(route)
        x = conn.execute(f"DELETE FROM Tickets WHERE ticket_id ={id}")
        # seats = conn.execute(f'Select remaining_seats from Flights where flight_id = {ticket["flight_id"]}')
        # conn.execute( f'UPDATE Flights set remaining_seats ={seats + 1} WHERE flight_id = {ticket["flight_id"]}')  # Could not execute
        conn.commit()
        conn.close()
        logging.debug(f"ticket {id} deleted")
        return 'ticket deleted'
    except Exception:
        return f'Failed to delete ticket', 400


# TICKETS_FUNCTIONS END
# *  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
# COUNTRIES_FUNCTIONS START


@app.route('/countries', methods=['GET'])
def get_countries():
    countries_lst = []
    conn = sqlite3.connect(route)
    x = conn.execute("SELECT * FROM Countries")
    for i in x:
        country = {'code_AI': i[0], 'name': i[1]}
        countries_lst.append(country)
    conn.close()
    logging.debug('Getting all countries')
    return json.dumps(countries_lst)


@app.route('/countries/<int:id>')
def get_country_by_id(id):
    try:
        conn = sqlite3.connect(route)
        x = conn.execute(f"SELECT * FROM Countries WHERE code_AI ={id}")
        for i in x:
            country = {'code_AI': i[0], 'name': i[1]}
        conn.close()
        logging.debug(f'Getting country {id} by ID')
        return country
    except Exception:
        return f'Country not found', 404


@app.route('/countries', methods=['POST'])
def create_country():
    try:
        country = request.get_json()
        if not validate_country_post(country):
            return 'bad input', 400
        conn = sqlite3.connect(route)
        conn.execute(f"INSERT INTO Countries (name) \
        VALUES (\"{country['name']}\")")
        conn.commit()
        conn.close()
        logging.debug('Posted new country')
        return json.dumps(country)
    except Exception:
        return f"Could not post country"


def validate_country_post(country_input):
    if country_input.get('name'):
        return True
    return False


@app.route('/countries/<int:id>', methods=['DELETE'])
def delete_country_by_id(id):
    try:
        conn = sqlite3.connect(route)
        x = conn.execute(f"DELETE FROM Countries WHERE code_AI ={id}")
        conn.commit()
        conn.close()
        logging.debug(f"Country {id} deleted")
        return f"Country {id} deleted"
    except Exception:
        return f'Failed to delete country {id}', 400


# COUNTRIES_FUNCTIONS END
# *  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

app.run()
