import pandas as pd
import numpy as np
from datetime import datetime


def operational_life(df, elec, outPutFile):
    dataToInsert = ""
    print("Operational life", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param OperationalLife default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for m, row in df.iterrows():
        objectId = row['OBJECTID *']
        count = 1

        # if electrified PV
        if objectId in elec.values:
            pvoperationallife = float(row['OperationalLifePV'])
            dataToInsert += "Kenya  SOPV_%i_1\t%i\n" % (objectId, pvoperationallife)

            pv4hoperationallife = float(row['OperationalLifePV4h'])
            dataToInsert += "Kenya  SOPV12h_%i_1\t%i\n" % (objectId, pv4hoperationallife)

            pv8hoperationallife = float(row['OperationalLifePV8h'])
            dataToInsert += "Kenya  SOPV8h_%i_1\t%i\n" % (objectId, pv8hoperationallife)

        somgoperationallife = float(row['OperationalLifeSOMG'])
        dataToInsert += "Kenya  SOMG_%i\t%i\n" % (objectId, somgoperationallife)

        somgoperationallife = float(row['OperationalLifeSOMG'])
        dataToInsert += "Kenya  SOMG12h_%i\t%i\n" % (objectId, somgoperationallife)

        windoperationallife = float(row['OperationalLifeWind'])
        # \t gives tab
        dataToInsert += "Kenya  WI_%i\t%i\n" % (objectId, windoperationallife)

        pvoperationallife = float(row['OperationalLifePV'])
        dataToInsert += "Kenya  SOPV_%i_0\t%i\n" % (objectId, pvoperationallife)

        pv4hoperationallife = float(row['OperationalLifePV4h'])
        dataToInsert += "Kenya  SOPV12h_%i_0\t%i\n" % (objectId, pv4hoperationallife)

        pv8hoperationallife = float(row['OperationalLifePV8h'])
        dataToInsert += "Kenya  SOPV8h_%i_0\t%i\n" % (objectId, pv8hoperationallife)

    life = pd.read_excel('Kenya_data_input_ALL.xlsx', 'operational_life')

    for m, row in life.iterrows():
        t = row['Technology']
        l = row['Life']

        dataToInsert += "Kenya  %s\t%i\n" % (t, l)

        cnt = 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def emissionactivity(df, outPutFile, startyear, endyear):
    ###############################################################
    #Emission activity (Region,Technology,Emissiontype,Year,Emission)
    ################################################################
    print("Emission activity", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    dataToInsert = ""

    param = "param EmissionActivityRatio default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for i, row in df.iterrows():
       objectId = row['OBJECTID *']
       count = 1

       year = startyear
       while year <= endyear:
          CO2 = 0.000069427604
          #\t gives tab
          dataToInsert += "Kenya  KEDSGEN_%i\tCO2\t1\t%i\t%f\n" % (objectId, year, CO2)
          year += 1
       year2 = startyear
       while year2 <= endyear:
          NOX = 5.687e-10
          dataToInsert += ("Kenya  KEDSGEN_%i\tNOX\t1\t%i\t%f\n" % (objectId, year2, NOX))
          year2 = year2 + 1
       year2 = startyear

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)

def variablecost(outPutFile, df, elec, startyear, endyear):
    ###############################################################
    #Variable cost (Region,Technology,ModeofOperation,Year,Variablecost)
    ################################################################
    print("Variable cost", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #reset
    dataToInsert = ""
    param = "param VariableCost default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for i, row in df.iterrows():
       objectId = row['OBJECTID *']
       count = 1
       #if electrified PV
       if objectId in elec.values:
          year2 = startyear
          while year2 <= endyear:
             pvvariablecost = float(row['VariableCostPV'])
             dataToInsert += ("Kenya  SOPV_%i_1\t1\t%i\t%f\n" % (objectId, year2, pvvariablecost))
             year2 = year2 + 1
          year2 = startyear
          while year2 <= endyear:
             pvvariablecost = float(row['VariableCostPV4h'])
             dataToInsert += ("Kenya  SOPV12h_%i_1\t1\t%i\t%f\n" % (objectId, year2, pvvariablecost))
             year2 = year2 + 1
          year2 = startyear
          while year2 <= endyear:
             pvvariablecost = float(row['VariableCostPV8h'])
             dataToInsert += ("Kenya  SOPV8h_%i_1\t1\t%i\t%f\n" % (objectId, year2, pvvariablecost))
             year2 = year2 + 1
       year = startyear
       # add for each year for one technology, total energy avaliable in each cell
       while year <= endyear:
          windvariablecost = float(row['VariableCostWind'])
          #\t gives tab
          dataToInsert += "Kenya  WI_%i\t1\t%i\t%f\n" % (objectId, year, windvariablecost)
          year += 1
       year2 = startyear
       while year2 <= endyear:
          pvvariablecost = float(row['VariableCostPV'])
          dataToInsert += ("Kenya  SOPV_%i_0\t1\t%i\t%f\n" % (objectId, year2, pvvariablecost))
          year2 = year2 + 1
       year2 = startyear
       while year2 <= endyear:
          pvvariablecost = float(row['VariableCostPV4h'])
          dataToInsert += ("Kenya  SOPV12h_%i_0\t1\t%i\t%f\n" % (objectId, year2, pvvariablecost))
          year2 = year2 + 1
       year3 = startyear
       year2 = startyear
       while year2 <= endyear:
          pvvariablecost = float(row['VariableCostPV8h'])
          dataToInsert += ("Kenya  SOPV8h_%i_0\t1\t%i\t%f\n" % (objectId, year2, pvvariablecost))
          year2 = year2 + 1
       year3 = startyear
       while year3 <= endyear:
          soMGvariablecost = float(row['VariableCostSOMG'])
          dataToInsert += ("Kenya  SOMG_%i\t1\t%i\t%f\n" % (objectId, year3, soMGvariablecost))
          year3 = year3 + 1
       while year3 <= endyear:
          soMGvariablecost = float(row['VariableCostSOMG'])
          dataToInsert += ("Kenya  SOMG12h_%i\t1\t%i\t%f\n" % (objectId, year3, soMGvariablecost))
          year3 = year3 + 1
       while year3 <= endyear:
          diesel = float(row['Diesel_transport'])
          dataToInsert += ("Kenya  KEDSGEN_%i\t1\t%i\t%f\n" % (objectId, year3, diesel))
          year3 = year3 + 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def totaltechnologyannualactivityupperlimit(df,outPutFile, startyear, endyear):
    #reset
    dataToInsert = ""
    #################################################################################
    #TotalTechnologyAnnualActivityUpperLimit (Region,technology,year,totaltechnologyupperlimit)
    ################################################################################
    print("TotalTechnologyAnnualActivityUpperLimit", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param TotalTechnologyAnnualActivityUpperLimit default 99999999999 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    for index, row in df.iterrows():
       objectId = row['OBJECTID *']
       cnt = 1
       year = startyear
       while year <= endyear:
          windcf2 = float(row['WindCF'])
          #convert kWh  to PJ for the 40x40 cell
          windcf=windcf2*8760*600*10**(-9)*3.6*40*40*10**6*0.1
          dataToInsert += "Kenya  WI_%i\t%i\t%f\n" % (objectId, year, windcf)
          year = year + 1
       year=startyear
       while year <= endyear:
          ghi2 = float(row['GHI'])
          #convert kWh to PJ for the 40x40 cell
          ghi=ghi2*8760*10**(-9)*3.6*40*40*10**6*0.1
          dataToInsert += "Kenya  SO_%i\t%i\t%f\n" % (objectId, year, ghi)
          year=year+1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def inputact(outPutFile, inputactivity, startyear, endyear):
    #reset
    dataToInsert = ""
    ###########################################################################
    #Inputactivity ratio
    ###########################################################################
    print("Input activity", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param InputActivityRatio default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for j, row in inputactivity.iterrows():
       technology = row['Technology']
       #print(technology)
       fuel = row['Fuel']
       inputactivityratio = row['Inputactivity']
       year = startyear
       while year<=endyear:
          dataToInsert += "Kenya  %s\t%s\t1\t%i\t%f\n" % (technology, fuel, year, inputactivityratio)
          year = year + 1
       cnt = 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)
def SpecifiedDemandProfile(outPutFile, demand, demand_urban, demand_rural):
    #reset
    dataToInsert = ""
    #########################################################################
    #SpecifiedDemandProfile (region,fuel,timeslice,year,profile)
    ########################################################################
    print("SpecifiedDemandProfile", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    param = "param SpecifiedDemandProfile default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for j, row in demand.iterrows():
       elec_start = row['ElecStart']
       #objectId = row['OBJECTID *']

       if elec_start == 1:
          for k, row in demand_urban.iterrows():
             year = startyear
             while year<=endyear:
                demand_profile = demand_urban.loc[k][year]
                dataToInsert += "Kenya  EL3_%s\t%s\t%i\t%f\n" % (j, k, year, demand_profile)
                year = year + 1
          cnt = 1
       else:
          for m, row in demand_rural.iterrows():
             year = startyear
             while year <= endyear:
                demand_profile = demand_rural.loc[m][year]
                dataToInsert += "Kenya  EL3_%s\t%s\t%i\t%f\n" % (j, m, year, demand_profile)
                year = year + 1
          cnt=1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capacityfactor_wi(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar, solar_power, wind_power, timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE, timesliceND, batteryCF, battery13h, battery8h, startyear, endyear, months):
    dataToInsert = ""
    ###########################################################################
     #Capacityfactor (region,technolgy,timeslice,year,CF)
     ###########################################################################
    print("Capacity factor wind", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityFactor default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    ######### WIND ###########

    for k, row in df.iterrows():
       ObjectId = row['OBJECTID *']

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
             slice = sum(thisMonthOnly[ObjectId].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m+1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m+1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd)) # CHANGE 71 to actual OBJECTID!!!
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
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
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)   #divided by capacity 600 kW
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)   #divided by capacity 600 kW
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values))/wind_power)   #divided by capacity 600 kW
             dataToInsert += "Kenya  WI_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             m = m + 1

          year = year + 1

       cnt = 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capacityfactor_PV(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar, solar_power, wind_power,
                            timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE, timesliceND, batteryCF,
                            battery13h, battery8h, startyear, endyear,months):
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
       ObjectId = row['OBJECTID *']
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
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             try:
                 average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) /solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) /solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) /solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
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
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) /solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             try:
                average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             except ZeroDivisionError:
                 average_wind = 0
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             m = m + 1

          year = year + 1

       cnt = 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

