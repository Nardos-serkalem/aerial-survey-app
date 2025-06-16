from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app as app
from datetime import datetime, timedelta, time
from flask_login import login_required, current_user
from models import FlightData, FlightEntry
from extensions import db
from sqlalchemy.orm import joinedload

views = Blueprint('views', __name__)

def safe_strftime(value, format_str='%H:%M'):
    try:
        if not value or value == '' or value == 'N/A':
            return 'N/A'
        if isinstance(value, str):
            if ':' in value:
                try:
                    parsed = datetime.strptime(value, '%H:%M').time()
                    return parsed.strftime(format_str)
                except:
                    return 'N/A'
            return value
        if isinstance(value, (datetime, time)):
            return value.strftime(format_str)
        if isinstance(value, timedelta):
            hours, remainder = divmod(value.seconds, 3600)
            minutes = remainder // 60
            return f"{hours:02d}:{minutes:02d}"
        return 'N/A'
    except Exception as e:
        print(f"safe_strftime error: {str(e)}")
        return 'N/A'

def parse_time(value):
    try:
        if not value or value.strip() == '':
            return None
        return datetime.strptime(value.strip(), '%H:%M').time()
    except Exception:
        return None

def calculate_time_diff(start, end):
    try:
        if not start or not end:
            return "N/A"
        if isinstance(start, str):
            start = parse_time(start)
        if isinstance(end, str):
            end = parse_time(end)
        if not start or not end:
            return "N/A"
        start_dt = datetime.combine(datetime.today(), start)
        end_dt = datetime.combine(datetime.today(), end)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        delta = end_dt - start_dt
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02d}:{minutes:02d}"
    except Exception as e:
        print(f"Time diff error: {e}")
        return "N/A"

@views.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return redirect(url_for('auth.login'))

@views.route('/dashboard')
@login_required
def dashboard():
    try:
        flights = FlightData.query.options(joinedload(FlightData.entries)) \
                                  .order_by(FlightData.flight_date.desc(), FlightData.id.desc()).all()

        flights_data = []
        for flight in flights:
            f = {
                'project_name': flight.project_name,
                'flight_No_Day': flight.flight_No_Day,
                'pilot': flight.pilot,
                'Operators': flight.Operators,
                'departure': flight.departure,
                'overlap': flight.overlap,
                'gsd': flight.gsd,
                'aircraft': flight.aircraft,
                'navigation_system': flight.navigation_system,
                'mount': flight.mount,
                'imu': flight.imu,
                'camera': flight.camera,
                'serial_no': flight.serial_no,
                'focal_length': flight.focal_length,
                'sun_angle': flight.sun_angle,
                'internal_pos_data_code': flight.internal_pos_data_code,
                'aperture': flight.aperture,
                'shutter_speed': flight.shutter_speed,
                'iso': flight.iso,
                'fmc': flight.fmc,
                'ibd': flight.ibd,
                'weather': flight.weather,
                'remarks': flight.remarks,
                'signature': flight.signature,
                'flight_date': flight.flight_date.strftime('%Y-%m-%d') if flight.flight_date else 'N/A',
                'gps_data_logging_time': safe_strftime(flight.gps_data_logging_time),
                'engine_start': safe_strftime(flight.engine_start),
                'start_movement': safe_strftime(flight.start_movement),
                'take_off': safe_strftime(flight.take_off),
                'landing': safe_strftime(flight.landing),
                'stop_movement': safe_strftime(flight.stop_movement),
                'shutdown': safe_strftime(flight.shutdown),
                'start_stop_movement': calculate_time_diff(flight.start_movement, flight.stop_movement),
                'takeoff_landing': calculate_time_diff(flight.take_off, flight.landing),
                'engine_start_shutdown': calculate_time_diff(flight.engine_start, flight.shutdown),
                'entries': []
            }

            for entry in flight.entries:
                e = {
                    'time_of_entry': safe_strftime(entry.time_of_entry),
                    'time_of_end': safe_strftime(entry.time_of_end),
                    'turning_time': entry.turning_time or 'N/A',
                    'run': entry.run or 'N/A',
                    'heading': entry.heading or 'N/A',
                    'dir': entry.dir or 'N/A',
                    'photo_numbers': entry.photo_numbers or 'N/A',
                    'qty': entry.qty or 'N/A',
                    'remarks_entry': entry.remarks_entry or 'N/A'
                }
                f['entries'].append(e)

            flights_data.append(f)

        return render_template('dashboard.html', flights=flights_data)
    except Exception as e:
        app.logger.error(f"Dashboard error: {str(e)}", exc_info=True)
        return "Error: Could not load flight data", 500

