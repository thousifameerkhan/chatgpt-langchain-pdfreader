import csv

# Read data from existing CSV file
with open('API_TXNS_old.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    
    # Iterate through rows and print values
     # Skip headers
    next(reader)
    next(reader)
    
    # Define headers
    headers = ['key', 'description']
    
    with open('API_TXNS.csv', 'w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in reader:
            # print(row[0])
            a = "API_TXNS"+"."+row[0]
            b = row[0]+" "+row[4]
            print(b)
            writer.writerow([a, b])