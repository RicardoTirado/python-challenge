#to import os module in order to create file path
import os

#to import csv files
import csv

#csv files
csv_files = [os.path.join('raw_data', 'employee_data1.csv'), os.path.join('raw_data', 'employee_data2.csv')]

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

for file in csv_files:
    with open(file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        header = next(csvreader)

        final_output = []
        for row in csvreader:
            EmpID = row[0]
            Name = row[1] 
            DOB = row[2] 
            SSN = row[3] 
            State = row[4] 

            # Convert values to new format
            first, last = Name.split()
            y, m, d = DOB.split("-")
            new_SSN = "***-**-" + SSN[-4:]
            new_State = us_state_abbrev[State]
            final_output.append([EmpID, first, last, m + "/" + d + "/" + y, new_SSN, new_State])

    # Write values in final_output list into new CSV
    with open(file[:-4] + "_new.csv", 'w', newline = '') as newcsvfile:
        newcsvwriter = csv.writer(newcsvfile, delimiter=',')
        newcsvwriter.writerow(["Emp ID","First","Last","DOB","SSN","State"])

        for row in final_output:
            newcsvwriter.writerow(row)