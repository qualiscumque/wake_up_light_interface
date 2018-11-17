import json
from datetime import datetime as dt

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, validators, DateTimeField, SelectMultipleField, IntegerField
from calendar import day_abbr

app = Flask(__name__)


def get_alarm_data():
    try:
        with open('alarms.json') as alarms_file:
            return json.load(alarms_file)["array"]
    except Exception:
        return []


def write_alarm_data(alarms):
    with open('alarms.json', 'w') as alarms_file:
        json.dump({"array": alarms}, alarms_file, indent=4)


#class MultiCheckboxField(SelectMultipleField):
#    """
#    A multiple-select, except displays a list of checkboxes.
#
#    Iterating the field will produce subfields, allowing custom rendering of
#    the enclosed checkbox fields.
#    """
#    widget = widgets.ListWidget(prefix_label=False)
#    option_widget = widgets.CheckboxInput()

# Alarm Form Class
class AlarmForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    time = DateTimeField('Alarm', format='%H:%M')
    days = SelectMultipleField('Weekdays', choices=list(zip(range(7), day_abbr)), coerce=int)
    action = StringField('Action', [validators.Length(min=1, max=200)])


# Index
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/toggle')
def toggle():
    import smbus
    device = smbus.SMBus(1)
    address = 50
    print("I2C: Schreiben auf Device 0x{:02X}".format(address))
    try:
        device.write_i2c_block_data(0x32, 0x00, [0x1])
    except IOError as err:
            print("Fehler beim Schreiben auf Device 0x{:02X}".format(address))
    return render_template('home.html')


@app.route('/display')
def display():
    from tm1637 import TM1637
    display = TM1637(CLK=21, DIO=20, brightness=1.0)
    display.Clear()
    digits = [1, 3, 3, 7]
    display.Show(digits)

    return render_template('home.html')


# Alarm Dashboard
@app.route('/alarm_dashboard')
def alarm_dashboard():
    alarms = get_alarm_data()

    #get names for the numbers
    for alarm in alarms:
        alarm["dnames"] = [day_abbr[int(x)] for x in alarm['days']]
        print(alarm["dnames"])

    if len(alarms) > 0:
        return render_template('alarm_dashboard.html', alarms=alarms)
    else:
        msg = 'Alarm DB not found!'
        return render_template('alarm_dashboard.html', msg=msg)

# Add Alarm
@app.route('/set_alarm', methods=['GET', 'POST'])
def set_alarm():
    form = AlarmForm(request.form)
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        time = request.form['time']
        action = request.form['action']

        alarms = get_alarm_data()

        new_id = 0
        for alarm in alarms:
            current_id = int(alarm['id'])
            if new_id <= current_id:
                new_id = current_id + 1

        new_alarm = {'id': str(new_id),
                     'title': title,
                     'alarm': time,
                     'action': action,
                     'days': form.days.data
                     }

        alarms.append(new_alarm)
        write_alarm_data(alarms)

        flash('Alarm Created', 'success')
        return redirect(url_for('alarm_dashboard'))
    return render_template('edit_alarm.html', form=form)


# Edit Alarm
@app.route('/edit_alarm/<string:id>', methods=['GET', 'POST'])
def edit_alarm(id):
    alarms = get_alarm_data()

    selected_alarm = None
    for alarm in alarms:
        if alarm['id'] == id:
            selected_alarm = alarm
            break
    else:
        flash('Alarm ID not found!', 'error')
        return redirect(url_for('alarm_dashboard'))

    # Get form
    form = AlarmForm(request.form)

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        time = request.form['time']
        action = request.form['action']

        selected_alarm['title'] = title
        selected_alarm['alarm'] = time
        selected_alarm['days'] = form.days.data
        selected_alarm['action'] = action

        write_alarm_data(alarms)

        flash('Alarm Updated', 'success')
        return redirect(url_for('alarm_dashboard'))
    else:
        # Populate alarm data form fields
        form.title.data = selected_alarm['title']
        form.time.data = dt.strptime(selected_alarm['alarm'], "%H:%M")
        form.action.data = selected_alarm['action']
        form.days.data = selected_alarm['days']

    return render_template('edit_alarm.html', form=form)


# Delete Alarm
@app.route('/delete_alarm/<string:id>', methods=['POST'])
def delete_alarm(id):

    alarms = get_alarm_data()

    for alarm in alarms:
        if alarm['id'] == id:
            alarms.remove(alarm)

    write_alarm_data(alarms)
    flash('Alarm Deleted', 'success')

    return redirect(url_for('alarm_dashboard'))


# Color Gauges
@app.route('/gauges')
def color_gauges():
    return render_template('gauges.html')


@app.route('/valueofslider')
def valueofslider():
    sender = request.args.get('sender')
    value = request.args.get('value')
    # print("{}: {}".format(sender, value))
    return render_template('gauges.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )
