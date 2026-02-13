import pandas as pd
import os




df = pd.read_excel('../input/input_samples.xlsx')

base_time = pd.Timestamp('2023-09-06 08:00:00')

df['appointment_start_time'] = df['appointment_time'].apply(lambda x: base_time + pd.Timedelta(minutes=30*(x-1)))

df['appointment_end_time'] = df['appointment_start_time'] + pd.Timedelta(minutes=30)

df.drop('appointment_time', axis=1, inplace=True)

df.to_excel("../input/input_samples_datetime.xlsx", index=False)
