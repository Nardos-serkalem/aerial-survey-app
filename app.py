from flask import Flask, send_from_directory
from config import Config
from extensions import db, socketio, login_manager
from routes import views
from auth import auth as auth_blueprint
from models import User, FlightData
import os
from flask_socketio import emit
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

@app.template_filter('to_datetime')
def to_datetime_filter(value, fmt='%H:%M'):
    if isinstance(value, str):
        try:
            return datetime.strptime(value.strip(), fmt)
        except:
            return None
    return value
db.init_app(app)
socketio.init_app(app, cors_allowed_origins="*")
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app.register_blueprint(views)
app.register_blueprint(auth_blueprint)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

with app.app_context():
    db.create_all()

#SocketiO logic
@socketio.on('submit_data')
def handle_submit_data(data):
    try:
        flight_no_day = data.get('flight_No_Day')
        project_name = data.get('project_name')
        operators = data.get('Operators')
        pilot = data.get('pilot')
        flight_date_str = data.get('flight_date')
        departure = data.get('departure')

        flight_date = datetime.strptime(flight_date_str, '%Y-%m-%d').date() if flight_date_str else None

        flight = FlightData(
            project_name=project_name,
            flight_No_Day=flight_no_day,
            Operators=operators,
            pilot=pilot,
            flight_date=flight_date,
            departure=departure,
        )

        db.session.add(flight)
        db.session.commit()

        emit('data_received', {
            'id': flight.id,
            'project_name': flight.project_name,
            'flight_No_Day': flight.flight_No_Day,
            'Operators': flight.Operators,
            'pilot': flight.pilot,
            'flight_date': str(flight.flight_date),
            'departure': flight.departure,
        })

        emit('new_data', {
            'id': flight.id,
            'project_name': flight.project_name,
            'flight_No_Day': flight.flight_No_Day,
            'Operators': flight.Operators,
            'pilot': flight.pilot,
            'flight_date': str(flight.flight_date),
            'departure': flight.departure,
        }, broadcast=True)

    except Exception as e:
        print("Error saving flight data:", e)
        emit('error', {'message': 'Failed to save data'})

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')
@app.route('/')
def home_redirect():
    return "App is running. Visit /login or /dashboard if authenticated."
if __name__ == '__main__':
    socketio.run(app, debug=True)
