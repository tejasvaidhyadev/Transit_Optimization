import pandas as pd
import numpy as np
import sys
sys.path.append("D:\IIT KGP\Thesis\scheduling\thesis final asish-20211123T065609Z-001\ga optimization\ga.py")
import ga as ga
import scipy as scipy
import scipy.stats
import matplotlib.pyplot as plt
import datetime as dt

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.precision', 2)

A ='Bag bazaar'
B="Garia"

frequencydefault =2         # Default frequency of Bus
dob = 43                    # Desired occupancy of bus
cob = 107                    # Capacity of bus 2.5 # crowding fact

buscost=7000000             # Cost of bus (including loan interest)
buslifecycle=800000         # No. of years a bus would be operational
crewperbus=2                # No. of crew required per bus (including support staff)
creqincome= 27500           # Average monthly wage of crew members (Driver, Operator, Technicians)
busmaintenance= 5         # Bus maintenance cost per km run
fuelprice=88                # Fuel cost
kmperliter=5                # Mileage

costunit_cantboard=7        # Cost incurred by user for not been able to board
costunit_waitingtime=48/60  # Waiting at bus stop cost incurred by user
costunit_invehtime=24/60    # Invehicle traveltime cost incurred by user
penalty=7                   # Operator part of penalty for loosing a bus passenger
hrinperiod=1                # Length of a period, value means no of hours inn

# important CODE      df.iloc[:, [4]]          to locate a column by no.
# important code     To add new column with default value in Data frame:  passengerarrivalrd['My 2nd new column']= 'default value 2'




#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           1. F R E Q U E N C Y      C A L C U L A T I O N
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           1.1.1 FREQUENCY CALCULATION  (based on Max passengers load in period) GARIA AIRPORT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
passengerarrivalrd = pd.read_csv(r"D:\S21 Data\Database for timetable prediction\Passenger_arrival_DN.csv").set_index('Passenger arrival')
#print(passengerarrivalrd)
                    # to print top 5 value: print(passengerarrival.head())
                    # to print max value of each column: print(passengerarrival.max())
                    #print(passengerarrivalrd)
max_pass_periodrd = passengerarrivalrd.max(axis=1,skipna=False)   # to print max value in a row, row wise i.e. max passengers in a period
#print(passengerarrivalrd)
                                                     # to print a row of maximum value in a particular column print(passengerarrival[passengerarrival['Raipur']==passengerarrival['Raipur'].max()])
#print(max_pass_periodrd)
freqrd =(np.ceil(max_pass_periodrd/(dob*hrinperiod)))        #Frequency is bus required for maximum passengers in an hour (1period =4)
#print(freqrd)
freqrd[freqrd<frequencydefault] = frequencydefault        # Minimum Desire bus frequency is 2, should not be less that 2
#print(freqrd)
headwayrd1=(1/freqrd)*60
infreqrd1= pd.DataFrame({'Time Period':freqrd.index, 'Initial Frequency':freqrd.values, 'Initial Headway':headwayrd1.values}).set_index('Time Period')      ############impo ########### , 'Initial Headway':headwayrd1.values
#print(f'\nHeadway determined by Max passeneger load in each period in Raipur to Durg is : \n',infreqrd1)     #FINAL PRINT

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           1.1.2 FREQUENCY CALCULATION 2  (based on load profile across stops)  GARIA AIRPORT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
distancerd= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\distanceDN.csv").set_index('Distance')
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
      f'\n----------------------------------------------------------------------------\n',infreqrd2)  #FINAL PRINT




#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                    1.1.3 FREQUENCY METHODOLOGY GARIA AIRPORT
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
frequencyrd =freqrd2.values      #freqrd
headwayrd= headwayrd2.values     #headwayrd1












#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           1.2.1 FREQUENCY CALCULATION  (based on Max passengers load in period)  AIRPORT GARIA
#-------------------------------------------------------------------------------------------------------------------------------------------------------
passengerarrivaldr = pd.read_csv(r"D:\S21 Data\Database for timetable prediction\Passenger_arrival_UP.csv").set_index('Passenger arrival')
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
distancedr= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\distanceUP.csv").set_index('Distance')
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



#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                    1.2.3 FREQUENCY METHODOLOGY AIRPORT GARIA
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
frequencydr =freqdr2.values      #freqdr
headwaydr= headwaydr2.values     #headwaydr1














#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2. F L E E T   S I Z E   C A L C U L A T I O N
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.1.1 Departure time calculation   GARIA AIRPORT
#-------------------------------------------------------------------------------------------------------------------------------------------------------

time_periodrd= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\tmeperiodDN.csv", header=0)
print(time_periodrd)
time_periodrd['frequency']= frequencyrd
#print(time_periodrd)
time_periodrd['Headway_in_hours']=(1/(frequencyrd)).round(2)
#print(time_periodrd)

departuretimerd = pd.DataFrame()
for ind,col in time_periodrd.iterrows():
    for f in range(0,int(time_periodrd.iloc[ind,1])):
        departuretimerd = departuretimerd.append({'Departure': (time_periodrd.iloc[ind,0])/100+ ((f*time_periodrd.iloc[ind,2])) ,'From': A },ignore_index=True)     # Replace ((f*time_periodrd.iloc[ind,2]))*60/100
      #print(f)
        #if f < frequencyrd.iloc[ind,2]:
        #df.loc[f,"Departure"]= (col['Time'])/100 + (ind * col["Headway_in_hours"])
#for ind in df.iterrows():
    #df= pd.to_datetime(df)
#print(departuretimerd)
#--------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.1.2 Departure time calculation  AIRPORT GARIA
#-------------------------------------------------------------------------------------------------------------------------------------------------------

time_perioddr= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\tmeperiodUP.csv", header=0)
#print(time_perioddr)
time_perioddr['frequency']= frequencydr
#print(time_perioddr)
time_perioddr['Headway_in_hours']=(1/(frequencydr)).round(2)
#print(time_perioddr)

departuretimedr = pd.DataFrame()
for ind,col in time_perioddr.iterrows():
    for f in range(0,int(time_perioddr.iloc[ind,1])):
        departuretimedr = departuretimedr.append({'Departure': (time_perioddr.iloc[ind,0])/100+ ((f*time_perioddr.iloc[ind,2])) +0.005,'From': B },ignore_index=True)     # Replace ((f*time_periodrd.iloc[ind,2]))*60/100
        #print(f)
        #if f < frequencydr.iloc[ind,2]:
        #df.loc[f,"Departure"]= (col['Time'])/100 + (ind * col["Headway_in_hours"])
#for ind in df.iterrows():
    #df= pd.to_datetime(df)
#print(departuretimedr)
#--------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.2.1 Travel time  GARIA AIRPORT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
traveltimerd= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\TravelTimeDN.csv")
traveltimerd.drop('Travel Time', axis=1, inplace= True)
sumtraveltimerd=traveltimerd.sum(axis = 1, skipna= True)

arrivaltimerd = pd.DataFrame()
for ind in range(0,len(sumtraveltimerd.index)):
    for f in range(0,int(time_periodrd.iloc[ind,1])):
        arrivaltimerd = arrivaltimerd.append({'TT_to_Garia': sumtraveltimerd[ind]/60,'From': A},ignore_index=True).round(2)
