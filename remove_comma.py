import pandas as pd

# Create an object representing the entire Excel file
excel_file = pd.ExcelFile('./01-data/ofsll_open_interface_manual_servicing.xlsx')

# Loop through each sheet in the file
for sheet_name in excel_file.sheet_names:
    # Read in the sheet as a DataFrame
    df = excel_file.parse(sheet_name)
    
    # Replace commas with spaces in all columns
    df = df.apply(lambda x: x.str.replace(',', ' '))
    
    # Write updated data to a CSV file with the sheet name as the file name
    df.to_csv(f'./02-csv-sheets/{sheet_name}.csv', index=False)