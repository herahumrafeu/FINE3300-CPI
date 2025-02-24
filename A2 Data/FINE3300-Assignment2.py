import pandas as pd

#answering first part of the assignment
#writing the file paths for the data files
file_path = [
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/AB.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/BC.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/Canada.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/MB.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/NB.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/NL.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/NS.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/ON.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/PEI.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/QC.CPI.1810000401.csv",
    "/Users/rafeuherahum/Documents/FINE3300/FINE3300-CPI/A2 Data/SK.CPI.1810000401.csv",
]

#creating an empty list to store DataFrames
dfs = []

#reading data from the csv files into Panda and formatting the data as asked in the assignment
for file in file_path:
    df = pd.read_csv(file)

    #as the jurisdiction is in the file name, writing command to extract the jurisdiction from the file name
    jurisdiction = file.split('/')[-1].split('.')[0].split("_")[0].replace("CPI", "").replace("1810000401", "").strip()
    
    #using df_melted to melt the data i.e. converting the multiple month headers into a single month column, making sure the items are not changed and CPI is the value
    df_melted = df.melt(id_vars=["Item"], var_name="Month", value_name="CPI")

    #adding the jurisdiction column
    df_melted["Jurisdiction"] = jurisdiction

    #making sure that the month column starts from January as per the example in the assignment brief
    month_order = ["24-Jan", "24-Feb", "24-Mar", "24-Apr", "24-May", "24-Jun", "24-Jul", "24-Aug", "24-Sep", "24-Oct", "24-Nov", "24-Dec"]
    df_melted["Month"] = pd.Categorical(df_melted["Month"], categories=month_order, ordered=True)

    #append to the list
    dfs.append(df_melted)

#combining all the DataFrames
combined_df = pd.concat(dfs, ignore_index=True)

#converting CPI to a numeric type.
combined_df["CPI"] = pd.to_numeric(combined_df["CPI"], errors='coerce')

#making sure the column headers are in the correct order as per the assignment brief
combined_df = combined_df[["Item", "Month", "Jurisdiction", "CPI"]]

#answering second part of the assignment
print(combined_df.groupby("Jurisdiction").head(1).head(12))


#answering third part of the assignment
#creating a list of the categories that are required by question 3
categories = ["Food", "Shelter", "All-items excluding food and energy"]

#making sure it filters the data for categories that are needed without modifying the original DataFrame
filtered_df = combined_df[combined_df["Item"].isin(categories)].copy()

#calculating the month-to-month percentage change as per the assignment brief
filtered_df["MoM_Change"] = filtered_df.groupby(["Jurisdiction", "Item"])["CPI"].pct_change() * 100

#then calculating the average month-to-month change by jurisdiction and category and rounding it to 1 decimal place
average_mom_change = filtered_df.groupby(["Jurisdiction", "Item"])["MoM_Change"].mean().round(1).reset_index()

#printing the results for question 3
print("\nAverage Month-to-Month Change for Canada and each of the provinces")
print(average_mom_change)


#answering fourth part of the assignment
#filtering the data to only show the highest month-to-month change using if statement
if not average_mom_change.empty:
    highest_mom_change = average_mom_change.loc[average_mom_change.groupby("Item")["MoM_Change"].idxmax()]
else:
    highest_mom_change = pd.DataFrame(columns=["Jurisdiction", "Item", "MoM_Change"])

#printing the results for question 4
print("\nProvince with the Highest Average Change")
print(highest_mom_change)


#answering fifth part of the assignment 
#filtering the data to only show the services category using if statement
if "Services" in combined_df["Item"].unique():
    services_df = combined_df[combined_df["Item"] == "Services"].copy()

    #extracting the CPI data for 24-Jan and 24-Dec from each csv file
    jan_cpi = services_df[services_df["Month"] == "24-Jan"].set_index("Jurisdiction")["CPI"]
    dec_cpi = services_df[services_df["Month"] == "24-Dec"].set_index("Jurisdiction")["CPI"]

    #calculating the annual CPI change for services across Canada and provinces
    annual_cpi_change = (dec_cpi - jan_cpi).round(1).reset_index()
    annual_cpi_change.columns = ["Jurisdiction", "Annual_CPI_Change"]

    #printing the results for question 5
    print("\nAnnual CPI Change for Services Across Canada and Provinces")
    print(annual_cpi_change)

else:
    print("\nNo change in CPI for services")


#answering sixth part of the assignment
#using if statement to sort the data by highest annual CPI change and only show the highest province
if "Services" in combined_df["Item"].unique():
    # Sort by highest annual CPI change
    highest_cpi_provinces = annual_cpi_change.sort_values(by="Annual_CPI_Change", ascending=False).head(1)

    # Display results for Question 6
    print("\nRegion with the Highest Annual Inflation in Services")
    print(highest_cpi_provinces)

else:
    print("\nNo change in CPI for services")