#print(arrivaltimerd)



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.2.2 Travel time  AIRPORT GARIA
#-------------------------------------------------------------------------------------------------------------------------------------------------------
traveltimedr= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\TravelTimeUP.csv")
traveltimedr.drop('Travel Time', axis=1,inplace= True)
sumtraveltimedr=traveltimedr.sum(axis = 1, skipna= True)
#print(traveltimedr.to_string())
arrivaltimedr = pd.DataFrame()
for ind in range(0,len(sumtraveltimedr.index)):
    for f in range(0,int(time_perioddr.iloc[ind,1])):
        arrivaltimedr = arrivaltimedr.append({'TT_to_BagBazaar': sumtraveltimedr[ind]/60,'From': B},ignore_index=True).round(2)
#print(arrivaltimedr)



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.3 Vehicle Scheduling ALL DIRECTION
#-------------------------------------------------------------------------------------------------------------------------------------------------------
departuretimerd['TT to Garia']= arrivaltimerd.TT_to_Garia
departuretimedr['TT to Bagbazaar']= arrivaltimedr.TT_to_BagBazaar

departuretime = pd.concat([departuretimerd, departuretimedr], ignore_index=True)
departuretime = departuretime.sort_values(by=['Departure']).reset_index(drop=True)
departuretime['Arrival']=np.zeros(departuretime.shape[0], dtype=int)
tempdeparturetime=departuretime
for i in range(0, departuretime.shape[0]):
    if departuretime.iloc[i,1] == "Bag bazaar":
        departuretime.iloc[i,4]= departuretime.iloc[i,0] + departuretime.iloc[i,2]
    else:
        departuretime.iloc[i,4] = departuretime.iloc[i,0] + departuretime.iloc[i,3]

departuretime["To"]= np.where(departuretime["From"] == "Bag bazaar" , 0, 1 )
departuretime['Fleet B']=np.zeros(departuretime.shape[0], dtype=int)
departuretime['Fleet G']=np.zeros(departuretime.shape[0], dtype=int)
departuretime['Pool B']=np.zeros(departuretime.shape[0], dtype=int)
departuretime['Pool G']=np.zeros(departuretime.shape[0], dtype=int)
for m in range(0,departuretime.shape[0]):#and departuretime.iloc[ind-1,3]=="Raipur":
    #print(departuretime.iloc[0,4].min() and departuretime.iloc[m, 5] == 1)
    if departuretime.iloc[m, 5] == 1 and departuretime.iloc[m,0] <= departuretime.iloc[:,4].min():
        departuretime.iloc[m, 7] = 1

    elif departuretime.iloc[m, 5] == 0 and departuretime.iloc[m,0] <= departuretime.iloc[:,4].min():
        departuretime.iloc[m, 6] = 1

    elif departuretime.iloc[m, 5] == 1 and departuretime.iloc[m,0] > departuretime.iloc[:,4].min():
        departuretime.iloc[m, 9] =1

        departuretime = departuretime.sort_values(["To", "Arrival"],ascending=[True, True])  # .replace(departuretime.iloc[0,4], 99)
        departuretime = departuretime.replace(departuretime.iloc[0, 4], 999)
        departuretime = departuretime.sort_index(ascending=True)

    elif departuretime.iloc[m, 5] == 0 and departuretime.iloc[m,0] > departuretime.iloc[:,4].min():
        departuretime.iloc[m, 8] = 1

        departuretime = departuretime.sort_values(["To", "Arrival"], ascending=[False, True])  # .replace(departuretime.iloc[0,4], 99)
        departuretime = departuretime.replace(departuretime.iloc[0, 4], 999)
        departuretime = departuretime.sort_index(ascending=True)
    else:
        departuretime.iloc[m, 6] = 1

#---------------------
departuretime["Departure"]=np.floor(tempdeparturetime["Departure"])+(tempdeparturetime["Departure"]- (np.floor(tempdeparturetime["Departure"])))/100*60
departuretime["Arrival"]= np.floor(tempdeparturetime["Arrival"])+(tempdeparturetime["Arrival"]- (np.floor(tempdeparturetime["Arrival"])))/100*60                          #str(tempdeparturetime["Arrival"](math.floor(time))) + ':' + str(tempdeparturetime["Arrival"]((time%(math.floor(time)))*60))
#---------------------
departuretime["To"]= np.where(departuretime["To"] == 0 , "Garia", "Bag bazaar" )
print(f'\n--------------------------------------------\n'
      f'Vehicle timetable as per Initial Frequency :'
      f'\n--------------------------------------------\n',departuretime.sort_index(ascending=True).to_string())        #.to_string() is to Show all content  in the result window.  IMPORTANT TO KNOW



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           3.  C O S T   C A L C U L A T I O N S   I N   A L L   D I R E C T I O N
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           3.1 FIXED COST CALCULATIONS ALL DIRECTIONs
#-------------------------------------------------------------------------------------------------------------------------------------------------------

busreq_at_raipur= departuretime['Fleet B'].sum()
busreq_at_durg=departuretime['Fleet G'].sum()
poolsize_at_raipur=departuretime['Pool B'].sum()
poolsize_at_durg=departuretime['Pool G'].sum()
print(f'\n---------------------------------------\n'
      f'Vehicle Operation Details and Costing :'
      f'\n---------------------------------------')
print(f'\nNo. of Bus required at Bag bazaar Depot :',busreq_at_raipur,'\nNo. of Bus required at Garia Depot:',busreq_at_durg,'\n\nNo. of Bus reutilized from Pool at Bagbazaar :',poolsize_at_raipur,"\nNo. of Bus reutilized from Pool at Garia :", poolsize_at_durg)



totalkilometrerunrd=(busreq_at_raipur+poolsize_at_raipur) * (Lrd)
#print(f'\nTotal Bus Kilometre-run in Raipur to Durg direction :\t    ',totalkilometrerunrd,'Km')

#print('----------------------------------------------------------------------')

fuelcostdayrd=(fuelprice*totalkilometrerunrd/kmperliter).round(-2).round(0)
#print(f'Cost of fuel in Raipur to Durg direction :\t\t\t\t  ₹',fuelcostdayrd)

maintenancecostrd= (totalkilometrerunrd*busmaintenance).round(0)
#print(f'Cost of maintenance in Raipur to Durg direction :\t\t   ₹',maintenancecostrd)

vehdepreciationrd= (buscost/buslifecycle *totalkilometrerunrd/(busreq_at_raipur)).round(0)
#print(f'Vehicle depreciation cost in Raipur to Durg direction :\t   ₹',vehdepreciationrd)

crewwagecostrd= (crewperbus*(busreq_at_raipur)*creqincome/30).round(0)
#print(f'Crew cost in Raipur to Durg direction :\t\t\t\t\t  ₹',crewwagecostrd)

#print('----------------------------------------------------------------------')
#print(f'Fixed Vehicle cost in Raipur to Durg direction :\t\t  ₹',fuelcostdayrd+maintenancecostrd+vehdepreciationrd+crewwagecostrd)


print("\nDirection wise details                               Bag bazaar to Garia        Garia to Bag bazaar")
print('-------------------------------------------------------------------------------------------')

totalkilometrerundr=(busreq_at_durg+poolsize_at_durg) * (Ldr)
print(f'Vehcile Kilometre-run :\t                                    ',totalkilometrerunrd,'Km','          ',totalkilometrerundr,'Km')


