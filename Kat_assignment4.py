
import pandas as pd
import xlrd

### these code allows use to use loop to grab data from all sheets, idea came from Qi Sun
for num in range(1,12):
    x = 'plate' + str(num)
    x = pd.read_excel('06222016_Staph_Array_Data.xlsx', sep = '\t', sheetname = 'Plate'+str(num))
    
    
### following code allows us to extract data from individual plate and change it into the dataframe    
def getdata(x):
    data = pd.read_excel('06222016_Staph_Array_Data.xlsx', sep = '\t', header = 1,index_col = 0, sheetname = 'Plate'+str(x))
    return data

print(getdata(2))

