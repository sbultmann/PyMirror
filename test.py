import pandas as pd
from datetime import datetime, timedelta
import thingspeak
import pytz
import json

ch = thingspeak.Channel(1880870)



df = pd.DataFrame(json.loads(ch.get({'results': 24*60*60/30}))['feeds'])
df.columns = ['time','entry_id','temperature', 'humidity', 'pressure']
print(df.head())
df['time'] = pd.to_datetime(df['time'])

df['temperature'] = pd.to_numeric(df['temperature'])
df['humidity'] = pd.to_numeric(df['humidity'])
df['pressure'] = pd.to_numeric(df['pressure'])


print(df.head())
print(list(df['time'])[-1])