fuelcostdaydr=(fuelprice*totalkilometrerundr/kmperliter).round(-2)
print(f'Cost of fuel:                                             ₹',fuelcostdayrd,'           ₹',fuelcostdaydr)

maintenancecostdr= (totalkilometrerundr*busmaintenance).round(0)
print(f'Cost of vehicle maintenance:                               ₹',maintenancecostrd,'            ₹',maintenancecostdr)

vehdepreciationdr= (buscost/buslifecycle *totalkilometrerundr/(busreq_at_raipur)).round(0)
print(f'Vehicle depreciation cost:                                 ₹',vehdepreciationrd,'            ₹',vehdepreciationdr)

crewwagecostdr= (crewperbus*(busreq_at_durg)*creqincome/30).round(0)
print(f'Crew cost:                                                ₹',crewwagecostrd,'           ₹',crewwagecostdr)

fixedcostrd=fuelcostdayrd+maintenancecostrd+vehdepreciationrd+crewwagecostrd
fixedcostdr=fuelcostdaydr+maintenancecostdr+vehdepreciationdr+crewwagecostdr
overallfixedcost=fixedcostrd+fixedcostdr
print('-------------------------------------------------------------------------------------------')
print(f'Fixed Vehicle cost:                                       ₹',fixedcostrd,'           ₹',fixedcostdr)
print(f'Total Fixed Vehicle Cost for full Day Operation in both directions:  ₹',overallfixedcost)







#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           3.2 OPERATIONAL COST CALCULATIONS GARIA TO AIRPORT
#-------------------------------------------------------------------------------------------------------------------------------------------------------

# 1 TO GET LIST OF DEPARTURE FROM RAIPUR
'''
depfromraipur=departuretime[departuretime.From=="Bag bazaar"]
depfromraipur = pd.concat([depfromraipur], ignore_index=True)
depfromraipur.reset_index(drop=False)
print(depfromraipur)

# 1 TO GET LIST OF DEPARTURE FROM RAIPUR
depfromdurg=departuretime[departuretime.From=="Garia"]
depfromdurg = pd.concat([depfromdurg], ignore_index=True)
depfromdurg.reset_index(drop=False)
print(depfromdurg)
'''



alightrd= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\alightingrate_DN.csv").set_index('Alighting')
boardrd= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\Boarding_rate_DN.csv").set_index('Boarding')
tratimerd= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\TravelTimeDN.csv").set_index('Travel Time')


alightdr= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\alighting_rate_UP.csv").set_index('Alighting')
boarddr= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\Boarding_rate_UP.csv").set_index('Boarding')
tratimedr= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\TravelTimeUP.csv").set_index('Travel Time')

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#                                                           3.2.1 WAITING TIME, FAILS TO BOARD, TRAVEL TIME + PENALTY   GARIA TO AIRPORT

#-------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------PASSENEGR WAITING-----------------------------------------------------------------------------

arrivalraterd= passengerarrivalrd/(hrinperiod*60)
#print(arrivalrate)passengerarrivaldr

pass_arrivingrd= arrivalraterd[:].multiply(headwayrd, axis="index")      #IMPORTANT CODE for Single column of headwayrd2 multiplied with multiple column of arrivalrate
pass_arrivingrd=np.ceil(pass_arrivingrd[:].multiply(frequencyrd, axis="index")*hrinperiod)
print(f'\nTable of Passenger arriving at bus stops G-A:\n',pass_arrivingrd.to_string())

Tot_pass_arrivingrd= np.ceil(pass_arrivingrd.sum(axis = 1, skipna= True))
#Tot_pass_arrivingrd= np.ceil(Tot_pass_arrivingrd.sum(axis = 0, skipna= True))
print(f'\n--------------------------------------------------------------------')
print(f'No. of Passengers arriving at Bus stops A-G is :',Tot_pass_arrivingrd)
print(f'--------------------------------------------------------------------')
#---------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------PASSENGER LOST--------------------------------------------------------------------------------

#print(dwelling)
#  IMP CODE to sum of all row wise Total dwelling= np.floor(dwelling.sum(axis = 1, skipna= True))

pass_boardingrd= (boardrd[:].multiply(pass_arrivingrd, axis="index"))
#pass_boarding= (pass_boarding[:].multiply(freqrd2, axis="index"))

pass_alightingrd= (alightrd[:].multiply(pass_arrivingrd, axis="index"))
#pass_alighting= (pass_alighting[:].multiply(freqrd2, axis="index"))

#print(f'Passenger boarding at all stops',pass_boardingrd)
#print(f'Passenger Alighting at all stops',pass_alightingrd)

dwellingsrd=pass_boardingrd-pass_alightingrd
#freqdr[freqdr>frequencydefault] = frequencydefault

#dwellingsrd= dwellingsrd[:].multiply(frequencyrd, axis="index")*hrinperiod

dwellingsrd=abs(np.ceil(dwellingsrd.cumsum(axis = 1, skipna = True)))
dwellingsrd=dwellingsrd. dropna()

for i in range(0, len(dwellingsrd.index)):
    for j in range(0, len(dwellingsrd.columns)):
        if dwellingsrd.iloc[i,j]>=(cob*(frequencyrd[i])):
            dwellingsrd.iloc[i,j]=(cob*(frequencyrd[i]))
        else:
            pass

#####dwellingsrd=dwellingsrd.sum(axis = 1, skipna= True)
print(f'\nTable of No.of people able to board the bus G_A:\n',dwellingsrd.to_string())



Totdwellingsrd=dwellingsrd.sum(axis = 1, skipna= True)
print(f'No of people who can board is :',Totdwellingsrd)

passcantboardrd=pass_arrivingrd-dwellingsrd
passcantboardrd[passcantboardrd<0] = 0

print(f"\nTable of people who can't board is :\n",(passcantboardrd).to_string())


#print(f'\nNo of people who cant board is',passcantboardrd)

Totpasscantboardrd= abs(np.ceil(passcantboardrd).sum(axis = 1, skipna= True))
#Totpasscantboardrd[Totpasscantboardrd<0] = 0
print(f"Total No of people who can't board the bus due to crowding G-A is :",Totpasscantboardrd)
 #IMPORTANT PASSENGER LOST
#---------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------TOTAL PASSENGER WAITING-----------------------------------------------------------------------
#print(f'this one',headwayrd)
#print(Tot_pass_arrivingrd)
#print(arrivalraterd)


#Tot_pass_wait_timerd= 1/2 * (arrivalraterd[:]).multiply(headwayrd, axis="index") + Totpasscantboardrd

pass_wait_timerd= 0.5*(arrivalraterd[:]).multiply(headwayrd, axis="index")  #+passcantboardrd
pass_wait_timerd= (pass_wait_timerd[:]).multiply(headwayrd, axis="index")
pass_wait_timerd=pass_wait_timerd+passcantboardrd

print(f"\nTable of time passengers are spending while waiting for bus G-A (min) :\n",pass_wait_timerd.to_string())
Tot_pass_wait_timerd=pass_wait_timerd.sum(axis = 1, skipna= True)
#Tot_pass_wait_timerd=Tot_pass_wait_timerd.sum(axis = 0, skipna= True)
print(f'Total passenger waiting time (min) G-A is :',Tot_pass_wait_timerd.round(0))
 #IMPORTANT TOTAL PASSENGER WAITING
