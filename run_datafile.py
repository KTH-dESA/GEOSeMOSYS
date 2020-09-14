import pandas as pd
import numpy as np
import os
from datetime import datetime
from build_data_file import *

##############################
##       Input data      ##
#############################

cd = os.getcwd()
df = pd.read_csv(cd +'/data/GIS_data.csv')
inputFileName = cd +'/base_file/Kenya_BIG_ALL_REF_200826_revF.txt'
file_object = cd +'/base_file/Kenya_BIG_ALL_REF_200826_revG.txt'
elec = pd.read_csv(cd +'/data/elec.csv')
trade = pd.read_csv(cd +'/data/capacitytoactivity.csv')
inputactivity = pd.read_csv(cd +'/data/inputactivity.csv', index_col=0)
demand = pd.read_csv(cd +'/data/demand.csv', index_col=0, header=0)
demand_urban = pd.read_csv(cd +'/data/demandprofile.csv', index_col=0, header=0)
demand_rural = pd.read_csv(cd +'/data/demandprofile_rural.csv', index_col=0, header=0)
capacityfactor_wind = pd.read_csv(cd +'/data/capacityfactor_wind.csv',index_col=None)
capacityfactor_wind['date'] = pd.to_datetime(capacityfactor_wind['date'],errors='coerce', format='%Y/%m/%d %H:%M')
capacityfactor_wind.index = capacityfactor_wind['date']
capacityfactor_wind = capacityfactor_wind.drop(columns=['date'])
capacityfactor_wind.columns = pd.to_numeric(capacityfactor_wind.columns)
capacityfactor_solar = pd.read_csv(cd +'/data/capacityfactor_solar.csv', index_col=None)
capacityfactor_solar['0'] = pd.to_datetime(capacityfactor_solar['0'], errors='coerce', format='%Y/%m/%d %H:%M')
#capacityfactor_solar = capacityfactor_solar.drop(columns=['date'])
capacityfactor_solar.columns = pd.to_numeric(capacityfactor_solar.columns)
capacityfactor_solar = pd.read_csv(cd +'/data/capacityfactor_solar.csv', header=0)
capitalcost_RET = pd.read_csv(cd +'/data/capitalcost_RET.csv', index_col=0, header=0)
capitalcost_RET.index = capitalcost_RET['CF']
trade_cost = pd.read_csv(cd +'/data/capitalcost.csv')

wind_power = 600      #600 kW from renewable ninja
solar_power = 1000  #1000W
batteryCF = 900  #900W
battery13h = 13  #hours that the battery is operational
battery8h = 8 #hours that the battery is operational

timesliceDN = '06:00'
timesliceDE = '17:00'
timesliceED = '18:00'
timesliceEN = '22:00'
timesliceNE = '23:00'
timesliceND = '05:00'
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
startyear = 2012
endyear = 2040

###############################
##    Reset all values      ##
##############################
allLinesFromKenyaXy = ""
with open(inputFileName, "r") as inputFile:
   allLinesFromKenyaXy = inputFile.read()

outPutFile = allLinesFromKenyaXy

## functions to run
#outPutFile = capitalcost(df, outPutFile, elec, capitalcost_RET, trade_cost, wind_power, solar_power, capacityfactor_wind, capacityfactor_solar, startyear, endyear)
#outPutFile = capacityfactor_solar_battery8h(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar,
#                                            solar_power, wind_power,
#                                            timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE,
#                                            timesliceND, batteryCF,
#                                            battery13h, battery8h, startyear, endyear, months)
#outPutFile = capacityfactor_solar_battery13h(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar, solar_power, wind_power, timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE, timesliceND, batteryCF, battery13h, battery8h, startyear, endyear, months)
#outPutFile = capacityfactor_PV(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar, solar_power, wind_power, timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE, timesliceND, batteryCF, battery13h, battery8h, startyear, endyear, months)

#outPutFile = capacityfactor_wi(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar, solar_power, wind_power, timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE, timesliceND, batteryCF, battery13h, battery8h, startyear, endyear, months)

#outPutFile = capacityfactor(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar, solar_power, wind_power, timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE, timesliceND, batteryCF, battery13h, battery8h, startyear, endyear)
#outPutFile = operational_life(df, elec, outPutFile)
#outPutFile = capacitytoactivity(trade,outPutFile)
#outPutFile = emissionactivity(df, outPutFile, startyear, endyear)
#outPutFile = variablecost(outPutFile, df, elec, startyear, endyear)
#outPutFile = totaltechnologyannualactivityupperlimit(df, outPutFile, startyear, endyear)
#outPutFile = SpecifiedDemandProfile(outPutFile, demand, demand_urban, demand_rural)
outPutFile = inputact(outPutFile, inputactivity, startyear, endyear)
#outPutFile = fixedcost(df, outPutFile, startyear, endyear, elec)
#outPutFile = specifiedannualdemand(outPutFile, demand)

#write data file
write_to_file(file_object, outPutFile)

