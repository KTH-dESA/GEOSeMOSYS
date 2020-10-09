import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

def load_csvs(paths):
    """Creates a dataframe dictionary from the csv files in /data : dict_df

    Arguments
    ---------
    param_file : paths
        Path to the data files (/data)
    """
    filepaths = [f for f in listdir(paths) if isfile(join(paths, f))]
    onlyfiles = [os.path.join(paths, f) for f in filepaths]
    dict_df = {}
    for files in onlyfiles:
    #validate that the files are csv. Else the read function will not work
        _, filename = os.path.split(files)
        name, ending = os.path.splitext(filename)
        if ending == '.csv':
            dict_df[name] = pd.read_csv(files, header=0)
        else:
            print('You have mixed file types in you directory, please make sure all are .csv type! {}'.format(files))

    return dict_df

def make_outputfile(param_file):
    """Creates a string from the template OSeMOSYS file

    Arguments
    ---------
    param_file : str
        Path to the parameter file
    """
    allLinesFromXy = ""
    with open(param_file, "r") as inputFile:
        allLinesFromXy = inputFile.read()
    outPutFile = allLinesFromXy
    return outPutFile

def functions_to_run(dict_df, outPutFile):
    """Runs all the functions for the different parameters

    Arguments
    ---------
    dict_df, outPutFile
        dict_df: is a dictionary which contains all the csv files as dataframes from load_csv. Key is the name of the csv file
        outPutFile: is a string with the empty OSeMOSYS parameters file from make_outputfile
    """
    if 'operational_life' in dict_df:
        outPutFile = operational_life(outPutFile, dict_df['GIS_data'],  dict_df['input_data'], dict_df['operational_life'])
    else:
        print('No operational_life file')
#################################################################################
    if 'fixed_cost' in dict_df:
        outPutFile = fixedcost(dict_df['GIS_data'], outPutFile, dict_df['input_data'], dict_df['fixed_cost'])
    else:
        print('No fixed_cost file')
#####################################################################################
    if 'total_annual_technology_limit' in dict_df:
        outPutFile = totaltechnologyannualactivityupperlimit(dict_df['GIS_data'], outPutFile, dict_df['input_data'], dict_df['total_annual_technology_limit'])
    else:
        print('No total_annual_technology_limit file')

    if 'demand' in dict_df:
        outPutFile = specifiedannualdemand(outPutFile, dict_df['demand'], dict_df['input_data'])
    else:
        print('No demand file')
####################################################################################
    if 'capitalcost_RET' in dict_df:
        outPutFile = capitalcost_dynamic(dict_df['GIS_data'], outPutFile, dict_df['capitalcost_RET'],
                                         dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'],
                                         dict_df['input_data'])
    else:
        print('No capitalcost_RET file')
###########################################################################
    if 'capitalcost' in dict_df:
        outPutFile = capitalcost(outPutFile, dict_df['capitalcost'], dict_df['input_data'])
    else:
        print('No capitalcost file')

##########################################################
###########TIMESLICE parameters###############
#     if 'battery' in dict_df:
#         outPutFile = capacityfactor_solar_battery(elec, outPutFile, dict_df['GIS_data'], dict_df['capacityfactor_solar'], dict_df['input_data'], dict_df['battery'], dict_df['input_data'])
#     else:
#         print('No battery file')
# ################################################################################
#     if 'capacityfactor_solar' in dict_df:
#         outPutFile = capacityfactor_PV(elec, outPutFile, dict_df['GIS_data'], dict_df['capacityfactor_solar'], dict_df['input_data'], dict_df['input_data'])
#     else:
#         print('No capacityfactor_solar file')
# ###############################################################################
#     if 'capacityfactor_wind' in dict_df:
#         outPutFile = capacityfactor_wi(outPutFile, dict_df['GIS_data'],  dict_df['capacityfactor_wind'], dict_df['input_data'], dict_df['input_data'])
#     else:
#         print('No capacityfactor_wind file')
##############################################################################
    if 'capacitytoactivity' in dict_df:
        outPutFile = capacitytoactivity(dict_df['capacitytoactivity'], outPutFile, dict_df['input_data'])
    else:
        print('No capacitytoactivity file')
#################################################################################
    # if 'demandprofile' in dict_df:
    #     outPutFile = SpecifiedDemandProfile(outPutFile, dict_df['demandprofile'],
    #                                         dict_df['input_data'])
    # else:
    #     print('No demandprofile file')