@views.route('/submit', methods=['POST'])
@login_required
def submit():
    try:
        form = request.form
        flight_data = FlightData(
            project_name=form.get('project_name', '').strip(),
            flight_No_Day=int(form.get('flight_No_Day')) if form.get('flight_No_Day') else None,
            Operators=form.get('Operators', '').strip(),
            pilot=form.get('pilot', '').strip(),
            flight_date=datetime.strptime(form.get('flight_date'), '%Y-%m-%d').date() if form.get('flight_date') else None,
            departure=form.get('departure', '').strip(),
            overlap=float(form.get('overlap')) if form.get('overlap') else None,
            gsd=form.get('gsd', '').strip(),
            aircraft=form.get('aircraft', '').strip(),
            navigation_system=form.get('navigation_system', '').strip(),
            mount=form.get('mount', '').strip(),
            imu=form.get('imu', '').strip(),
            camera=form.get('camera', '').strip(),
            serial_no=form.get('serial_no', '').strip(),
            focal_length=form.get('focal_length', '').strip(),
            gps_data_logging_time=parse_time(form.get('gps_data_logging_time')),
            sun_angle=form.get('sun_angle', '').strip(),
            internal_pos_data_code=form.get('internal_pos_data_code', '').strip(),
            aperture=form.get('aperture', '').strip(),
            shutter_speed=form.get('shutter_speed', '').strip(),
            iso=form.get('iso', '').strip(),
            fmc=form.get('fmc', '').strip(),
            ibd=form.get('ibd', '').strip(),
            engine_start=parse_time(form.get('engine_start')),
            start_movement=parse_time(form.get('start_movement')),
            take_off=parse_time(form.get('take_off')),
            landing=parse_time(form.get('landing')),
            stop_movement=parse_time(form.get('stop_movement')),
            shutdown=parse_time(form.get('shutdown')),
            weather=form.get('weather', '').strip(),
            remarks=form.get('remarks', '').strip(),
            signature=form.get('signature', '').strip()
        )

        db.session.add(flight_data)
        db.session.flush()

        entries = zip(
            form.getlist('time_of_entry[]'),
            form.getlist('time_of_end[]'),
            form.getlist('turning_time[]'),
            form.getlist('run[]'),
            form.getlist('heading[]'),
            form.getlist('dir[]'),
            form.getlist('photo_numbers[]'),
            form.getlist('qty[]'),
            form.getlist('remarks_entry[]')
        )

        for entry in entries:
            if not any(field.strip() for field in entry if field):
                continue
            flight_entry = FlightEntry(
                flight_data_id=flight_data.id,
                time_of_entry=parse_time(entry[0]),
                time_of_end=parse_time(entry[1]),
                turning_time=int(entry[2]) if entry[2] else None,
                run=int(entry[3]) if entry[3] else None,
                heading=int(entry[4]) if entry[4] else None,
                dir=entry[5].strip() if entry[5] else None,
                photo_numbers=entry[6].strip() if entry[6] else None,
                qty=int(entry[7]) if entry[7] else None,
                remarks_entry=entry[8].strip() if entry[8] else None
            )
            db.session.add(flight_entry)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Flight data submitted successfully!'})

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Submission error: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@views.route('/index')
@login_required
def index():
    return render_template('index.html')

@views.route('/home')
@login_required
def home():
    return render_template('home.html')