#---------------------------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------In VEHICLE TRAVEL TIME------------------------------------------------------------------------

#invehtime= dwelling.mul(distancerd)

#value_of_time= pd.read_csv(r'C:\Users\Ashish\Documents\IIT\thesis\PYTHON\DATABASE\valueoftimerd.csv').set_index('Value of Time (Raipur - Durg) (Rupee)')
print(dwellingsrd)
print(tratimerd)
print(dwellingsrd.iloc[0,0])
print(tratimerd.iloc[0,0])

invehtimerd= pd.DataFrame((dwellingsrd.values*tratimerd.values), columns=dwellingsrd.columns, index=dwellingsrd.index)

print(f'\nTable of Invehicle waiting time (min) G-A:\n',invehtimerd.to_string())
#invehtimerd= np.ceil(invehtimerd.sum())
Totalinvehtimerd= np.ceil(invehtimerd.sum(axis=1))
print(f'Total Invehicle waiting time G-A (min) is :',Totalinvehtimerd)
print("heeeee")

 # IMPORTANT In VEHICLE TRAVEL TIME
#---------------------------------------------------------------------------------------------------------------------------------------------------------









#-------------------------------------------------------------------------------------------------------------------------------------------------------

#                                                           3.2.2 WAITING TIME, FAILS TO BOARD, TRAVEL TIME + PENALTY  AIRPORT TO GARIA

#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------PASSENEGR WAITING-----------------------------------------------------------------------------

arrivalratedr= passengerarrivaldr/(hrinperiod*60)
#print(arrivalrate)passengerarrivaldr

pass_arrivingdr= arrivalratedr[:].multiply(headwaydr, axis="index")      #IMPORTANT CODE for Single column of headwayrd2 multiplied with multiple column of arrivalrate
pass_arrivingdr=np.ceil(pass_arrivingdr[:].multiply(frequencydr, axis="index")*hrinperiod)
print(f'\nTable of Passenger arriving at bus stops A-G:\n',pass_arrivingdr.to_string())

Tot_pass_arrivingdr= np.ceil(pass_arrivingdr.sum(axis = 1, skipna= True))
#Tot_pass_arrivingrd= np.ceil(Tot_pass_arrivingrd.sum(axis = 0, skipna= True))
print(f'\n--------------------------------------------------------------------')
print(f'No. of Passengers arriving at Bus stops A-G is :',Tot_pass_arrivingdr)
print(f'--------------------------------------------------------------------')
#---------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------PASSENGER LOST--------------------------------------------------------------------------------

#print(dwelling)
#  IMP CODE to sum of all row wise Total dwelling= np.floor(dwelling.sum(axis = 1, skipna= True))

pass_boardingdr= (boarddr[:].multiply(pass_arrivingdr, axis="index"))
#pass_boarding= (pass_boarding[:].multiply(freqrd2, axis="index"))

pass_alightingdr= (alightdr[:].multiply(pass_arrivingdr, axis="index"))
#pass_alighting= (pass_alighting[:].multiply(freqrd2, axis="index"))

#print(f'Passenger boarding at all stops',pass_boardingrd)
#print(f'Passenger Alighting at all stops',pass_alightingrd)

dwellingsdr=pass_boardingdr-pass_alightingdr
#freqdr[freqdr>frequencydefault] = frequencydefault

#dwellingsrd= dwellingsrd[:].multiply(frequencyrd, axis="index")*hrinperiod

dwellingsdr=abs(np.ceil(dwellingsdr.cumsum(axis = 1, skipna = True)))


for i in range(0, len(dwellingsdr.index)):
    for j in range(0, len(dwellingsdr.columns)):
        if dwellingsdr.iloc[i,j]>=(cob*(frequencydr[i])):
            dwellingsdr.iloc[i,j]=(cob*(frequencydr[i]))
        else:
            pass

#####dwellingsrd=dwellingsrd.sum(axis = 1, skipna= True)
print(f'\nTable of No.of people able to board the bus A-G:\n',dwellingsdr.to_string())



Totdwellingsdr=dwellingsdr.sum(axis = 1, skipna= True)
print(f'No of people who can board is :',Totdwellingsdr)

passcantboarddr=pass_arrivingdr-dwellingsdr
passcantboarddr[passcantboarddr<0] = 0

print(f"\nTable of people who can't board is :\n",(passcantboarddr).to_string())


#print(f'\nNo of people who cant board is',passcantboardrd)

Totpasscantboarddr= abs(np.ceil(passcantboarddr).sum(axis = 1, skipna= True))
#Totpasscantboardrd[Totpasscantboardrd<0] = 0
print(f"Total No of people who can't board the bus due to crowding A-G is :",Totpasscantboarddr)
 #IMPORTANT PASSENGER LOST
#---------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------TOTAL PASSENGER WAITING-----------------------------------------------------------------------
#print(f'this one',headwayrd)
#print(Tot_pass_arrivingrd)
#print(arrivalraterd)


#Tot_pass_wait_timerd= 1/2 * (arrivalraterd[:]).multiply(headwayrd, axis="index") + Totpasscantboardrd

pass_wait_timedr= 0.5*(arrivalratedr[:]).multiply(headwaydr, axis="index")  #+passcantboardrd
pass_wait_timedr= (pass_wait_timedr[:]).multiply(headwaydr, axis="index")
pass_wait_timedr=pass_wait_timedr+passcantboarddr

print(f"\nTable of time passengers are spending while waiting for bus A-G (min) :\n",pass_wait_timedr.to_string())
Tot_pass_wait_timedr=pass_wait_timedr.sum(axis = 1, skipna= True)
#Tot_pass_wait_timerd=Tot_pass_wait_timerd.sum(axis = 0, skipna= True)
print(f'Total passenger waiting time (min) A-G is :',Tot_pass_wait_timedr.round(0))
 #IMPORTANT TOTAL PASSENGER WAITING
#---------------------------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------In VEHICLE TRAVEL TIME------------------------------------------------------------------------

#invehtime= dwelling.mul(distancerd)

#value_of_time= pd.read_csv(r'C:\Users\Ashish\Documents\IIT\thesis\PYTHON\DATABASE\valueoftimerd.csv').set_index('Value of Time (Raipur - Durg) (Rupee)')

invehtimedr= pd.DataFrame((dwellingsdr.values*tratimedr.values), columns=dwellingsdr.columns, index=dwellingsdr.index)

print(f'\nTable of Invehicle waiting time (min) A-G:\n',invehtimedr.to_string())
#invehtimerd= np.ceil(invehtimerd.sum())
Totalinvehtimedr= np.ceil(invehtimedr.sum(axis=1))
print(f'Total Invehicle waiting time A-G (min) is :',Totalinvehtimedr)
print("heeeee")

 # IMPORTANT In VEHICLE TRAVEL TIME
#---------------------------------------------------------------------------------------------------------------------------------------------------------


















































#---------------------------------------------------------------------------------------------------------------------------------------------------------

#                                                           3.3  COSTING OF BUS WAITING TIME, FAILS TO BOARD, TRAVEL TIME + OPERATOR PENALTY

#---------------------------------------------------------------------------------------------------------------------------------------------------------