###########################################################
###################### Mode of operation parameters######################

    if 'emissions' in dict_df:
        outPutFile = emissionactivity(dict_df['GIS_data'], outPutFile, dict_df['input_data'], dict_df['emissions'])
    else:
        print('No emissions file')
########################################################
    if 'variable_cost' in dict_df:
        outPutFile = variblecost(dict_df['GIS_data'], outPutFile, dict_df['input_data'], dict_df['variable_cost'])
    else:
        print('No variable_cost file')
#############################################################
    if 'inputactivity' in dict_df:
        outPutFile = inputact(outPutFile, dict_df['inputactivity'], dict_df['input_data'])
    else:
        print('No inputactivity file')
################################################################
    if 'outputactivity' in dict_df:
        outPutFile = outputactivity(outPutFile, dict_df['outputactivity'], dict_df['input_data'])
    else:
        print('No outputactivity file')

    return(outPutFile)

def operational_life(outPutFile, GIS_data, input_data, operational_life):
    """
    builds the OperationalLife (Region, Technology, OperationalLife)
    -------------
    Arguments
    outPutFile, GIS_data, input_data, operational_life
        outPutFile: is a string containing the OSeMOSYS parameters file
        GIS_data: is the location specific data which is used to iterate the data
        input_data: contains meta data such as region, start year, end year, months, timeslices
        OperationalLife: is the operational life per technology
    """
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
    """
    Builds the Fixed cost (Region, Technology, Year, Fixed cost)
    -------------
    Arguments
    df, outPutFile, input_data, fixed_cost
        outPutFile: is a string containing the OSeMOSYS parameters file
        df: is the location specific data which is used to iterate the data
        input_data: contains meta data such as region, start year, end year, months, timeslices
        fixed_cost: is the fixed cost per technology
    """
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
    """
    Builds the Emission activity (Region, Technology, Emissiontype, Technology, ModeofOperation, Year, emissionactivity)
    -------------
    Arguments
    df, outPutFile, input_data, emissions
        outPutFile: is a string containing the OSeMOSYS parameters file
        df: is the location specific data which is used to iterate the data
        input_data: contains meta data such as region, start year, end year, months, timeslices
        emissions: is the emissionactivity per technology and mode of operation
    """
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
    """
    Builds the Variable cost (Region, Technology, ModeofOperation, Year, Variablecost)
    -------------
    Arguments
    df, outPutFile, input_data, variable_cost
        outPutFile: is a string containing the OSeMOSYS parameters file
        df: is the location specific data which is used to iterate the data
        input_data: contains meta data such as region, start year, end year, months, timeslices
        variable_cost: is the variable cost per technology and mode of operation
    """

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

