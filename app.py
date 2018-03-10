# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
import sys
import smbus
from tm1637 import TM1637
#from crontab import CronTab
device = smbus.SMBus(1)



display = TM1637(CLK=21, DIO=20, brightness=1.0)

display.Clear()
digits = [1, 3, 3, 7]
display.Show(digits)

#Initialize the Flask applicationI
app = Flask(__name__)
# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    #cron = CronTab(user=True)
    #return "UserCron: " + str(cron)#render_template('form_submit.html')
    return render_template('form_submit.html')

@app.route('/hello/', methods=['POST'])
def hello():
    name=request.form['yourname']
    email=sys.version #request.form['youremail']
    run_count = 0


    display.Clear()
    digits = [int(name), 5, 5, 5]
    display.Show(digits)


    address = 50
    print("I2C: Schreiben auf Device 0x{:02X}".format(address))
    try:
            device.write_i2c_block_data(0x32, 0x00, [0x1])

    except IOError as err:
            print("Fehler beim Schreiben auf Device 0x{:02X}".format(address))
            #exit(-1)


    print("Done")
 
    #return render_template('form_action.html', name=name, email=sys.version)
    return render_template('form_submit.html')

# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=int("80")
  )
