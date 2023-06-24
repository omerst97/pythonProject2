r0 = [4.15, 2.12, 1.03]
r1 = [2.05, 4.25, 0.92]
r2 = [1.85, 3.96, 1.15]
r3 = [4.95, 2.45, 1.05]
r4 = [4.87, 2.98, 1.91]
r5 = [5.18, 2.92, 2.03]
r6 = [2.78, 4.85, 0.96]

l = [r0, r1, r2, r3, r4, r5, r6]

res =[]
for i in l:
    raw = []
    for j in l:
        sumsquered=0
        for k in range(len(i)):
            sumsquered += (i[k]-j[k])**2

        dis = sumsquered**0.5
        raw.append(dis)
    res.append(raw)




import pandas as pd


df = pd.DataFrame(res)  # Create a pandas DataFrame from the list of lists

filepath = 'C:\\Users\\159om\\OneDrive\\Desktop\\trees.xlsx'  # Specify the file path where you want to save the Excel file

df.to_excel(filepath, index=False)  # Write the DataFrame to an Excel file