def totaltechnologyannualactivityupperlimit(df,outPutFile, input_data, totalannuallimit):
    """
    Builds the TotalTechnologyAnnualActivityUpperLimit (Region, Technology, Year, TotalTechnologyUpperLimit)
    -------------
    Arguments
    df,outPutFile, input_data, totalannuallimit
        outPutFile: is a string containing the OSeMOSYS parameters file
        df: is the location specific data which is used to iterate for the location specific the data
        input_data: contains meta data such as region, start year, end year, months, timeslices
        totalannuallimit: is the total annual limit per technology
    """

    print("TotalTechnologyAnnualActivityUpperLimit", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    dataToInsert = ""
    param = "param TotalTechnologyAnnualActivityUpperLimit default 99999999999 :=\n"
    startIndex = outPutFile.index(param) + len(param)

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
    """
    Builds the InputactivityRatio (Region, Technology, Fuel, Modeofoperation, Year, InputactivityRatio)
    -------------
    Arguments
    outPutFile, inputactivity, input_data
        outPutFile: is a string containing the OSeMOSYS parameters file
        input_data: contains meta data such as region, start year, end year, months, timeslices
        inputactivity: is the inputactivity per fuel and technology
    """
    dataToInsert = ""
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

def SpecifiedDemandProfile(outPutFile, demandprofile, input_data):
    """
    Builds the SpecifiedDemandProfile (Region, Fuel, Timeslice, Year, SpecifiedDemandProfile)
    -------------
    Arguments
    outPutFile, demandprofile,input_data
        outPutFile: is a string containing the OSeMOSYS parameters file
        input_data: contains meta data such as region, start year, end year, months, timeslices
        demandprofile: is the demandprofile per fuel and technology
    """
    dataToInsert = ""
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

def capacityfactor_wi(outPutFile, df, capacityfactor_wind, input_data):
    """
    builds the Capacityfactor (Region, Technolgy, Timeslice, Year, CapacityFactor)
    -------------
    Arguments
    outPutFile, df, capacityfactor_wind, input_data
        outPutFile: is a string containing the OSeMOSYS parameters file
        df: is the location specific data which is used to iterate the data
        capacityfactor_wind: Hourly 8760 wind CF file for each location
        input_data: contains meta data such as region, start year, end year, months, timeslices
    """
    dataToInsert = ""
    print("Capacity factor wind", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityFactor default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)

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

def capacityfactor_PV(outPutFile, df, capacityfactor_solar, input_data):
    """
    builds the Capacityfactor (Region, Technolgy, Timeslice, Year, CapacityFactor)
    -------------
    Arguments
    outPutFile, df, capacityfactor_solar, input_data
        outPutFile: is a string containing the OSeMOSYS parameters file
        df: is the location specific data which is used to iterate the data
        capacityfactor_solar: Hourly 8760 solar CF file for each location
        input_data: contains meta data such as region, start year, end year, months, timeslices
    """
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

# def capacityfactor_solar_battery13h(elec, outPutFile, df, capacityfactor_solar, input_data, batteryCF, startyear, endyear, months,region):
#
#     dataToInsert = ""
#     ######### Solar 13h battery ###############
#     print("Capacity factor solar PV & MG 13h", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#     param = "param CapacityFactor default 1 :=\n"
#     startIndex = outPutFile.index(param) + len(param)
#
#     batteryCapacityFactor = batteryCF
#     batteryTime = battery13h
#     lastRowWasZero = False
#     batteryConsumed = False
#     index = 0
#     for k, row in df.iterrows():
#        location = row['Location']
#        lastRowWasZero = False
#        batteryConsumed = False
#        index = 0
#        for solarCapacity in capacityfactor_solar[location].values:
#           currentRowIsZero = solarCapacity == 0
#           if not currentRowIsZero:
#              # This will happen when the current row is not zero. We should "reset" everything.
#              batteryTime = battery13h
#              batteryCapacityFactor = batteryCF
#              batteryConsumed = False
#              lastRowWasZero = False
#           elif batteryTime == int(0):
#              # This will happen when the current value is 0, the last value was zero and there is no batterytime left.
#              batteryConsumed = True
#              batteryTime = battery13h
#              batteryCapacityFactor = batteryCF
#           elif solarCapacity == 0 and lastRowWasZero and not batteryConsumed:
#              # This will happen when the last row was zero and the current row is 0.
#              capacityfactor_solar.at[index, location] = batteryCapacityFactor
#              lastRowWasZero = True
#              batteryTime -= 1
#           elif not batteryConsumed:
#              # This will happen when the last row was not zero and the current row is 0.
#              capacityfactor_solar.at[index, location] = batteryCapacityFactor
#              lastRowWasZero = True
#              batteryTime -= 1
#           index += 1
#     capacityfactor_solar_batt = capacityfactor_solar.copy()
#     capacityfactor_solar_batt.index = capacityfactor_solar_batt[0]
#     #capacityfactor_solar = capacityfactor_solar.drop(columns=['0'])
#     #capacityfactor_solar.columns = pd.to_numeric(capacityfactor_solar.columns)
#     for k, row in df.iterrows():
#        location = row['Location']
#        # print(location)
#        year = startyear
#        while year <= endyear:
#           m = 0
#           while m < 11:
#              currentMonth = months[m]
#              startDate = "2016-%s-01" % (currentMonth)
#              endDate = "2016-%s-01" % (months[m + 1])
#              thisMonthOnly = capacityfactor_solar_batt.loc[startDate:endDate]
#              #thisMonthOnly = capacityfactor_solar.query('date > @startDate and date < @endDate')
#              #print(thisMonthOnly)
#
#              sliceStart = timesliceDN
#              sliceEnd = timesliceDE
#              ts = "%iD" % (m + 1)
#              slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
#              average_wind = (
#              (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
#              if location in elec.values:
#                 dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#
#              sliceStart = timesliceED
#              sliceEnd = timesliceEN
#              ts = "%iE" % (m + 1)
#              slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
#              average_wind = (
#              (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
#              if location in elec.values:
#                 dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#
#              sliceStart = timesliceNE
#              sliceEnd = timesliceND
#              ts = "%iN" % (m + 1)
#              slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
#              average_wind = (
#              (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
#              if location in elec.values:
#                 dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              m = m + 1
#
#           while m == 11:
#              currentMonth = months[m]
#              # for j, row in timeslice.iterrows():
#              startDate = "2016-%s-01" % (currentMonth)
#              endDate = "2016-%s-31" % (months[m])
#              thisMonthOnly = capacityfactor_solar_batt.loc[startDate:endDate]
#              #thisMonthOnly = capacityfactor_solar.query('date > @startDate and date < @endDate')
#
#              sliceStart = timesliceDN
#              sliceEnd = timesliceDE
#              ts = "%iD" % (m + 1)
#              slice = sum(thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
#              average_wind = (
#              (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
#              if location in elec.values:
#                 dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#
#              sliceStart = timesliceED
#              sliceEnd = timesliceEN
#              ts = "%iE" % (m + 1)
#              slice = sum(
#                 thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
#              average_wind = (
#              (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
#              if location in elec.values:
#                 dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#
#              sliceStart = timesliceNE
#              sliceEnd = timesliceND
#              ts = "%iN" % (m + 1)
#              slice = sum(
#                 thisMonthOnly[(location)].between_time(sliceStart, sliceEnd))
#              average_wind = (
#              (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
#              if location in elec.values:
#                 dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (location, ts, year, average_wind)
#              m = m + 1
#
#           year = year + 1
#
#        cnt = 1
#     outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
#     return (outPutFile)

def capacityfactor_solar_battery(outPutFile, df, capacityfactor_solar, input_data, capitalcost_RET):
    """
    builds the Capacityfactor(Region, Technolgy, Timeslice, Year, CapacityFactor)
    This method is for capacityfactor which does not use storage equations
    -------------
    Arguments
    outPutFile, df, capacityfactor_solar, input_data, capitalcost_RET
        outPutFile: is a string containing the OSeMOSYS parameters file
        df: is the location specific data which is used to iterate the data
        capacityfactor_solar: Hourly 8760 solar CF file for each location
        input_data: contains meta data such as region, start year, end year, months, timeslices
        capitalcost_RET: --
    """
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
    """
    builds the Outputactivity(Region, Technology, Fuel, ModeofOperation, Year, outputactivity)
    -------------
    Arguments
    outPutFile, outputactivity, input_data
        outPutFile: is a string containing the OSeMOSYS parameters file
        outputactivity: The outputactivity between the Technology and Fuel
        input_data: contains meta data such as region, start year, end year, months, timeslices
    """
    dataToInsert = ""
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
    """
    builds the SpecifiedAnnualDemand (Region, Fuel, Year, Demand)
    -------------
    Arguments
    outPutFile, demand, input_data
        outPutFile: is a string containing the OSeMOSYS parameters file
        demand: The demand per Fuel
        input_data: contains meta data such as region, start year, end year, months, timeslices
    """
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
    """
    builds the Capitalcost (Region, Technology, Year, CapitalCost) where the cost is dynamic. Here when the capacity factor vary for Wind
    -------------
    Arguments
    df, outPutFile, capitalcost_RET, capacityfactor_wind, capacityfactor_solar, input_data
        df: is the location specific data which is used to iterate the data
        outPutFile: is a string containing the OSeMOSYS parameters file
        capitalcost_RET: The capital cost per technology and capacity factor
        capacityfactor_wind: Hourly 8760 wind CF file for each location
        capacityfactor_solar: Hourly 8760 solar CF file for each location
        input_data: contains meta data such as region, start year, end year, months, timeslices
    """
    dataToInsert = ""
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

def capitalcost(outPutFile, trade_cost, input_data):
    """
    builds the Capital cost (region,technology,year,capitalcost)
    -------------
    Arguments
    outPutFile, outputactivity, trade_cost
        outPutFile: is a string containing the OSeMOSYS parameters file
        trade_cost: The Capitalcost which is not dynamic
        input_data: contains meta data such as region, start year, end year, months, timeslices
    """
    dataToInsert = ""

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
    """
    builds the CapacityToActivityUnit (Region, Technology, CapacitytoActivityUnit)
    -------------
    Arguments
    trade, outPutFile, input_data
        outPutFile: is a string containing the OSeMOSYS parameters file
        trade: The capacitytoactivity for each technology
        input_data: contains meta data such as region, start year, end year, months, timeslices
    """
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
    """
    write_to_file writes the string outPutFile to file_object
    -------------
    Arguments
    file_object, outPutFile
        file_object: is the path and name of the file where the datafile will be saved
        outPutFile:  is the accumulated final string of all data
    """
###############################################################
# write all to file
#########################################################
    print("write to file", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    with open(file_object, "w") as actualOutputFile:
       actualOutputFile.truncate(0) #empty the file
       actualOutputFile.write(outPutFile)