#print(Tot_pass_wait_time)
# -----------------------------------------------------VARIABLE COSTING OF BUS WAITING TIME --------------------------------------------------------------

if headwayrd[0] <= 10:
    costunit_waitingtime=costunit_waitingtime/(1)
elif headwayrd[0] <= 15:
    costunit_waitingtime=costunit_waitingtime/(1 + 0.05*0.05)
elif headwayrd[0] <= 20:
    costunit_waitingtime = costunit_waitingtime/(1 + 0.1*0.1)
elif headwayrd[0] <= 25:
    costunit_waitingtime = costunit_waitingtime / (1 + 0.15*0.15)
else:
    costunit_waitingtime = costunit_waitingtime/(1 + 0.20*0.20)
#print(costunit_waitingtime)

# -------------------------------------------------------------------------------------------------------------------------------------------------------
  #IMPORTANT VARIABLE COSTING OF BUS WAITING TIME
print(f"\n----------------------------------------------------------------------------"
      f"\nOverall social cost of bus operation between Bag bazaar - Garia"
      f"\n----------------------------------------------------------------------------")

#COST OF INVEHICLE WAITING TIME W.R.T CROWDING.

load_factdr =(dwellingsdr[:].divide(dob*frequencydr, axis="index"))
load_factrd= (dwellingsrd[:].divide(dob*frequencyrd, axis="index"))

cost_invehicledr= load_factdr
for i in range(0, len(load_factdr.index)):
    for j in range(0, len(load_factdr.columns)):
        if load_factdr.iloc[i,j] <=1:
            cost_invehicledr.iloc[i,j] = 0
        elif load_factdr.iloc[i,j] >1 and load_factdr.iloc[i,j] <1.75:
            cost_invehicledr.iloc[i, j] = ( invehtimedr.iloc[i,j]*.4)
        else:
            cost_invehicledr.iloc[i, j] = ( invehtimedr.iloc[i, j] * .8)

cost_invehiclerd = load_factrd
for i in range(0, len(load_factrd.index)):
    for j in range(0, len(load_factrd.columns)):
        if load_factrd.iloc[i,j] <=1:
            cost_invehiclerd.iloc[i,j] = 0
        elif load_factrd.iloc[i,j] >1 and load_factrd.iloc[i,j] <1.75:
            cost_invehiclerd.iloc[i, j] = ( invehtimerd.iloc[i, j] * .4)
        else:
            cost_invehiclerd.iloc[i, j] = (invehtimerd.iloc[i, j] * .8)

Total_cost_invehtimerd= np.ceil(cost_invehiclerd.sum(axis=1))
Total_cost_invehtimedr= np.ceil(cost_invehicledr.sum(axis=1))

#------------------------------------------------------#

cuserrd= (Totpasscantboardrd)*(costunit_cantboard)+ (Tot_pass_wait_timerd)*(costunit_waitingtime) + (Total_cost_invehtimerd)
coperatorrd= (Totpasscantboardrd)*(penalty)#+fixedcostrd
print(f"User Cost for bus operation in Raipur to Durg direction:          ₹",cuserrd)#.round(0))
print(f"Operator Cost for bus operation in Raipur to Durg direction:       ₹",coperatorrd)#.round(0))

cuserdr= (Totpasscantboarddr)*(costunit_cantboard)+ (Tot_pass_wait_timedr)*(costunit_waitingtime) + (Total_cost_invehtimedr)
coperatordr= (Totpasscantboarddr)*(penalty)#+fixedcostdr
print(f"User Cost for bus operation in Durg to Raipur direction:          ₹",cuserdr)#.round(0))
print(f"Operator Cost for bus operation in Durg to Raipur direction:       ₹",coperatordr)#.round(0))

#cuserrd= (Totpasscantboardrd)*(costunit_cantboard)+ (Tot_pass_wait_timerd)*(costunit_waitingtime) + (Totalinvehtimerd) *(costunit_invehtime)
#coperatorrd= (Totpasscantboardrd)*(penalty)#+fixedcostrd
#print(f"User Cost for bus operation in Raipur to Durg direction:          ₹",cuserrd)#.round(0))
#print(f"Operator Cost for bus operation in Raipur to Durg direction:       ₹",coperatorrd)#.round(0))

#cuserdr= (Totpasscantboarddr)*(costunit_cantboard)+ (Tot_pass_wait_timedr)*(costunit_waitingtime) + (Totalinvehtimedr) *(costunit_invehtime)
#coperatordr= (Totpasscantboarddr)*(penalty)#+fixedcostdr
#print(f"User Cost for bus operation in Durg to Raipur direction:          ₹",cuserdr)#.round(0))
#print(f"Operator Cost for bus operation in Durg to Raipur direction:       ₹",coperatordr)#.round(0))

costoverallrd= pd.DataFrame({'Time Period':freqrd.index, 'User Cost':cuserrd,'Operator Cost':coperatorrd,'Overall_Social_cost':cuserrd+coperatorrd }).set_index('Time Period')
costoveralldr= pd.DataFrame({'Time Period':freqdr.index, 'User Cost':cuserdr,'Operator Cost':coperatordr,'Overall_Social_cost':cuserdr+coperatordr }).set_index('Time Period')

print(f'\nOverall cost of running a bus service in Bag bazaar to Garia  direction is:     ₹\n',costoverallrd)#.round(0))
print(f'Overall cost of running a bus service in  Garia to Bag bazaar direction is:     ₹\n',costoveralldr)#.round(0))

file_name= 'cost of running a bus service in Bag bazaar to Garia .xlsx'
costoverallrd.to_excel('cost of running a bus service in Bag bazaar to Garia .xlsx')

file_name= 'cost of running a bus service in Garia to Bag bazaar  .xlsx'
costoveralldr.to_excel('cost of running a bus service in Garia to Bag bazaar .xlsx')

overallcost=pd.concat([costoverallrd.iloc[:,2], costoveralldr.iloc[:,2]],axis=0)
print(overallcost)
sumoverallcost=np.sum(overallcost)    # for comparision

# -----------------------------------------------------FREQUENCY RANGE FOR ITERATION IN GA--------------------------------------------------------------

frequencyrdmin=max_pass_periodrd/cob

frequencyrdmax=max_pass_periodrd/dob

frequencydrmin=max_pass_periodrd/cob

frequencydrmax=max_pass_periodrd/dob

frequencyrd= pd.DataFrame({'Time Period':freqrd.index, 'Frequency Min':frequencyrdmin, 'Frequency Max':frequencyrdmax}).set_index('Time Period')
frequencydr= pd.DataFrame({'Time Period':freqrd.index, 'Frequency Min':frequencydrmin, 'Frequency Max':frequencydrmax}).set_index('Time Period')

frequencycomb=pd.concat([frequencyrd, frequencydr],axis=0)
print(frequencycomb)




#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           4.0   O P T I M I Z A T I O N
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           4.A INITIAL SETTINGS  Matrix of High and Lof frequency in all 18 period direction wise togenther
#-------------------------------------------------------------------------------------------------------------------------------------------------------







#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           4.1 GENETIC ALGORITHM MODEL RAIPUR TO DURG
#-------------------------------------------------------------------------------------------------------------------------------------------------------

