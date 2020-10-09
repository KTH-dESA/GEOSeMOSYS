import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime


def load_csvs(paths):
    basdir = os.getcwd()
    os.chdir(paths)
    onlyfiles = [f for f in listdir(paths) if isfile(join(paths, f))]
    dfs = {}  #.csv files
    param=[]  #list of parameters
    dict_df = {}
    for files in onlyfiles:
    #validate that the files are csv. Else the read function will not work
        if files.split('.')[1] == 'csv':
            dfs[files] = pd.read_csv(files, header=0)
            param.append(files.split('.')[0])
        else:
            print("You have mixed file types in you directory, please make sure all are .csv type!")
            os.chdir(basdir)
            exit()
    for i, value in enumerate(param):
        dict_df[param[i]] = dfs[param[i]+'.csv']
    os.chdir(basdir)
    return dict_df

def make_outputfile(path, param_file):
    inputFileName = path + param_file
    allLinesFromXy = ""
    with open(inputFileName, "r") as inputFile:
        allLinesFromXy = inputFile.read()
    outPutFile = allLinesFromXy
    return(outPutFile)

def functions_to_run(dict_df, outPutFile, startyear, endyear, region, modeofoperation):
    if 'operational_life' in dict_df:
        outPutFile = operational_life(outPutFile, dict_df['GIS_data'], region, dict_df['operational_life'])
    else:
        print('No operational_life file')
#################################################################################
    if 'fixed_cost' in dict_df:
        outPutFile = fixedcost(dict_df['GIS_data'], outPutFile, input_data, dict_df['fixed_cost'])
    else:
        print('No fixed_cost file')
#####################################################################################
    if 'total_annual_technology_limit' in dict_df:
        outPutFile = totaltechnologyannualactivityupperlimit(dict_df['GIS_data'], outPutFile, startyear, endyear,
                                                             region, dict_df['total_annual_technology_limit'])
    else:
        print('No total_annual_technology_limit file')

    if 'demand' in dict_df:
        outPutFile = specifiedannualdemand(outPutFile, dict_df['demand'], region, startyear, endyear)
    else:
        print('No demand file')
####################################################################################
    if 'capitalcost_RET' in dict_df:
        outPutFile = capitalcost_dynamic(dict_df['GIS_data'], outPutFile, dict_df['capitalcost_RET'],
                                         dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'], startyear,
                                         endyear, region)
    else:
        print('No capitalcost_RET file')
###########################################################################
    if 'capitalcost' in dict_df:
        outPutFile = capitalcost(dict_df['GIS_data'], outPutFile, dict_df['capitalcost'], startyear, endyear, region)
    else:
        print('No capitalcost file')

##########################################################
###########TIMESLICE parameters###############
    if 'battery' in dict_df:
        outPutFile = capacityfactor_solar_battery(elec, outPutFile, dict_df['GIS_data'], dict_df['capacityfactor_solar'], dict_df['input_data'], dict_df['battery'], startyear, endyear, months, region)
    else:
        print('No battery file')
################################################################################
    if 'capacityfactor_solar' in dict_df:
        outPutFile = capacityfactor_PV(elec, outPutFile, dict_df['GIS_data'], dict_df['capacityfactor_solar'], dict_df['input_data'], startyear, endyear,
                                       months, region)
    else:
        print('No capacityfactor_solar file')
###############################################################################
    if 'capacityfactor_wind' in dict_df:
        outPutFile = capacityfactor_wi(outPutFile, dict_df['GIS_data'],  dict_df['capacityfactor_wind'], dict_df['input_data'], startyear, endyear,
                                       months, region)
    else:
        print('No capacityfactor_wind file')
##############################################################################
    if 'capacitytoactivity' in dict_df:
        outPutFile = capacitytoactivity(dict_df['capacitytoactivity'], outPutFile, region)
    else:
        print('No capacitytoactivity file')
#################################################################################
    if 'demandprofile' in dict_df:
        outPutFile = SpecifiedDemandProfile(outPutFile, dict_df['demand'], dict_df['demandprofile'], startyear, endyear, region)
    else:
        print('No demandprofile file')
###########################################################
###################### Mode of operation parameters######################

    if 'emissions' in dict_df:
        outPutFile = emissionactivity(dict_df['GIS_data'], outPutFile, startyear, endyear, region, dict_df['emissions'])
    else:
        print('No emissions file')
