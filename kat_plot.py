import xlrd
import pandas as pd
import re
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


plate1 = pd.read_excel('06222016_Staph_Array_Data.xlsx', sheetname='Plate1', header = 1)
col_names = (plate1.columns.values)
toxins = col_names[4:] #use header as the toxin names


plate1['Sample ID'] = plate1 ['Sample ID'].str.strip()

plate1['Patient ID'] = [re.findall('Standard|^\d*', item)[0] for item in plate1['Sample ID']] 
plate1['Visit'] = [re.findall('V\d|Standard', item)[0] for item in plate1['Sample ID']] 
plate1['Dilution'] = [re.findall('100*$', item)[0] for item in plate1['Sample ID']]    

#This function divide each unique patient by their unique visit, each visit plot toxin against dilution
def uniquepatientvisit(patient,toxin): 
    for visit in patient['Visit'].unique():
        #print(patient[patient['Visit']==visit])
        data = patient[patient['Visit']==visit]
        plt.plot(data['Dilution'], data[toxin])
        
#This function divide the data by each unique patient ID, call the previous uniquepatientvisit function and plot one graph for a toxin of each patient
def plottoxin(plate,toxin):
    for patient in plate['Patient ID'].unique():
        bypatient = plate[plate['Patient ID'] == patient]
        fig = plt.figure()
        uniquepatientvisit(bypatient,toxin)
        if (bypatient[toxin].isnull().sum().sum()) == 0:
            plt.legend(bypatient['Visit'],loc = 1)
            plt.xscale('log')
            plt.title('patient: '+patient+" "+ 'toxin: '+toxin)
            plt.show()
                                                  
        else:
            print('Missing data for %s %s' %(patient,toxin))
            

#loop through the toxins and plot each toxin using the plottoxin function
print('VERY IMPORTANT! THE OUTPUT IS NOT SAVED GRAPH BECAUSE I CANT FIGURE OUT THE BEST WAY TO CHANGE THE NAME OF THE TOXIN..SO WHILE RUNNING THIS CODE, THE OUPUT ARE TONES OF GRPH\
AS!!!!!!!')
###### VERY IMPORTANT! THE OUTPUT IS NOT SAVED GRAPH BECAUSE I CANT FIGURE OUT THE BEST WAY TO CHANGE THE NAME OF THE TOXIN..SO WHILE RUNNING THIS CODE, THE OUPUT ARE TONES OF GRPHAS!!!!!!!
for toxin in toxins:
    plottoxin(plate1, toxin)