def capacityfactor_solar_battery13h(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar, solar_power, wind_power,
                             timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE, timesliceND, batteryCF,
                             battery13h, battery8h, startyear, endyear, months):
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
       ObjectId = row['OBJECTID *']
       lastRowWasZero = False
       batteryConsumed = False
       index = 0
       for solarCapacity in capacityfactor_solar[ObjectId].values:
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
             capacityfactor_solar.at[index, ObjectId] = batteryCapacityFactor
             lastRowWasZero = True
             batteryTime -= 1
          elif not batteryConsumed:
             # This will happen when the last row was not zero and the current row is 0.
             capacityfactor_solar.at[index, ObjectId] = batteryCapacityFactor
             lastRowWasZero = True
             batteryTime -= 1
          index += 1
    capacityfactor_solar_batt = capacityfactor_solar.copy()
    capacityfactor_solar_batt.index = capacityfactor_solar_batt[0]
    #capacityfactor_solar = capacityfactor_solar.drop(columns=['0'])
    #capacityfactor_solar.columns = pd.to_numeric(capacityfactor_solar.columns)
    for k, row in df.iterrows():
       ObjectId = row['OBJECTID *']
       # print(ObjectId)
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
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
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
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(
                thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(
                thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV12h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV12h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOMG12h_%i\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             m = m + 1

          year = year + 1

       cnt = 1
    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)
def capacityfactor_solar_battery8h(elec, outPutFile, df, capacityfactor_wind, capacityfactor_solar, solar_power, wind_power,
                             timesliceDN, timesliceDE, timesliceED, timesliceEN, timesliceNE, timesliceND, batteryCF,
                             battery13h, battery8h, startyear, endyear, months):
   ######### Solar 8h battery ###############
    print("Capacity factor solar PV 8h", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityFactor default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    dataToInsert = ""

    for k, row in df.iterrows():
       ObjectId = row['OBJECTID *']

       batteryCapacityFactor = batteryCF
       batteryTime = battery8h
       lastRowWasZero = False
       batteryConsumed = False
       index = 0
       for solarCapacity in capacityfactor_solar[ObjectId].values:

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
             capacityfactor_solar.at[index, ObjectId] = batteryCapacityFactor
             lastRowWasZero = True
             batteryTime -= 1
          elif not batteryConsumed:
             # This will happen when the last row was not zero and the current row is 0. Same as above???
             capacityfactor_solar.at[index, ObjectId] = batteryCapacityFactor
             lastRowWasZero = True
             batteryTime -= 1
          index += 1
    capacityfactor_solar_batt_8 = capacityfactor_solar.copy()
    capacityfactor_solar_batt_8.index = capacityfactor_solar_batt_8[0]
    capacityfactor_solar_batt_8 = capacityfactor_solar_batt_8.drop(columns=[0])
    #capacityfactor_solar.columns = pd.to_numeric(capacityfactor_solar.columns)
    for k, row in df.iterrows():
       ObjectId = row['OBJECTID *']
       # print(ObjectId)
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
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
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
                thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceED
             sliceEnd = timesliceEN
             ts = "%iE" % (m + 1)
             slice = sum(
                thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = (
             (slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)

             sliceStart = timesliceNE
             sliceEnd = timesliceND
             ts = "%iN" % (m + 1)
             slice = sum(
                thisMonthOnly[(ObjectId)].between_time(sliceStart, sliceEnd))
             average_wind = ((slice / len(thisMonthOnly.between_time(sliceStart, sliceEnd)._values)) / solar_power)
             if ObjectId in elec.values:
                dataToInsert += "Kenya  SOPV8h_%i_1\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             dataToInsert += "Kenya  SOPV8h_%i_0\t%s\t%i\t%f\n" % (ObjectId, ts, year, average_wind)
             m = m + 1

          year = year + 1

       cnt = 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)

def outputactivity(outPutFile, df):
    #reset
    dataToInsert = ""
    ###########################################################################
    #Outputactivity ratio
    ###########################################################################
    print("Outputactivity", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param OutputActivityRatio default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    outputactivity = pd.read_excel('Kenya_data_input_ALL.xlsx', 'outputactivity', index_col=0)

    for j, row in outputactivity.iterrows():
       technology = row['Technology']
       fuel = row['Fuel']
       outputactivityratio = row['Outputactivity']
       year = startyear
       while year<=endyear:
          dataToInsert += "Kenya  %s\t%s\t1\t%i\t%f\n" % (technology, fuel, year, outputactivityratio)
          year = year + 1
    cnt = 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]


    #reset

def specifiedannualdemand(outPutFile, demand):
    #########################################################################
    #SpecifiedAnnualDemand (region,fuel,year,demand)
    ########################################################################
    print("Specified annual demand", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param SpecifiedAnnualDemand default 0 :=\n"
    dataToInsert = ""
    startIndex = outPutFile.index(param) + len(param)

    for j, row in demand.iterrows():
       year = startyear
       while year<=endyear:
          demandForThisYearAndObjectId = demand.loc[j][year]
          dataToInsert += "Kenya  EL3_%s\t%i\t%f\n" % (j, year, demandForThisYearAndObjectId)
          year = year + 1
    cnt = 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)
    #reset

def fixedcost(df, outPutFile,startyear, endyear, elec):
    ##############################################################
    #Fixed cost (Region,Technology,Year,Fixedcost)
    ################################################################
    print("Fixed cost", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param FixedCost default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)
    dataToInsert = ""
    #print(startIndex)

    for m, row in df.iterrows():
       objectId = row['OBJECTID *']
       cont = 1

       year = startyear
       # add for each year for one technology, total energy avaliable in each cell
       while year <= endyear:
          windfixedcost = float(row['FixedCostWind'])
          #\t gives tab
          dataToInsert += "Kenya  WI_%i\t%i\t%f\n" % (objectId, year, windfixedcost)
          year += 1
       year2 = startyear

       if objectId in elec.values:
          while year2 <= endyear:
             pvfixedcost = float(row['FixedCostPV'])
             dataToInsert += ("Kenya  SOPV_%i_1\t%i\t%f\n" % (objectId, year2, pvfixedcost))
             year2 = year2 + 1
          year2 = startyear
          while year2 <= endyear:
             pvfixedcost = float(row['FixedCostPV4h'])
             dataToInsert += ("Kenya  SOPV12h_%i_1\t%i\t%f\n" % (objectId, year2, pvfixedcost))
             year2 = year2 + 1
          year2 = startyear
          while year2 <= endyear:
             pvfixedcost = float(row['FixedCostPV8h'])
             dataToInsert += ("Kenya  SOPV8h_%i_1\t%i\t%f\n" % (objectId, year2, pvfixedcost))
             year2 = year2 + 1

       while year2 <= endyear:
          pvfixedcost = float(row['FixedCostPV'])
          dataToInsert += ("Kenya  SOPV_%i_0\t%i\t%f\n" % (objectId, year2, pvfixedcost))
          year2 = year2 + 1
       year2=startyear
       while year2 <= endyear:
          pvfixedcost = float(row['FixedCostPV4h'])
          dataToInsert += ("Kenya  SOPV12h_%i_0\t%i\t%f\n" % (objectId, year2, pvfixedcost))
          year2 = year2 + 1
       year2 = startyear
       while year2 <= endyear:
          pvfixedcost = float(row['FixedCostPV8h'])
          dataToInsert += ("Kenya  SOPV8h_%i_0\t%i\t%f\n" % (objectId, year2, pvfixedcost))
          year2 = year2 + 1
       year3 = startyear
       while year3 <= endyear:
          somgfixedcost = float(row['FixedCostSOMG'])
          dataToInsert += ("Kenya  SOMG_%i\t%i\t%f\n" % (objectId, year3, somgfixedcost))
          dataToInsert += ("Kenya  SOMG12h_%i\t%i\t%f\n" % (objectId, year3, somgfixedcost))
          year3 = year3 + 1
       while year3 <= endyear:
          somgfixedcost = 15
          dataToInsert += ("Kenya  KEDSGEN_%i\t%i\t%f\n" % (objectId, year3, somgfixedcost))
          year3 = year3 + 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return (outPutFile)
def capitalcost(df, outPutFile, elec, capitalcost_RET, trade_cost, wind_power, solar_power, capacityfactor_wind, capacityfactor_solar,startyear, endyear):
    dataToInsert = ""

     #################################################################
    #Capital cost (region,technology,year,capitalcost)
    ################################################################
    print("Capital cost", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapitalCost default 0 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    PV_MG_CF = [0.12, 0.14,0.155,0.17,0.20]
    PV_SA_CF = [0.13,0.15, 0.16,0.18, 0.21]
    Wind_CF = [0.48,0.47,0.45,0.44,0.41,0.37,0.31,0.25,0.19,0.125]
    Battery = [8,13]

    windcf_year = pd.capacityfactor_wind
    print(windcf_year)


    solarcf_year = []
    slice = sum(capacityfactor_solar[(ObjectId)])
    average_solar = ((slice / len(capacityfactor_solar._values)) / solar_power)

    for m, row in df.iterrows():
       ObjectId = row['OBJECTID *']
       year = startyear
       while year <= endyear:

          def find_nearest(Wind_CF, average_wind):
             arraywind = np.asarray(Wind_CF)
             idx = (np.abs(arraywind - average_wind)).argmin()
             return arraywind[idx]
          cf=find_nearest(Wind_CF, average_wind)
          windcapitalcost = capitalcost_RET.loc[cf][year]
          #windcapitalcost = float(row['CapitalCostWind'])
          dataToInsert += "Kenya  WI_%i\t%i\t%f\n" % (ObjectId, year, windcapitalcost)
          year += 1
       year2 = startyear
       while year2 <= endyear:
          #thisMonthOnly = capacityfactor_solar.query('date > @startDate and date < @endDate')

          def find_nearest(PV_SA_CF, average_solar):
             arraysun = np.asarray(PV_SA_CF)
             idx = (np.abs(arraysun - average_solar)).argmin()
             return arraysun[idx]
          cf=find_nearest(PV_SA_CF, average_solar)
          pvcapitalcost = capitalcost_RET.loc[cf][year2]
          #pvcapitalcost = float(row['CapitalCostPV'])
          if ObjectId in elec.values:
              dataToInsert += ("Kenya  SOPV_%i_1\t%i\t%f\n" % (ObjectId, year2, pvcapitalcost))
          dataToInsert += ("Kenya  SOPV_%i_0\t%i\t%f\n" % (ObjectId, year2, pvcapitalcost))
          year2 = year2 + 1
       year3 = startyear
       while year3 <= endyear:
          slice = sum(capacityfactor_solar[(ObjectId)])
          average_solar = ((slice / len(capacityfactor_solar._values)) / solar_power)
          #print(average_solar)
          def find_nearest(PV_MG_CF, average_solar):
             arraysun = np.asarray(PV_MG_CF)
             idx = (np.abs(arraysun - average_solar)).argmin()
             return arraysun[idx]
          #print(find_nearest(PV_MG_CF, average_solar))
          cf=find_nearest(PV_MG_CF, average_solar)
          somgcapitalcost = capitalcost_RET.loc[cf][year3]
          somg12hcapitalcost = capitalcost_RET.loc[cf][year3] + capitalcost_RET.loc[13][year3]
          #somgcapitalcost = float(row['CapitalCostSOMG'])
          dataToInsert += ("Kenya  SOMG_%i\t%i\t%f\n" % (ObjectId, year3, somgcapitalcost))
          dataToInsert += ("Kenya  SOMG12h_%i\t%i\t%f\n" % (ObjectId, year3, somg12hcapitalcost))
          year3 = year3 + 1
       year3 = startyear
       while year3 <= endyear:
          slice = sum(capacityfactor_solar[(ObjectId)])
          average_solar = ((slice / len(capacityfactor_solar._values)) / solar_power)
          #print(average_solar)
          def find_nearest(PV_SA_CF, average_solar):
             array = np.asarray(PV_SA_CF)
             idx = (np.abs(array - average_solar)).argmin()
             return array[idx]
          #print(find_nearest(PV_SA_CF, average_solar))
          cf=find_nearest(PV_SA_CF, average_solar)
          sopv4hcapitalcost = capitalcost_RET.loc[cf][year3]+capitalcost_RET.loc[13][year3]

          #somgcapitalcost = float(row['CapitalCostPV4h'])
          if ObjectId in elec.values:
              dataToInsert += ("Kenya  SOPV12h_%i_1\t%i\t%f\n" % (ObjectId, year3, sopv4hcapitalcost))
          dataToInsert += ("Kenya  SOPV12h_%i_0\t%i\t%f\n" % (ObjectId, year3, sopv4hcapitalcost))
          year3 = year3 + 1
       year3 = startyear
       while year3 <= endyear:
          slice = sum(capacityfactor_solar[(ObjectId)])
          average_solar = ((slice / len(capacityfactor_solar._values)) / solar_power)
          #print(average_solar)
          def find_nearest(PV_SA_CF, average_solar):
             arrayso = np.asarray(PV_SA_CF)
             idx = (np.abs(arrayso - average_solar)).argmin()
             return arrayso[idx]
          #print(find_nearest(PV_SA_CF, average_solar))
          cf=find_nearest(PV_SA_CF, average_solar)
          sopv8hcapitalcost = capitalcost_RET.loc[cf][year3]+capitalcost_RET.loc[8][year3]
          #somgcapitalcost = float(row['CapitalCostPV8h'])
          if ObjectId in elec.values:
              dataToInsert += ("Kenya  SOPV8h_%i_1\t%i\t%f\n" % (ObjectId, year3, sopv8hcapitalcost))
          dataToInsert += ("Kenya  SOPV8h_%i_0\t%i\t%f\n" % (ObjectId, year3, sopv8hcapitalcost))
          year3 = year3 + 1
     #### TRADE XYYX ######


    for m, row in trade_cost.iterrows():
      cost = row['Capitalcost']
      tech = row['Technology']

      year = startyear
      while year <= endyear:
         dataToInsert += "Kenya  %s\t%i\t%f\n" % (tech, year, cost)
         year += 1
      cnt = 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

#################################################
#CapacityToActivityUnit (region,technology,capacitytoactivityunit)
#################################################
def capacitytoactivity(trade,outPutFile):
    dataToInsert = ""
    print("Capacity to activity", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    param = "param CapacityToActivityUnit default 1 :=\n"
    startIndex = outPutFile.index(param) + len(param)

    for m, row in trade.iterrows():
       t = row['Capacitytoactivity']

       dataToInsert += "Kenya  %s\t31.536\n" % (t)

       cnt = 1

    outPutFile = outPutFile[:startIndex] + dataToInsert + outPutFile[startIndex:]
    return(outPutFile)

###############################################################
#write all to file
#########################################################
def write_to_file(file_object, outPutFile):
    print("write to file", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    with open(file_object, "w") as actualOutputFile:
       actualOutputFile.truncate(0) #empty the file
       actualOutputFile.write(outPutFile)
