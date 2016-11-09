import xlrd
import pandas as pd
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


#This function divide each unique patient by their unique visit, each visit plot toxin against dilution
def uniquepatientvisit(patient,toxin): 
    for visit in patient['Visit'].unique():
        data = patient[patient['Visit']==visit]
        plt.plot(data['Dilution'], data[toxin])
        
#This function divide each plate by the unique patient and toxin, and plot one graph for each patient and toxin
##### THIS IS TO PRINT NOT TO SAVE THE FIGURES!! BEWARE OF COMPUTER CRASHING
def plottoxin(plate,toxin):
    for patient in plate['Patient ID'].unique():
        bypatient = plate[plate['Patient ID'] == patient]
        fig = plt.figure()
        uniquepatientvisit(bypatient,toxin)
        if (bypatient[toxin].isnull().sum().sum()) == 0:
            plt.legend(bypatient['Visit'].unique(), loc = 1)
            plt.xscale('log')
            plt.title('patient: '+patient+" "+ 'toxin: '+toxin)
            plt.show()
                                                  
        else:
            print('Missing data for %s %s' %(patient,toxin))


#For loop that read the content of each data sheet of the excel file
for i in range(1, 12):
    # put the content of each data sheet into variable x
    if i in range(1,6):
        x = pd.read_excel('06222016 Staph Array Data.xlsx', sheetname='Plate '+ str(i), header = 1)
    else:
        x= pd.read_excel('06222016 Staph Array Data.xlsx', sheetname='Plate'+ str(i), header = 1)
    
#fix the formatting issues in the 'Sample ID' column on each plate
#For Plate2, fix the dilution for the 'Standard'
    if i == 2:
        x.ix[0:6, 'Sample ID'] = ['Standard 10', 'Standard 100', 'Standard 1000', 'Standard 10000', 'Standard 100000','Standard 1000000', 'Standard 10000000']

#For plate3, add 'visit' for row31-34 and 39-42,  change 'v1' to 'V1' for row4-6
    if i == 3:
        x.ix[31:34, 'Sample ID'] = ['62900 V1 100', '62900 V1 1000', '62900 V1 10000', '62900 V1 100000']
        x.ix[39:42, 'Sample ID'] = ['17588 V1 100', '17588 V1 1000', '17588 V1 10000', '17588 V1 100000']
        x.ix[4:6, 'Sample ID']=['48689 V1 1000', '48689 V1 10000','48689 V1 100000' ]

#For plate6, 7, 8 and 9, fix the dilution for the 'Standard'
    if i in range(6,10):
        x.ix[0:2, 'Sample ID'] = ['Standard 1000', 'Standard 10000', 'Standard 100000']

#For plate10, remove the HSS from 'Sample ID' column (this should be in 'hospital' column)
    if i == 10:
        x.ix[3: ,'Sample ID'] = [item[3:] for item in x.ix[3: ,'Sample ID']]
    
#Remove the extra blank space before and after the contents of 'Sample ID' column
    x['Sample ID'] = x['Sample ID'].str.strip() 

#Parse Patient ID information from the'Sample ID' column and put into a new column called 'Patient ID'. For 'Standard 100' kind of rows, patient ID is considered 'Standard'; for ' Healthy GS1 100' kind of rows, patient ID is considered 'Healthy'.
    x['Patient ID'] = [re.findall('Standard|Healthy|^\d*', item)[0] for item in x['Sample ID']]

#Parse visit information from 'Sample ID'column and put into a new column called 'Visit'. For 'Standar ID' kind of row, 'Standard' is considered the Visit. For 'Healthy GS1 100' kind of rows, 'GS1' is considered the Visit.
    x['Visit'] = [re.findall('V\d|Standard|GS\d|JM', item)[0] for item in x['Sample ID']]

#Parse dilution information from 'Sample ID' column and put into a new column called 'Dilution'.    
    x['Dilution'] = [re.findall('100*$', item)[0] for item in x['Sample ID']]

#Fill in the empty cells in Hospital, Age and Gender columns with implied values
    x = x.fillna(method='ffill', limit = 3)
    
# Converts and saves cleaned dataframe as tab-delimited CSV file
    x.to_csv('tab_delimited_Plate' + str(i) +'.csv', sep='\t', index = False, header = True)

#Using the tab delimited files to print the plots for all the toxins
#BEWARE TONS OF PLOTS ARE COMING...
for i in range(1, 12):
    x = pd.read_csv('tab_delimited_Plate'+ str(i)+'.csv', sep='\t',index_col=0)
    col_names = (x.columns.values)
    toxins = col_names[4:-3]
#Call the plotting function: plottoxin for every plate.    
    for toxin in toxins:
        plottoxin(x,toxin)   