########################################################
    if 'variable_cost' in dict_df:
        outPutFile = variblecost(dict_df['GIS_data'], outPutFile, startyear, endyear, region, dict_df['variable_cost'])
    else:
        print('No variable_cost file')
#############################################################
    if 'inputactivity' in dict_df:
        outPutFile = inputact(outPutFile, dict_df['inputactivity'], startyear, endyear, region)
    else:
        print('No inputactivity file')
################################################################
    if 'outputactivity' in dict_df:
        outPutFile = outputactivity(outPutFile, dict_df['outputactivity'], region)
    else:
        print('No outputactivity file')

    return(outPutFile)

def read_files_old_____():
    cd = os.getcwd()
    df = pd.read_csv(cd + '/data/GIS_data.csv')  # dtype={'user_id': int}
    life = pd.read_csv(cd + '/data/operational_life.csv')  # dtype={'user_id': int}
    totalannuallimit = pd.read_csv(cd + '/data/total_annual_technology_limit.csv')
    trade = pd.read_csv(cd + '/data/capacitytoactivity.csv')  # dtype={'user_id': int}
    inputactivity = pd.read_csv(cd + '/data/inputactivity.csv', index_col=0)  # dtype={'user_id': int}
    demand = pd.read_csv(cd + '/data/demand.csv', index_col=0, header=0)  # dtype={'user_id': int}
    demand_urban = pd.read_csv(cd + '/data/demandprofile.csv', index_col=0, header=0)  # dtype={'user_id': int}
    demand_rural = pd.read_csv(cd + '/data/demandprofile_rural.csv', index_col=0, header=0)  # dtype={'user_id': int}
    capacityfactor_wind = pd.read_csv(cd + '/data/capacityfactor_wind.csv', index_col=None)  # dtype={'user_id': int}
    capacityfactor_wind['date'] = pd.to_datetime(capacityfactor_wind['date'], errors='coerce', format='%Y/%m/%d %H:%M')
    capacityfactor_wind.index = capacityfactor_wind['date']
    capacityfactor_wind = capacityfactor_wind.drop(columns=['date'])
    # capacityfactor_wind.columns = pd.to_numeric(capacityfactor_wind.columns)
    capacityfactor_solar = pd.read_csv(cd + '/data/capacityfactor_solar.csv', index_col=None, header=0)
    capacityfactor_solar['date'] = pd.to_datetime(capacityfactor_solar['date'], errors='coerce',
                                                  format='%Y/%m/%d %H:%M')
    # capacityfactor_solar = capacityfactor_solar.drop(columns=['date'])
    # capacityfactor_solar.columns = pd.to_numeric(capacityfactor_solar.columns)
    # capacityfactor_solar = pd.read_csv(cd +'/data/capacityfactor_solar.csv', header=0)
    capitalcost_RET = pd.read_csv(cd + '/data/capitalcost_RET.csv', header=0)
    trade_cost = pd.read_csv(cd + '/data/capitalcost.csv')
    emissions = pd.read_csv(cd + '/data/emissions.csv')
    variable_cost = pd.read_csv(cd + '/data/variable_cost.csv', header=0)
    fixed_cost = pd.read_csv(cd + '/data/fixed_cost.csv', header=0)

def operational_life(outPutFile, GIS_data, input_data, operational_life):
###############################################################
### OperationalLife (Region, Technology,operationallife)
#############################################################

    dataToInsert = ""
    print("Operational life", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param OperationalLife default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for i, row in GIS_data.iterrows():
        location = row['Location']
        for m, line in operational_life.iterrows():
            t = line['Technology']
            l = line['Life']
            dataToInsert += "%s\t%s_%i\t%i\n" % (input_data['region'][0],t, location, l)
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]

    return(outPutFile)

