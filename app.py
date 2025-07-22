from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import db, User, Production
from datetime import datetime
import csv, io, calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_request
def before_request_func():
    if not hasattr(app, 'db_created'):
        db.create_all()
        app.db_created = True

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user = User.query.filter_by(username=uname).first()
        if user and user.check_password(pwd):
            session['user'] = uname
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if User.query.filter_by(username=uname).first():
            flash('User already exists!')
        else:
            user = User(username=uname)
            user.set_password(pwd)
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully!')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = Production(
            date=request.form['date'],
            machine_id=request.form['machine_id'],
            shift=request.form['shift'],
            department=request.form['department'],
            units=int(request.form['units']),
            uptime_hrs=float(request.form['uptime']),
            downtime=float(request.form['downtime'])
        )
        db.session.add(data)
        db.session.commit()
        flash('Data added successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add_data.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    entries = Production.query.all()
    bar_data, pie_data, line_data, uptime_data = {}, {}, {}, {}
    weekdays_total = {day: 0 for day in calendar.day_name}

    for entry in entries:
        bar_data[entry.date] = bar_data.get(entry.date, 0) + entry.units
        uptime_data[entry.date] = uptime_data.get(entry.date, 0) + entry.uptime_hrs
        pie_data[entry.department] = pie_data.get(entry.department, 0) + entry.units
        line_data[entry.date] = line_data.get(entry.date, 0) + entry.downtime
        try:
            weekday = calendar.day_name[datetime.strptime(entry.date, "%Y-%m-%d").weekday()]
            weekdays_total[weekday] += entry.units
        except:
            pass

    return render_template('dashboard.html',
        bar_labels=list(bar_data.keys()),
        bar_values=list(bar_data.values()),
        uptime_values=list(uptime_data.values()),
        pie_labels=list(pie_data.keys()),
        pie_values=list(pie_data.values()),
        line_labels=list(line_data.keys()),
        line_values=list(line_data.values()),
        summary_labels=list(weekdays_total.keys()),
        summary_values=list(weekdays_total.values())
    )

@app.route("/data")
def data_table():
    if 'user' not in session:
        return redirect(url_for('login'))
    entries = Production.query.all()
    return render_template('data_table.html', entries=entries)

@app.route("/export")
def export_csv():
    if 'user' not in session:
        return redirect(url_for('login'))
    start = request.args.get('start')
    end = request.args.get('end')
    query = Production.query
    if start and end:
        query = query.filter(Production.date >= start, Production.date <= end)
    data = query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Machine ID", "Shift", "Department", "Units", "Uptime", "Downtime"])
    for row in data:
        writer.writerow([row.date, row.machine_id, row.shift, row.department, row.units, row.uptime_hrs, row.downtime])
    output.seek(0)
    return app.response_class(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=production_data.csv"}
    )
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
