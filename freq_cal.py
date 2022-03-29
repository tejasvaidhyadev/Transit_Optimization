import pandas as pd 
import yaml
import numpy as np

def load_yaml(file_name):
    with open(file_name, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg
args = load_yaml('config/param.yaml')
globals().update(args) # not a good practice

def freq():
    passengerarrivalrd = pd.read_csv("data/Passenger_arrival_DN.csv").set_index('Passenger arrival')
    max_pass_periodrd = passengerarrivalrd.max(axis=1,skipna=False)   # to print max value in a row, row wise i.e. max passengers in a period
                                    
    freqrd =(np.ceil(max_pass_periodrd/(dob*hrinperiod)))        #Frequency is bus required for maximum passengers in an hour (1period =4)
    #print(freqrd)
    freqrd[freqrd<frequencydefault] = frequencydefault        # Minimum Desire bus frequency is 2, should not be less that 2
    #print(freqrd)
    headwayrd1=(1/freqrd)*60
    infreqrd1= pd.DataFrame({'Time Period':freqrd.index, 'Initial Frequency':freqrd.values, 'Initial Headway':headwayrd1.values}).set_index('Time Period')      ############impo ########### , 'Initial Headway':headwayrd1.values


    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                           1.1.2 FREQUENCY CALCULATION 2  (based on load profile across stops)  GARIA AIRPORT
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    distancerd= pd.read_csv("data/distanceDN.csv").set_index('Distance')
    #print(distancerd)
    Lrd= distancerd.sum(axis = 1, skipna = True).values   # defined Total Distance depot ot depot
    #print(Lrd)
    Lrd= np.ceil(float(np.asarray(Lrd)))   # converts Array value to Float value with ceiling
    #print(Lrd)
    #max_pass_periodrd = pd.DataFrame({'Time Period':max_pass_periodrd.index, 'Max Passenger Load':freqrd.values}).set_index('Time Period')    #making Series to Dataframe
                                                                    ### Not Required      passengerarrivalrd.apply(lambda x: x.max() - x, axis=1)
    #####max_pass_periodrd['passenger lost']= max_pass_periodrd['Max Passenger Load'] - passengerarrivalrd.iloc[2]
    passengerkilometerrd = passengerarrivalrd.mul(distancerd.values, axis=1)      #passengerkilometerrd is no of passenger traveling distance
    #print(f'\nStop to stop distance : \n',distancerd)
    #print(f'\nPassenger kilometer (period) : \n',passengerkilometerrd)
    asasrd= np.ceil(passengerkilometerrd.sum(axis = 1, skipna= True))
    #print(asasrd)
    passkmrd= passengerkilometerrd/(dob*Lrd*hrinperiod)   #passenegr load kilometer required / desired  capacity of bus kilometer available
    passkmrd= np.ceil(passkmrd.sum(axis = 1, skipna= True))   #Sum value of row in row wise
    #print(passkmrd)                                                                                                          # IMP CODE   to round decimal point       passkmrd=passkmrd.round(decimals=1)

    maxcaprd= max_pass_periodrd/(cob*hrinperiod)
    maxcaprd= np.ceil(maxcaprd)
    #print(maxcaprd)
    freqrd2= pd.DataFrame({'Time Period':freqrd.index,'passenger kilometer': passkmrd.values, 'Maximum Capacity':maxcaprd, 'Default Frequency': frequencydefault}).set_index('Time Period')   #matric of frequency by maximum passenger kilometer, maximum capacity and defalult frequency
    #print(freqrd2)

    freqrd2 = freqrd2.max(axis=1,skipna=False)
    #print(freqrd2)
    headwayrd2=(1/freqrd2)*(60)
    infreqrd2= pd.DataFrame({'Time Period':freqrd2.index, 'Initial Frequency2':freqrd2.values, 'Initial Headway2':headwayrd2.values}).set_index('Time Period')

    print(f'\n----------------------------------------------------------------------------\n'
        f'Frequency and Headway determined by Ride Check Method in Bag Bazaar to Garia is :'
        f'\n----------------------------------------------------------------------------\n',infreqrd2) 
    return (Lrd, freqrd2, headwayrd2, infreqrd2)

def freq_cal3(Lrd, freqrd2, headwayrd2, infreqrd2):
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                           1.1.3 FREQUENCY METHODOLOGY GARIA AIRPORT
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    frequencyrd =freqrd2.values      #freqrd
    headwayrd= headwayrd2.values     #headwayrd1

    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                           1.2.1 FREQUENCY CALCULATION  (based on Max passengers load in period)  AIRPORT GARIA
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    passengerarrivaldr = pd.read_csv("data/Passenger_arrival_UP.csv").set_index('Passenger arrival')
    #print(passengerarrivaldr)
                        # to print top 5 value: print(passengerarrival.head())
                        # to print max value of each column: print(passengerarrival.max())
                        #print(passengerarrivaldr)
    max_pass_perioddr = passengerarrivaldr.max(axis=1,skipna=False)   # to print max value in a row, row wise i.e. max passengers in a period
    #print(passengerarrivaldr)
                                                        # to print a row of maximum value in a particular column print(passengerarrival[passengerarrival['Raipur']==passengerarrival['Raipur'].max()])
    #print(max_pass_perioddr)
    freqdr =(np.ceil(max_pass_perioddr/(dob*hrinperiod)))        #Frequency is bus required for maximum passengers in an hour (1period =4)
    #print(freqdr)
    freqdr[freqdr<frequencydefault] = frequencydefault        # Minimum Desire bus frequency is 2, should not be less that 2
    #print(freqdr)
    headwaydr1=(1/freqdr)*60
    infreqdr1= pd.DataFrame({'Time Period':freqdr.index, 'Initial Frequency':freqdr.values, 'Initial Headway':headwaydr1.values}).set_index('Time Period')      ############impo ########### , 'Initial Headway':headwaydr1.values
    #print(f'\nHeadway determined by Max passeneger load in each period in Durg to Raipur is : \n',infreqdr1)     #FINAL PRINT


    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                           1.2.2 FREQUENCY CALCULATION 2  (based on load profile across stops)   AIRPORT GARIA
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    distancedr= pd.read_csv("data/distanceUP.csv").set_index('Distance')
    #print(distancedr)
    Ldr= distancedr.sum(axis = 1, skipna = True).values   # defined Total Distance depot ot depot
    #print(Ldr)
    Ldr= np.ceil(float(np.asarray(Ldr)))   # converts Array value to Float value with ceiling
    #print(Ldr)
    #max_pass_perioddr = pd.DataFrame({'Time Period':max_pass_perioddr.index, 'Max Passenger Load':freqdr.values}).set_index('Time Period')    #making Series to Dataframe
                                                                    ### Not Required      passengerarrivaldr.apply(lambda x: x.max() - x, axis=1)
    #####max_pass_perioddr['passenger lost']= max_pass_perioddr['Max Passenger Load'] - passengerarrivaldr.iloc[2]
    passengerkilometerdr = passengerarrivaldr.mul(distancedr.values, axis=1)      #passengerkilometerdr is no of passenger traveling distance

    #print(f'\nStop to stop distance : \n',distancedr)
    #print(f'\nPassenger kilometer (period) : \n',passengerkilometerdr)
    asasdr= np.ceil(passengerkilometerdr.sum(axis = 1, skipna= True))
    #print(asasdr)
    passkmdr= passengerkilometerdr/(dob*Ldr*hrinperiod)   #passenegr load kilometer required / desired  capacity of bus kilometer available
    passkmdr= np.ceil(passkmdr.sum(axis = 1, skipna= True))   #Sum value of row in row wise
    #print(passkmdr)                                                                                                          # IMP CODE   to round decimal point       passkmdr=passkmdr.round(decimals=1)

    maxcapdr= max_pass_perioddr/(cob*hrinperiod)
    maxcapdr= np.ceil(maxcapdr)
    #print(maxcapdr)
    freqdr2= pd.DataFrame({'Time Period':freqdr.index,'passenger kilometer': passkmdr.values, 'Maximum Capacity':maxcapdr, 'Default Frequency': frequencydefault}).set_index('Time Period')   #matric of frequency by maximum passenger kilometer, maximum capacity and defalult frequency
    #print(freqdr2)

    freqdr2 = freqdr2.max(axis=1,skipna=False)
    #print(freqdr2)
    headwaydr2=(1/freqdr2)*(60)
    infreqdr2= pd.DataFrame({'Time Period':freqdr2.index, 'Initial Frequency2':freqdr2.values, 'Initial Headway2':headwaydr2.values}).set_index('Time Period')

    print(f'\n----------------------------------------------------------------------------\n'
        f'Frequency and Headway determined by Ride Check Method in Garia to Bag Bazaar is :\n'
        f'----------------------------------------------------------------------------\n',infreqdr2)  #FINAL PRINT