'''
The y=target is to maximize this equation ASAP:
    y = w1x1+w2x2+w3x3+w4x4+w5x5+6wx6
    where (x1,x2,x3,x4,x5,x6)=(4,-2,3.5,5,-11,-4.7)
    What are the best values for the 6 weights w1 to w6?
    We are going to use the genetic algorithm for the best possible values after a number of generations.
'''

# Inputs of the equation.
equation_inputs =[overallcost]                                               #[costoverall['Overall Cost(₹)']]                  #[infreqrd2['Initial Frequency2']]
print(np.sum(equation_inputs))
# Number of the periods we are looking to optimize.
num_weights = 32

'''
Genetic algorithm parameters:
    Mating_pool_size
    Population_size
'''
sol_per_pop = 16
num_parents_mating = 8
print("\n---------------------------------------------------------------------------\nInitiating Genetic Algorithm for Raipur to Durg to Optimise Overall Cost(₹)\n---------------------------------------------------------------------------")

# Defining the population size.
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop (chromosome) where each chromosome has num_weights (genes).
#Creating the initial population.

#--------------------Lower and Upper bound values of frequency based on Confidence interval of 0.90 --------------------------
'''
confidence_level = 0.95
degrees_freedom = frequencycomb.size - 1
sample_mean = np.mean(frequencycomb)
sample_standard_error = scipy.stats.sem(frequencycomb)
frequencyrange = scipy.stats.t.interval(confidence_level, degrees_freedom, sample_mean, sample_standard_error)
print(frequencyrange)
'''
#------------------------------------------------------------------------------------------------------------------------------


new_populationrd = np.random.uniform(low=frequencycomb.iloc[:,0], high=frequencycomb.iloc[:,1], size=pop_size)        ## NEED TO HAVE A SYNTAX THAT GENERATE MIN FREQUENCY AND MAX FREQUENCY INSTEAD LOW AND HIGH MANUAL INPUT
print(new_populationrd)
b=new_populationrd/sol_per_pop

    #print(b)
b=np.sum(b, axis=1)
    #print(b)
    #b=np.sum(b, axis=0)/sol_per_pop
b=np.min(b)#+0.2
    #print(b)

num_generations = 5
for generation in range(num_generations):
    print("\nGeneration : ", generation)
    # Measuring the fitness of each chromosome in the population.
    fitness = ga.cal_pop_fitness(equation_inputs, new_populationrd)

    # Selecting the best parents in the population for mating.
    parents = ga.select_mating_pool(new_populationrd, fitness, num_parents_mating)

    # Generating next generation using crossover.
    offspring_crossover = ga.crossover(parents, offspring_size=(pop_size[0]-parents.shape[0], num_weights))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = ga.mutation(offspring_crossover)

    # Creating the new population based on the parents and offspring.
    new_populationrd[0:parents.shape[0], :] = parents
    new_populationrd[parents.shape[0]:, :] = offspring_mutation
    # The best result in the current iteration.


#IMP    print("Best result : ₹",np.min(np.sum(new_populationrd*equation_inputs, axis=1)/(sol_per_pop*b)).round(0))            #NOT TO DISTURB
    #print("Best result : ₹", (np.sum(new_populationrd * equation_inputs)))# / (sol_per_pop * b)).round(0))


    gacost= pd.DataFrame({'Time': frequencycomb.index, 'col1': new_populationrd[0], 'col2': new_populationrd[1],'col3': new_populationrd[2],'col4': new_populationrd[3],
                                                      'col5': new_populationrd[4], 'col6': new_populationrd[5],'col7': new_populationrd[6],'col48': new_populationrd[7],
                                                      'col9': new_populationrd[8], 'col10': new_populationrd[9], 'col11': new_populationrd[10],'col12': new_populationrd[11],
                                                      'col13': new_populationrd[12], 'col4': new_populationrd[13], 'col15': new_populationrd[14],'col16': new_populationrd[15]}).set_index('Time')
    gacost = gacost.min(axis = 1)

    print("Best result : ₹", gacost.mul(equation_inputs[0])) # / (sol_per_pop * b)).round(0))
    optimumcostrd=(np.sum(gacost.mul(equation_inputs[0]))/sol_per_pop * b).round(0)
    print("Best result : ₹", optimumcostrd)

    #print("Best result : ₹", (new_populationrd))    # * equation_inputs))


# Getting the best solution after iterating finishing all generations.
# At first, the fitness is calculated for each solution in the final generation.
fitness = ga.cal_pop_fitness(equation_inputs, new_populationrd)
# Then return the index of that solution corresponding to the best fitness.
best_match_idx = np.where(fitness == np.min(fitness))
best_match_idx=best_match_idx
bestsolution=(new_populationrd[best_match_idx, :]).round(2)
bestsolfitnessrd=np.ceil(fitness[best_match_idx])


a=np.sum(bestsolution, axis=0)
a=np.sum(a, axis=0)
ahalf=np.sort(a[0:8])
bhalf=np.sort(a[8:16])
chalf=np.sort(a[16:24])
dhalf=np.sort(a[24:32])
#print(np.concatenate((np.sort(a[0:8]), np.sort(a[9:16]))))
ss = sorted(ahalf)
#print(ss)
ss1 = ss[::2]
#print(ss1)
ss2 = ss[::-2]
#print(ss2)
ss3=ss1+ss2
#print(ahalf)
#print(ss3)
pp = sorted(bhalf)
#print(pp)
pp1 = pp[::2]
#print(pp1)
pp2 = pp[::-2]
#print(pp2)
pp3=pp1+pp2
#print(ahalf)
#print(pp3)
qq = sorted(chalf)

qq1 = qq[::2]

qq2 = qq[::-2]

qq3=qq1+qq2

rr = sorted(dhalf)

rr1 = rr[::2]

rr2 = rr[::-2]

rr3=rr1+rr2

optimisedfreqrd= ss3+pp3+qq3+rr3


Optimisedsolution= []
for item in optimisedfreqrd:
    if item < 1.5:
        item = 1.5
    Optimisedsolution.append(item)
optimisedfreqrd = Optimisedsolution
print("\n---------------------------------------------------------------------------\nOutput: Genetic Algorithm Optimization for Overall Social Cost\n---------------------------------------------------------------------------")

#print("\nOptimised Frequency for Raipur to Durg: ",optimisedfreqrd)
print("\nOptimised Frequency for Bag bazaar to Garia : ",optimisedfreqrd[0:8])
print(f'                                        ',optimisedfreqrd[8:16])
print("\nOptimised Frequency for Garia to Bag bazaar: ",optimisedfreqrd[16:24])
print(f'                                        ',optimisedfreqrd[24:32])
#print(np.concatenate((np.sort(a[0:8]), np.sort(a[9:16]))))
'''
x= ['6:00AM','7:00AM','8:00AM','9:00AM','10:00AM','11:00AM','12:00PM','13:00PM','14:00PM','15:00PM','16:00PM','17:00PM','18:00PM','19:00PM','20:00PM','21:00PM']
plt.plot(x,optimisedfreqrd, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12)
plt.show()
'''
#print(b)

print("Optimum overall cost of Bus service in both Direction:   ₹",optimumcostrd)
costredcutionrd=optimumcostrd/sumoverallcost*100
print(f'(Cost reduction: ',100-float(np.asarray(costredcutionrd).round(0)),'%,  i.e: ₹',(sumoverallcost-optimumcostrd).round(0),')')



