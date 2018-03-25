import os
import json
from datetime import datetime
from tm1637 import TM1637

# Get current time
current_time = datetime.now()
working_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep

def display_time(time_element):
	time_to_display = time_element.strftime('%H%M')
	#Display time
	display = TM1637(CLK=21, DIO=20, brightness=1.0)
	display.Clear()
	display.ShowDoublepoint(True)
	display.Show([int(d) for d in str(time_to_display)])

display_time(current_time)

alarms = []
with open(working_dir + 'alarms.json') as alarms_file:    
    alarms = json.load(alarms_file)["array"]

for alarm_num in range(len(alarms)):
    alarm_ref_time = current_time.strftime('%H:%M')
    alarm_entry = alarms[alarm_num]["alarm"]
    alarm_minutes = ":".join(alarm_entry.split(":")[:2])
    
    if(alarm_ref_time == alarm_minutes):
	action = alarms[alarm_num]["action"]
	print("running action ", action)
	os.system("python " + working_dir + action)
    print(alarm_ref_time)
    print(alarm_minutes)

