#Note: pandas package for python needs to be installed
#and the path name in the os.walk() method also needs to be changed to be able to run the script

import pandas as pd
import xml.etree.ElementTree as ET
import os

bug_counter = 0

#Dict with bug status to count types of bugs and their amount and time submitted and time resolved to calcuate resoltion time metrics
my_dict = {
    'bug_status': [],
    'time_submitted': [],
    'time_resolved': []
}

#Change the path to where your hbaseBugReport extracted tar folder is
#(Do not remove the r character that is in front of the path name)
for path, dirs, files in os.walk(r"C:\Users\shafa\Desktop\hbaseBugReport"):
    #looping through every xml file in the folder
    for f in files:
        my_path = os.path.join(path, f)
        root = ET.parse(os.path.join(path, f)).getroot()
        #finding the xml element "type" and only the ones that include the text 'Bug'
        if root.find('./channel/item/type').text == 'Bug':
            bug_counter += 1
            #finding all bug statuses
            bug_status = root.find('./channel/item/status').text.strip()

            if bug_status != 'Resolved' and bug_status != 'Closed':
                my_dict['time_resolved'].append(None)

            #finding bug statuses that have been resolved (closed and resolved bugs only)
            else:
                #parsing the bug resolution date and formatting it
                timestamp_resolved = pd.to_datetime(root.find('./channel/item/resolved').text, format='%a, %d %b %Y %H:%M:%S %z')
                my_dict['time_resolved'].append(timestamp_resolved)

            my_dict['bug_status'].append(bug_status)
            #parsing the bug creation date and formatting it
            timestamp_created = pd.to_datetime(root.find('./channel/item/created').text, format='%a, %d %b %Y %H:%M:%S %z')
            my_dict['time_submitted'].append(timestamp_created)

df = pd.DataFrame.from_dict(my_dict)
#finding bug statuses that have been resolved (closed and resolved bugs only)
df_resolved = df[df.bug_status.isin(['Closed', 'Resolved'])].reset_index(drop=True)
#calculating the time taken to resolve the bugs
df_timeresolved = df_resolved['time_resolved'] - df_resolved['time_submitted']

#converting the dataframe into a dictionary
counts = df['bug_status'].value_counts().to_dict()

print("There are a total of {} issue reports that are bugs".format(bug_counter))

for k in counts:
    print(f'There are {counts[k]} bugs that are in the {k} state.')

#formatting output into days hours minutes and seconds
days, hours, minutes, seconds, *_ = df_timeresolved.min().components
#finding amount of years taken to resolve the bug
q, r = divmod(days, 365)
print(f'The minimum resolution time is: {q} years, {r} days, {hours} hours, {minutes} minutes, {seconds} seconds')

days, hours, minutes, seconds, *_ = df_timeresolved.max().components
q, r = divmod(days, 365)
print(f'The maximum resolution time is: {q} years, {r} days, {hours} hours, {minutes} minutes, {seconds} seconds')

days, hours, minutes, seconds, *_ = df_timeresolved.median().components
q, r = divmod(days, 365)
print(f'The median resolution time is: {q} years, {r} days, {hours} hours, {minutes} minutes, {seconds} seconds')

days, hours, minutes, seconds, *_ = df_timeresolved.mean().components
q, r = divmod(days, 365)
print(f'The average resolution time is: {q} years, {r} days, {hours} hours, {minutes} minutes, {seconds} seconds')