#-------------------------------------------------------------------------------------------------------------------------------------------------------

#                                                           TOTAL SOCIAL COSTING IN ALL DIRECTION

#-------------------------------------------------------------------------------------------------------------------------------------------------------

print('Fixed cost from fleet sizes:                                       ₹',(overallfixedcost).round(0))
print('---------------------------------------------------------------------------------------')
print('Total cost of optimised Bus operation in both Direction:           ₹',(optimumcostrd + overallfixedcost).round(0))
print('---------------------------------------------------------------------------------------')





#-------------------------------------------------------------------------------------------------------------------------------------------------------

#                                                           OPTIMISED FREQUENCY AND HEADWAY

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#print(optimisedfreqrd)

optimisedheadwayrd = [60 /item for item in optimisedfreqrd]

optimisedheadwayrd = [round(num, 0) for num in optimisedheadwayrd]



optimisedfreqrd=np.array_split(optimisedfreqrd, 2)

optimisedheadwayrd=np.array_split(optimisedheadwayrd, 2)

print("------------------------------------------------------"
      "\nOptimised Frequency and Headway in both Direction is :"
      "\n------------------------------------------------------")


#print(optimisedfreqrd)
#print(optimisedheadwayrd)

#optimisedfreqrd= pd.DataFrame({'Time Period':optimisedfreqrd.index, 'Optimised Frequency G-A':optimisedfreqrd[0],'Optimised Headway A-G':optimisedheadwayrd[0], 'Optimised Frequency D-R':optimisedfreqrd[1],'Optimised Headway D-R':optimisedheadwayrd[1]}).set_index('Time Period')
optimisedfreqrd= pd.DataFrame({'Time Period':frequencyrd.index, 'Optimised Frequency B-G':optimisedfreqrd[0],'Optimised Headway B-G':optimisedheadwayrd[0], 'Optimised Frequency G-B':optimisedfreqrd[1],'Optimised Headway G-B':optimisedheadwayrd[1]}).set_index('Time Period')

#print(optimisedfreqrd)
file_name = 'optimised frequency and headway.xlsx'
optimisedfreqrd.to_excel('optimised frequency and headway.xlsx')

print(optimisedfreqrd.to_string())




#_______________________________________________________________________________________________________________________
#                                                   fleet Size Estimation
#_______________________________________________________________________________________________________________________

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2. F L E E T   S I Z E   C A L C U L A T I O N
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------



frequencyrd=optimisedfreqrd['Optimised Frequency B-G']
#print(frequencyrd)
frequencydr=optimisedfreqrd['Optimised Frequency G-B']

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.1.1 Departure time calculation   GARIA AIRPORT
#-------------------------------------------------------------------------------------------------------------------------------------------------------

timeo_periodrd= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\tmeperiodDN.csv", header=0)
#print(time_periodrd)
timeo_periodrd['frequency']= frequencyrd.values
#print(frequencyrd)
#print(timeo_periodrd)
timeo_periodrd['Headway_in_hours']=(1/(frequencyrd.values)).round(2)
#print(timeo_periodrd)

departuretimerd = pd.DataFrame()

for ind,col in timeo_periodrd.iterrows():
    for f in range(0,int(timeo_periodrd.iloc[ind,1])):
        if ind==0:
           departuretimerd = departuretimerd.append({'Departure': (timeo_periodrd.iloc[ind,0])/100+ ((f*timeo_periodrd.iloc[ind,2])) ,'From': A },ignore_index=True)     # Replace ((f*time_periodrd.iloc[ind,2]))*60/100

        else:
            departuretimerd = departuretimerd.append({'Departure': (departuretimerd.iloc[-1,0]) + ((timeo_periodrd.iloc[ind, 2])), 'From': A}, ignore_index=True)  # Replace ((f*time_periodrd.iloc[ind,2]))*60/100

    while ind < (len(timeo_periodrd.index)-2) :
        headway_avg = (timeo_periodrd.iloc[ind, 2] + timeo_periodrd.iloc[ind + 1, 2]) / 2
        temp_departure = departuretimerd.iloc[-1, 0] + headway_avg
        departuretimerd = departuretimerd.append({'Departure': temp_departure, 'From': A}, ignore_index=True)
        break



#print(timeo_periodrd.iloc[0,0])
#print(timeo_periodrd.iloc[0,1])
#for ind,col in timeo_periodrd.iterrows():
    #for f in range(0,int(timeo_periodrd.iloc[ind,1])):
   #    departuretimerd = departuretimerd.append({'Departure': (timeo_periodrd.iloc[ind,0])/100+ ((f*timeo_periodrd.iloc[ind,2])) ,'From': A },ignore_index=True)     # Replace ((f*time_periodrd.iloc[ind,2]))*60/100

        #print(f)
        #if f < frequencyrd.iloc[ind,2]:
       #df.loc[f,"Departure"]= (col['Time'])/100 + (ind * col["Headway_in_hours"])
#for ind in df.iterrows():
    #df= pd.to_datetime(df)
#print(departuretimerd)
#--------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.1.2 Departure time calculation  AIRPORT GARIA
#-------------------------------------------------------------------------------------------------------------------------------------------------------

timeo_perioddr= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\tmeperiodUP.csv", header=0)
#print(time_perioddr)
timeo_perioddr['frequency']= frequencydr.values
#print(time_perioddr)
timeo_perioddr['Headway_in_hours']=(1/(frequencydr.values)).round(2)
#print(time_perioddr)

departuretimedr = pd.DataFrame()
for ind,col in timeo_perioddr.iterrows():
    for f in range(0,int(timeo_perioddr.iloc[ind,1])):
        if ind==0:
            departuretimedr = departuretimedr.append({'Departure': (timeo_perioddr.iloc[ind,0])/100+ ((f*timeo_perioddr.iloc[ind,2]))+0.005,'From': B },ignore_index=True)     # Replace ((f*time_periodrd.iloc[ind,2]))*60/100

        else:
            departuretimedr = departuretimedr.append({'Departure': (departuretimedr.iloc[-1,0]) + ((timeo_perioddr.iloc[ind, 2]))+0.005,'From': B }, ignore_index=True)  # Replace ((f*time_periodrd.iloc[ind,2]))*60/100

    while ind < (len(timeo_perioddr.index)-2) :
        headway_avg = (timeo_perioddr.iloc[ind, 2] + timeo_perioddr.iloc[ind + 1, 2]) / 2
        temp_departure = departuretimedr.iloc[-1, 0] + headway_avg+0.005
        departuretimedr = departuretimedr.append({'Departure': temp_departure, 'From': B}, ignore_index=True)
        break
#for ind,col in timeo_perioddr.iterrows():
    #for f in range(0,int(timeo_perioddr.iloc[ind,1])):
        #departuretimedr = departuretimedr.append({'Departure': (timeo_perioddr.iloc[ind,0])/100+ ((f*timeo_perioddr.iloc[ind,2])) +0.005,'From': B },ignore_index=True)     # Replace ((f*time_periodrd.iloc[ind,2]))*60/100
        #print(f)
        #if f < frequencydr.iloc[ind,2]:
        #df.loc[f,"Departure"]= (col['Time'])/100 + (ind * col["Headway_in_hours"])
#for ind in df.iterrows():
    #df= pd.to_datetime(df)