def fixedcost(df, outPutFile, input_data, fixed_cost):
###############################################################
#Variable cost (Region,Technology,ModeofOperation,Year,Variablecost)
################################################################
    print("Fixed cost", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    dataToInsert = ""
    param = "param FixedCost default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for i, row in df.iterrows():
       location = row['Location']

       for m, line in fixed_cost.iterrows():
           t = line['Technology']
           fc = line['Fixed Cost']
           year = int(input_data['startyear'][0])
           while year <= int(input_data['endyear'][0]):
               dataToInsert += "%s\t%s_%i\t%i\t%f\n" % (input_data['region'][0], t, location, year, fc)
               year += 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def emissionactivity(df, outPutFile, input_data, emissions):
###################################################################################
#Emission activity (Region,Technology,Emissiontype,Modeofoperation, Year,Emission)
###################################################################################
    print("Emission activity", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    dataToInsert = ""
    param = "param EmissionActivityRatio default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    for i, row in df.iterrows():
       location = row[0]
       for m, line in emissions.iterrows():
           year = int(input_data['startyear'][0])
           t = line['Technology']
           k = line['Modeofoperation']
           CO2 = line['CO2']
           NOx = line['NOx']
           while year <=  int(input_data['endyear'][0]):
               dataToInsert += "%s\t%s_%i\tCO2\t%i\t%i\t%f\n" % (input_data['region'][0], t, location, k, year, CO2)
               dataToInsert += "%s\t%s_%i\tNOX\t%i\t%i\t%f\n" % (input_data['region'][0], t, location, k, year, NOx)
               year += 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)

def variblecost(df, outPutFile, input_data, variable_cost):
###############################################################
#Variable cost (Region,Technology,ModeofOperation,Year,Variablecost)
################################################################
    print("Variable cost", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    dataToInsert = ""
    param = "param VariableCost default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for i, row in df.iterrows():
       location = str(row['Location'])
       year = int(input_data['startyear'][0])
       for m, line in variable_cost.iterrows():
           while year <= int(input_data['endyear'][0]):
               t = line['Technology']
               vc = line['Variable Cost']
               modeofop = line['ModeofOperation']
               dataToInsert += "%s\t%s_%s\t%i\t%i\t%f\n" % (input_data['region'][0], t, location, modeofop, year, vc)
               year += 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def totaltechnologyannualactivityupperlimit(df,outPutFile, input_data,totalannuallimit):
#################################################################################
#TotalTechnologyAnnualActivityUpperLimit (Region,technology,year,totaltechnologyupperlimit)
################################################################################
    print("TotalTechnologyAnnualActivityUpperLimit", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param TotalTechnologyAnnualActivityUpperLimit default 99999999999 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    dataToInsert = ""
    for index, row in df.iterrows():
       location = row['Location']
       year = int(input_data['startyear'][0])
       while year <= int(input_data['endyear'][0]):
           for m, line in totalannuallimit.iterrows():
               tech = line['Technology']
               cf = line[location]
               dataToInsert += "%s\t%s_%i\t%i\t%f\n" % (input_data['region'][0], tech, location, year, cf)
           year = year + 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def inputact(outPutFile, inputactivity, input_data):
    dataToInsert = ""
    ###########################################################################
    #Inputactivity ratio (Region, technology, fuel, modeofoperation, year)
    ###########################################################################
    print("Input activity", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param InputActivityRatio default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for j, row in inputactivity.iterrows():
       technology = row['Technology']
       fuel = row['Fuel']
       inputactivityratio = row['Inputactivity']
       modeofoperation = row['ModeofOperation']
       year = int(input_data['startyear'][0])
       while year<=int(input_data['endyear'][0]):
           dataToInsert += "%s\t%s\t%s\t%i\t%i\t%f\n" % (input_data['region'][0], technology, fuel, modeofoperation, year, inputactivityratio)
           year = year + 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)

def SpecifiedDemandProfile(outPutFile, demand, demandprofile,input_data):
    dataToInsert = ""
    #########################################################################
    #SpecifiedDemandProfile (region,fuel,timeslice,year,profile)
    ########################################################################
    print("SpecifiedDemandProfile", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    param = "param SpecifiedDemandProfile default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    fuels = input_data['Demand fuel']
    demand_fuels = [x for x in fuels if str(x) != 'nan']
    for i in demand_fuels:
        for k, line in demandprofile.iterrows():
            timeslice = line['Timeslice']
            year = int(input_data['startyear'][0])
            while year<=int(input_data['endyear'][0]):
                demandprofile.index = demandprofile['Timeslice']
                demand_profile = demandprofile.loc[timeslice][year]
                dataToInsert += "%s\t%s\t%s\t%i\t%f\n" % (input_data['region'][0], i, timeslice, year, demand_profile)
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capacityfactor_wi(outPutFile, df, capacityfactor_wind, input_data, startyear, endyear, months):
    dataToInsert = ""
    ###########################################################################
     #Capacityfactor (region,technolgy,timeslice,year,CF)
     ###########################################################################
    print("Capacity factor wind", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityFactor default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    ######### WIND ###########

    for k, row in df.iterrows():
       location = row['Location']

       year = startyear
       while year <= endyear:
          m= 0
          while m < 11:
             currentMonth = months[m]
             startDate = "2016-%s-01" % (currentMonth)
             endDate = "2016-%s-01" % (months[m+1])
             thisMonthOnly = capacityfactor_wind.query('date > @startDate and date < @endDate')
             #print(thisMonthOnly)
             sliceStart = timesliceDN
             sliceEnd = timesliceDE
             #print(sliceStart)
             #print(sliceEnd)
             ts = "%iD" % (m+1)
             slice = sum(thisMonthOnly[location].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m+1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m+1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd)) # CHANGE 71 to actual location!!!
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             m = m + 1

          while m ==11:
             currentMonth = months[m]
             # for j, row in timeslice.iterrows():
             startDate = "2016-%s-01" % (currentMonth)
             endDate = "2016-%s-31" % (months[m])
             thisMonthOnly = capacityfactor_wind.query('date > @startDate and date < @endDate')

             sliceStart = timesliceDN
             sliceEnd = timesliceDE
             ts = "%iD" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)   #divided by capacity 600 kW
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)   #divided by capacity 600 kW
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)   #divided by capacity 600 kW
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             m = m + 1

          year = year + 1

       cnt = 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capacityfactor_PV(elec, outPutFile, df, capacityfactor_solar, input_data, startyear, endyear,months,region):
    dataToInsert = ""

    ######### Solar PV and MG ###############
    print("Capacity factor solar", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityFactor default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    capacityfactor_solar_pv = capacityfactor_solar.copy()
    capacityfactor_solar_pv.index = capacityfactor_solar_pv[0]
    #capacityfactor_solar = capacityfactor_solar.drop(columns=['0'])
    #capacityfactor_solar.columns = pd.to_numeric(capacityfactor_solar.columns)
    for k, row in df.iterrows():
       location = row['Location']
       year = startyear
       while year <= endyear:
          m = 0
          while m < 11:
             currentMonth = months[m]
             startDate = "2016-%s-01" % (currentMonth)
             endDate = "2016-%s-01" % (months[m + 1])
             thisMonthOnly = capacityfactor_solar_pv.loc[startDate:endDate]
             #thisMonthOnly = capacityfactor_solar.query('date > @startDate and date < @endDate')
             sliceStart = timesliceDN
             sliceEnd = timesliceDE
             ts = "%iD" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             try:
                 average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) /solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if location in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) /solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if location in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) /solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if location in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             m = m + 1

          while m == 11:
             currentMonth = months[m]
             startDate = "2016-%s-01" % (currentMonth)
             endDate = "2016-%s-31" % (months[m])
             thisMonthOnly = capacityfactor_solar_pv.loc[startDate:endDate]
             #thisMonthOnly = capacityfactor_solar.query('date > @startDate and date < @endDate')
             sliceStart = timesliceDN
             sliceEnd = timesliceDE
             ts = "%iD" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) /solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if location in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if location in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if location in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             m = m + 1

          year = year + 1

       cnt = 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capacityfactor_solar_battery13h(elec, outPutFile, df, capacityfactor_solar, input_data, batteryCF, startyear, endyear, months,region):
    dataToInsert = ""
    ######### Solar 13h battery ###############
    print("Capacity factor solar PV & MG 13h", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityFactor default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    batteryCapacityFactor = batteryCF
    batteryTime = battery13h
    lastRowWasZero = False
    batteryConsumed = False
    index = 0
    for k, row in df.iterrows():
       location = row['Location']
       lastRowWasZero = False
       batteryConsumed = False
       index = 0
       for solarCapacity in capacityfactor_solar[location].values:
          currentRowIsZero = solarCapacity == 0
          if not currentRowIsZero:
             # This will happen when the current row is not zero. We should "reset" everything.
             batteryTime = battery13h
             batteryCapacityFactor = batteryCF
             batteryConsumed = False
             lastRowWasZero = False
          elif batteryTime == int(0):
             # This will happen when the current value is 0, the last value was zero and there is no batterytime left.
             batteryConsumed = True
             batteryTime = battery13h
             batteryCapacityFactor = batteryCF
          elif solarCapacity == 0 and lastRowWasZero and not batteryConsumed:
             # This will happen when the last row was zero and the current row is 0.
             capacityfactor_solar.at[index, location] = batteryCapacityFactor
             lastRowWasZero = True
             batteryTime -= 1
          elif not batteryConsumed:
             # This will happen when the last row was not zero and the current row is 0.
             capacityfactor_solar.at[index, location] = batteryCapacityFactor
             lastRowWasZero = True
             batteryTime -= 1
          index += 1
    capacityfactor_solar_batt = capacityfactor_solar.copy()
    capacityfactor_solar_batt.index = capacityfactor_solar_batt[0]
    #capacityfactor_solar = capacityfactor_solar.drop(columns=['0'])
    #capacityfactor_solar.columns = pd.to_numeric(capacityfactor_solar.columns)
    for k, row in df.iterrows():
       location = row['Location']
       # print(location)
       year = startyear
       while year <= endyear:
          m = 0
          while m < 11:
             currentMonth = months[m]
             startDate = "2016-%s-01" % (currentMonth)
             endDate = "2016-%s-01" % (months[m + 1])
             thisMonthOnly = capacityfactor_solar_batt.loc[startDate:endDate]
             #thisMonthOnly = capacityfactor_solar.query('date > @startDate and date < @endDate')
             #print(thisMonthOnly)

             sliceStart = timesliceDN
             sliceEnd = timesliceDE
             ts = "%iD" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             m = m + 1

          while m == 11:
             currentMonth = months[m]
             # for j, row in timeslice.iterrows():
             startDate = "2016-%s-01" % (currentMonth)
             endDate = "2016-%s-31" % (months[m])
             thisMonthOnly = capacityfactor_solar_batt.loc[startDate:endDate]
             #thisMonthOnly = capacityfactor_solar.query('date > @startDate and date < @endDate')

             sliceStart = timesliceDN
             sliceEnd = timesliceDE
             ts = "%iD" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(
                thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(
                thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             m = m + 1

          year = year + 1

       cnt = 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)

def capacityfactor_solar_battery(elec, outPutFile, df, capacityfactor_solar, input_data, capitalcost_RET, startyear, endyear, months, region):

    print("Capacity factor solar with battery", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityFactor default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    dataToInsert = ""

    cf_tech = capitalcost_RET.groupby('Technology')
    battery_tech = cf_tech.get_group('Battery')
    battery_CF = battery_tech['CF']
    battery_tech.index = battery_tech['CF']

    for k, row in df.iterrows():
       location = str(row['Location'])

       batteryCapacityFactor = batteryCF
       batteryTime = battery8h
       lastRowWasZero = False
       batteryConsumed = False
       index = 0
       for solarCapacity in capacityfactor_solar[location].values:

          currentRowIsZero = solarCapacity == 0

          if not currentRowIsZero:
             # This will happen when the current row is not zero. We should "reset" everything.
             batteryTime = battery8h
             batteryCapacityFactor = batteryCF
             batteryConsumed = False
             lastRowWasZero = False
          elif batteryTime == int(0):
             # This will happen when the current value is 0, the last value was zero and there is no batterytime left.
             batteryConsumed = True
             batteryTime = 8
             batteryCapacityFactor = batteryCF
          elif solarCapacity == 0 and lastRowWasZero and not batteryConsumed:
             # This will happen when the last row was zero and the current row is 0.
             capacityfactor_solar.at[index, location] = batteryCapacityFactor
             lastRowWasZero = True
             batteryTime -= 1
          elif not batteryConsumed:
             # This will happen when the last row was not zero and the current row is 0. Same as above???
             capacityfactor_solar.at[index, location] = batteryCapacityFactor
             lastRowWasZero = True
             batteryTime -= 1
          index += 1
    capacityfactor_solar_batt_8 = capacityfactor_solar.copy()
    capacityfactor_solar_batt_8.index = capacityfactor_solar_batt_8[0]
    capacityfactor_solar_batt_8 = capacityfactor_solar_batt_8.drop(columns=[0])
    #capacityfactor_solar.columns = pd.to_numeric(capacityfactor_solar.columns)
    for k, row in df.iterrows():
       location = row['Location']
       # print(location)
       year = startyear
       while year <= endyear:
          m = 0
          while m < 11:
             currentMonth = months[m]
             startDate = "2016-%s-01" % (currentMonth)
             endDate = "2016-%s-01" % (months[m + 1])
             thisMonthOnly = capacityfactor_solar_batt_8.loc[startDate:endDate]

             sliceStart = timesliceDN
             sliceEnd = timesliceDE
             ts = "%iD" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             m = m + 1

          while m == 11:
             currentMonth = months[m]
             # for j, row in timeslice.iterrows():
             startDate = "2016-%s-01" % (currentMonth)
             endDate = "2016-%s-31" % (months[m])
             thisMonthOnly = capacityfactor_solar_batt_8.loc[startDate:endDate]
             #thisMonthOnly = capacityfactor_solar.query('date > @startDate and date < @endDate')

             sliceStart = timesliceDN
             sliceEnd = timesliceDE
             ts = "%iD" % (m + 1)
             slice = sum(
                thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(
                thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(
                thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if location in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
             m = m + 1

          year = year + 1

       cnt = 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)

def outputactivity(outPutFile, outputactivity, input_data):
    dataToInsert = ""
    ###########################################################################
    #Outputactivity ratio
    ###########################################################################
    print("Outputactivity", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param OutputActivityRatio default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for j, row in outputactivity.iterrows():
       technology = row['Technology']
       fuel = row['Fuel']
       outputactivityratio = row['Outputactivity']
       modeofoperation = row['ModeofOperation']
       year = int(input_data['startyear'][0])
       while year<=int(input_data['endyear'][0]):
          dataToInsert += "%s\t%s\t%s\t%s\t%i\t%f\n" % (input_data['region'][0], technology, fuel, modeofoperation, year, outputactivityratio)
          year = year + 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def specifiedannualdemand(outPutFile, demand, input_data):
    #########################################################################
    #SpecifiedAnnualDemand (region,fuel,year,demand)
    ########################################################################
    print("SpecifiedAnnualDemand", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param SpecifiedAnnualDemand default 0 :=\n"
    dataToInsert = ""
    startIndex = outPutFile.index(param) + len(param)
    demand.index = demand['Fuel']
    demand = demand.drop(columns=['Fuel'])
    for j, row in demand.iterrows():
        year = demand.columns
        for k in year: #year is an object so I cannot match it with a number (e.g. startyear)
            demandForThisYearAndlocation = demand.loc[j][k]
            dataToInsert += "%s\t%s\t%s\t%f\n" % (input_data['region'][0], j, k, demandForThisYearAndlocation)
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capitalcost_dynamic(df, outPutFile, capitalcost_RET, capacityfactor_wind, capacityfactor_solar, input_data):
    dataToInsert = ""
    ##################################################################
    #Capital cost (region,technology,year,capitalcost)
    ##################################################################
    print("Capital cost dynamic cost", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapitalCost default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    #Section the different technology types per CF and OSeMOSYS name
    cf_tech = capitalcost_RET.groupby('Technology')
    wind_tech = cf_tech.get_group('Wind')
    wind_CF = wind_tech['CF']
    wind_tech_name = wind_tech.loc[1]['Technology_name_OSeMOSYS']
    comm_PV_tech =  cf_tech.get_group('Comm PV')
    comm_PV_CF = comm_PV_tech['CF']
    comm_PV_tech_name = comm_PV_tech.loc[10]['Technology_name_OSeMOSYS']
    pv_tech = cf_tech.get_group('PV')
    pv_CF = pv_tech['CF']
    pv_tech_name = pv_tech.loc[17]['Technology_name_OSeMOSYS']
    battery_tech = cf_tech.get_group('Battery')
    battery_CF = battery_tech['CF']
    battery_tech.index = battery_tech['CF']

    #Caluculate the CF for the location over the year
    for m, row in df.iterrows():
       location = str(row['Location']) # This is needed because the columns in capacityfactor_wind isn't int64. They are strings.
       slice_wind = sum(capacityfactor_wind[location])
       average_wind = (slice_wind / len(capacityfactor_wind._values))

       slice_solar = sum(capacityfactor_solar[location])
       average_solar = (slice_solar / len(capacityfactor_solar._values))

       # Wind
       for k in wind_tech.columns[3:]:  # year is an object so I cannot match it with a number (e.g. startyear)
          def find_nearest(wind_CF, average_wind):
              arraywind = np.asarray(wind_CF)
              idx = (np.abs(arraywind - average_wind)).argmin()
              return arraywind[idx]
          cf=find_nearest(wind_CF, average_wind)
          wind_tech.index = wind_tech['CF']
          windcapitalcost = wind_tech.loc[cf][k]
          dataToInsert += "%s\t%s_%s\t%s\t%f\n" % (input_data['region'][0], wind_tech_name, location, k, windcapitalcost)

       #Solar PV
       for k in pv_tech.columns[3:]:
          def find_nearest(pv_CF, average_solar):
             arraysun = np.asarray(pv_CF)
             idx = (np.abs(arraysun - average_solar)).argmin()
             return arraysun[idx]
          cf=find_nearest(pv_CF, average_solar)
          pv_tech.index = pv_tech['CF']
          pvcapitalcost = pv_tech.loc[cf][k]
          dataToInsert += ("%s\t%s_%s\t%s\t%f\n" % (input_data['region'][0], pv_tech_name, location, k, pvcapitalcost))
          # Battery
          if battery_tech is None:
              pass
          else:
              for battcf in battery_CF:
                  battery_tech_name = battery_tech.loc[battcf]['Technology_name_OSeMOSYS']
                  sopvcapitalcostbatt = pv_tech.loc[cf][k] + battery_tech.loc[battcf][k]
                  techname = pv_tech_name+"_"+battery_tech_name
                  dataToInsert += ("%s\t%s_%s\t%s\t%f\n" % (input_data['region'][0], techname, location, k, sopvcapitalcostbatt))

       #Solar MG
       for k in comm_PV_tech.columns[3:]:
          def find_nearest(comm_PV_CF, average_solar):
             arraysun = np.asarray(comm_PV_CF)
             idx = (np.abs(arraysun - average_solar)).argmin()
             return arraysun[idx]
          cf = find_nearest(comm_PV_CF, average_solar)
          comm_PV_tech.index = comm_PV_tech['CF']
          somgcapitalcost = comm_PV_tech.loc[cf][k]
          dataToInsert += ("%s\t%s_%s\t%s\t%f\n" % (input_data['region'][0], comm_PV_tech_name, location, k, somgcapitalcost))

       # Battery
       if battery_tech is None:
           pass
       else:
           for battcf in battery_CF:
               battery_tech_name = battery_tech.loc[battcf]['Technology_name_OSeMOSYS']
               somgcapitalcostbatt = comm_PV_tech.loc[cf][k] + battery_tech.loc[battcf][k]
               techname = comm_PV_tech_name + "_" + battery_tech_name
               dataToInsert += ("%s\t%s_%s\t%s\t%f\n" % (input_data['region'][0], techname, location, k, somgcapitalcostbatt))

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capitalcost(df, outPutFile, trade_cost, input_data):
    dataToInsert = ""

     #################################################################
    #Capital cost (region,technology,year,capitalcost)
    ################################################################
    print("Capital cost", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapitalCost default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for m, row in trade_cost.iterrows():
      cost = row['Capitalcost']
      tech = row['Technology']

      year = int(input_data['startyear'][0])
      while year <= int(input_data['endyear'][0]):
         dataToInsert += "%s\t%s\t%i\t%f\n" % (input_data['region'][0], tech, year, cost)
         year += 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capacitytoactivity(trade, outPutFile, input_data):
    #################################################
    # CapacityToActivityUnit (region,technology,capacitytoactivityunit)
    #################################################
    dataToInsert = ""
    print("Capacity to activity", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityToActivityUnit default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for m, row in trade.iterrows():
       capact = row['CapacitytoActivity']
       t = row['Tech']
       dataToInsert += "%s\t%s\t%f\n" % (input_data['region'][0],t ,capact)

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def write_to_file(file_object, outPutFile):
###############################################################
# write all to file
#########################################################
    print("write to file", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    with open(file_object, "w") as actualOutputFile:
       actualOutputFile.truncate(0) #empty the file
       actualOutputFile.write(outPutFile)
