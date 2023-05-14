import csv,os,pandas as pd

# Create an object representing the entire Excel file
excel_file = pd.ExcelFile('./01-data/ofsll_open_interface_manual_servicing.xlsx')

# Loop through each sheet in the file
with open(f'./02-csv-sheets/master.csv', 'w', newline='\n') as file:
    
    # Define headers
    headers = ['key', 'description']
    writer = csv.writer(file)
    writer.writerow(headers)

    for sheet_name in excel_file.sheet_names:
        print(sheet_name)
        if sheet_name != "API MAPPING":
            # Read in the sheet as a DataFrame
            df = excel_file.parse(sheet_name)

            # Replace commas with spaces in all columns
            df = df.apply(lambda x: x.str.replace(',', ' '))

            # Write updated data to a CSV file with the sheet name as the file name
            df.to_csv(f'./02-csv-sheets/{sheet_name}_old.csv', index=False)
            with open(f'./02-csv-sheets/{sheet_name}_old.csv', 'r') as input_file:
                reader = csv.reader(input_file)

                # Iterate through rows and print values
                # Skip headers
                next(reader)
                next(reader)
                for row in reader:
                    # print(row[0])
                    a = sheet_name+"."+row[0]
                    b = row[0]+" "+row[4]
                    print(b)
                    writer.writerow([a, b])
            os.remove(f'./02-csv-sheets/{sheet_name}_old.csv')