#print(departuretimedr)
#--------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.2.1 Travel time GARIA AIRPORT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
traveltimerd= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\TravelTimeDN.csv")
traveltimerd.drop('Travel Time', axis=1, inplace= True)
sumtraveltimerd=traveltimerd.sum(axis = 1, skipna= True)

arrivaltimerd = pd.DataFrame()
for ind in range(0,len(sumtraveltimerd.index)):
    for f in range(0,int(timeo_periodrd.iloc[ind,1])):
        arrivaltimerd = arrivaltimerd.append({'TT_to_Garia': sumtraveltimerd[ind]/60,'From': A},ignore_index=True).round(2)
#print(arrivaltimerd)



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.2.2 Travel time  AIRPORT GARIA
#-------------------------------------------------------------------------------------------------------------------------------------------------------
traveltimedr= pd.read_csv(r"D:\S21 Data\Database for timetable prediction\TravelTimeUP.csv")
traveltimedr.drop('Travel Time', axis=1, inplace= True)
sumtraveltimedr=traveltimedr.sum(axis = 1, skipna= True)
#print(traveltimedr.to_string())
arrivaltimedr = pd.DataFrame()
for ind in range(0,len(sumtraveltimedr.index)):
    for f in range(0,int(timeo_perioddr.iloc[ind,1])):
        arrivaltimedr = arrivaltimedr.append({'TT_to_Bag_Bazaar': sumtraveltimedr[ind]/60,'From': B},ignore_index=True).round(2)
#print(arrivaltimedr)



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           2.3 Vehicle Scheduling ALL DIRECTION
#-------------------------------------------------------------------------------------------------------------------------------------------------------
departuretimerd['TT to Garia']= arrivaltimerd.TT_to_Garia
departuretimedr['TT to Bag Bazaar']= arrivaltimedr.TT_to_Bag_Bazaar

departuretime = pd.concat([departuretimerd, departuretimedr], ignore_index=True)
departuretime = departuretime.sort_values(by=['Departure']).reset_index(drop=True)
departuretime['Arrival']=np.zeros(departuretime.shape[0], dtype=int)
tempdeparturetime=departuretime
for i in range(0, departuretime.shape[0]):
    if departuretime.iloc[i,1] == "Bag bazaar":
        departuretime.iloc[i,4]= departuretime.iloc[i,0] + departuretime.iloc[i,2]
    else:
        departuretime.iloc[i,4] = departuretime.iloc[i,0] + departuretime.iloc[i,3]

departuretime["To"]= np.where(departuretime["From"] == "Bag bazaar" , 0, 1 )
departuretime['Fleet B']=np.zeros(departuretime.shape[0], dtype=int)
departuretime['Fleet G']=np.zeros(departuretime.shape[0], dtype=int)
departuretime['Pool B']=np.zeros(departuretime.shape[0], dtype=int)
departuretime['Pool G']=np.zeros(departuretime.shape[0], dtype=int)
for m in range(0,departuretime.shape[0]):#and departuretime.iloc[ind-1,3]=="Raipur":
    #print(departuretime.iloc[0,4].min() and departuretime.iloc[m, 5] == 1)
    if departuretime.iloc[m, 5] == 1 and departuretime.iloc[m,0] <= departuretime.iloc[:,4].min():
        departuretime.iloc[m, 7] = 1

    elif departuretime.iloc[m, 5] == 0 and departuretime.iloc[m,0] <= departuretime.iloc[:,4].min():
        departuretime.iloc[m, 6] = 1

    elif departuretime.iloc[m, 5] == 1 and departuretime.iloc[m,0] > departuretime.iloc[:,4].min():
        departuretime.iloc[m, 9] =1

        departuretime = departuretime.sort_values(["To", "Arrival"],ascending=[True, True])  # .replace(departuretime.iloc[0,4], 99)
        departuretime = departuretime.replace(departuretime.iloc[0, 4], 999)
        departuretime = departuretime.sort_index(ascending=True)

    elif departuretime.iloc[m, 5] == 0 and departuretime.iloc[m,0] > departuretime.iloc[:,4].min():
        departuretime.iloc[m, 8] = 1

        departuretime = departuretime.sort_values(["To", "Arrival"], ascending=[False, True])  # .replace(departuretime.iloc[0,4], 99)
        departuretime = departuretime.replace(departuretime.iloc[0, 4], 999)
        departuretime = departuretime.sort_index(ascending=True)
    else:
        departuretime.iloc[m, 6] = 1

#---------------------
departuretime["Departure"]=np.floor(tempdeparturetime["Departure"])+(tempdeparturetime["Departure"]- (np.floor(tempdeparturetime["Departure"])))/100*60
departuretime["Arrival"]= np.floor(tempdeparturetime["Arrival"])+(tempdeparturetime["Arrival"]- (np.floor(tempdeparturetime["Arrival"])))/100*60                          #str(tempdeparturetime["Arrival"](math.floor(time))) + ':' + str(tempdeparturetime["Arrival"]((time%(math.floor(time)))*60))
#---------------------
departuretime["To"]= np.where(departuretime["To"] == 0 , "Garia", "Bag bazaar" )
print(f'\n--------------------------------------------\n'
      f'Vehicle timetable as per Optimised Frequency :'
      f'\n--------------------------------------------\n',departuretime.sort_index(ascending=True).to_string())        #.to_string() is to Show all content  in the result window.  IMPORTANT TO KNOW
file_name= 'optimized timetable.xlsx'
departuretime.to_excel('optimized timetable.xlsx')


#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           3.  C O S T   C A L C U L A T I O N S   I N   A L L   D I R E C T I O N
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           3.1 FIXED COST CALCULATIONS ALL DIRECTIONs
#-------------------------------------------------------------------------------------------------------------------------------------------------------

busreq_at_raipur= departuretime['Fleet B'].sum()
busreq_at_durg=departuretime['Fleet G'].sum()
poolsize_at_raipur=departuretime['Pool B'].sum()
poolsize_at_durg=departuretime['Pool G'].sum()
#print(f'\n---------------------------------------\n'
   #   f'Vehicle Operation Details and Costing :'
    #  f'\n---------------------------------------')
#print(f'\nNo. of Bus required at Raipur Depot :',busreq_at_raipur,'\nNo. of Bus required at Durg Depot:',busreq_at_durg,'\n\nNo. of Bus reutilized from Pool at Raipur :',poolsize_at_raipur,"\nNo. of Bus reutilized from Pool at Durg :", poolsize_at_durg)

#print(f'\n---------------------------------------\n'
#      f'Vehicle Operation Details and Costing :'
 #     f'\n---------------------------------------')
#print(f"\nNo. of Bus required at Garia Depot : 8\nNo. of Bus required at Airport Depot:6\n\nNo. of Bus reutilized from Pool at Garia : 31\nNo. of Bus reutilized from Pool at Airport : 27")

print(f'\n---------------------------------------\n'
      f'Vehicle Operation Details and Costing :'
      f'\n---------------------------------------')
print(f'\nNo. of Bus required at Bag bazaar Depot :',busreq_at_raipur,'\nNo. of Bus required at Garia Depot:',busreq_at_durg,'\n\nNo. of Bus reutilized from Pool at Bag Bazaar :',poolsize_at_raipur,"\nNo. of Bus reutilized from Pool at Garia :", poolsize_at_durg)

