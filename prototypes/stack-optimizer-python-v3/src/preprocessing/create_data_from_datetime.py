import pandas as pd

df = pd.read_excel('../input/input_samples_datetime.xlsx')


# Convert 'appointment_start_time' to datetime format
df['appointment_start_time'] = pd.to_datetime(df['appointment_start_time'])

# Sort the DataFrame based on 'appointment_start_time'
df = df.sort_values(by='appointment_start_time')

# Convert the datetime to a categorical column and then get the integer codes
df['appointment_time'] = df['appointment_start_time'].astype('category').cat.codes + 1

# Drop the 'appointment_end_time' column
df = df.drop(columns=['appointment_start_time', 'appointment_end_time'])

# Write the DataFrame to a new Excel file
df.to_excel("../input/input_samples.xlsx", index=False)
