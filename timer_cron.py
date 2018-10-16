import os
from importlib.util import spec_from_file_location, module_from_spec
from json import load
from re import match
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
    alarms = load(alarms_file)["array"]

alarm_ref_time = current_time.strftime('%H:%M')
print(alarm_ref_time)
alarm_ref_day = current_time.weekday()

for alarm in alarms:
    alarm_entry = alarm["alarm"]
    
    if(alarm_ref_time == alarm_entry) and alarm_ref_day in alarm["days"]:
        action = alarm["action"]
        print("running action ", action)

        m = match("([a-zA-Z]+) ?(.*)?", action)
        if m:
            spec = spec_from_file_location("actions."+m.group(1),"%sactions/%s.py"%(working_dir, m.group(1)))
            mod = module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.main(m.group(2))

    print(alarm_entry)

