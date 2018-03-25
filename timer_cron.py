import json
from datetime import datetime
from tm1637 import TM1637

# Time as 4-digit int
current_time = datetime.now().strftime('%H%M')

# Split int as four individual list entries
tm = [int(d) for d in str(current_time)]

#Display time
display = TM1637(CLK=21, DIO=20, brightness=1.0)
display.Clear()
display.ShowDoublepoint(True)
display.Show(tm)

#alarms = []
#with open('alarms.json') as alarms_file:    
#    alarms = json.load(alarms_file)["array"]
#
#for alarm_num in range(len(alarms)):
#    print(alarms[alarm_num]["alarm"])
#
