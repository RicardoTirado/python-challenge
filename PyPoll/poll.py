import os
import csv
candidate = []
pollDict = []
percentage = []

pollcsv = [os.path.join('election_data_1.csv'), os.path.join('election_data_2.csv')]

for file in pollcsv:
    with open(file, newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        first_line = csvfile.readline()

        for row in csvreader:
            candidate.append(row[2])

            totalvotes = len(candidate)

        from collections import Counter
        pollDict = Counter(candidate)

print("Election Results")
print("-----------------------------")
print("Total Votes: " + str(totalvotes))
print("-----------------------------")

for k, v in pollDict.items():
    print(k, ": ", round(v/totalvotes*100, 2), "% ", "(", v, ")")

print("-----------------------------")
print("Winner: " + max(pollDict))
print("-----------------------------")
