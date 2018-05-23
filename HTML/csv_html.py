from prettytable import PrettyTable

from prettytable import from_csv

with open('cities.csv', 'r') as fp:
    x=from_csv(fp)

html_code = x.get_html_string()
html_file = open('table.html', 'w')
html_file = html_file.write(html_code)

