#!/usr/bin/python

import csv
import json
import argparse
import os
import calendar


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

def main():

	parser = argparse.ArgumentParser( description="csv 2 json" )
	parser.add_argument( "-i", help="The input csv file to be processed.", required = True)
	parser.add_argument( "-o", help="The output directory for the json files.", required = True)
	parser.add_argument( "-t", help="The input type (fish, benthic, fishpond, hcbc).")

	pa = parser.parse_args()

	if not os.path.exists(pa.o):
		os.makedirs(pa.o)

	csv_reader = csv.DictReader(open(pa.i, 'rU'), dialect=csv.excel_tab, delimiter=',')

	lat_syn = ['latitude','lat','latitude_dd']
	long_syn = ['longitude','long','longitude_dd']
	date_syn = ['date_','date','observationdate']
	time_syn = ['sampling time']

	string_keys = []

	if pa.t:
		if pa.t == 'benthic':
			float_keys = ['SITE_MAX_DEPTH', 'SITE_MAX_DEPTH', 'MINDEPTH' , 'MAXDEPTH', 'COLONYLENGTH', 'COLONYWIDTH', 'COLONYHEIGHT','EXTENT','SEVERITY','OLDDEAD','RECENTDEAD']
			int_keys = ['Count']

		elif pa.t == 'fish':
			float_keys = ['HARD_CORAL', 'SOFT_CORAL', 'MA' , 'CCA_', 'TA', 'SAND_', 'TUNICATE','ZOANTHID','CORALLIMORPH','CLAM','CYANO','SPONGE','OTHER_','OTHER_TYPE','SIZE_','SLOPE_MIN_DEPTH','SLOPE_MAX_DEPTH','SUBSTRATE_HEIGHT_0','SUBSTRATE_HEIGHT_20','SUBSTRATE_HEIGHT_50','SUBSTRATE_HEIGHT_100','SUBSTRATE_HEIGHT_150','MAX_HEIGHT']
			int_keys = ['Count']

		elif pa.t == 'hcbc':
			float_keys = ['PctCoralUnbleached','Depth_ft','AreaSurveyed_m2','PctCoralUnbleached','PctCoralPartialBleached','PctCoralFullyBleached']
			int_keys = []
			string_keys = ['TotalAreaSurveyed_m2','PercentLiveCoralCover','PctCoralBins']

	month_abbr = list(calendar.month_abbr)
	
	counter = 0
	for row in csv_reader:
		counter += 1

		lat = None
		long = None  
		date = None
		time = None

		for key in row:
			if key.lower() in lat_syn:
				lat = row[key]
				lat_key = key
			elif key.lower() in long_syn:
				long = row[key]
				long_key = key
			elif key.lower() in date_syn:
				date = row[key]
				date_key = key
			elif key.lower() in time_syn:
				time = row[key]
				time_key = key
			elif key in string_keys:
				row[key] = str(row[key])
				if "'" in row[key]: 
					row[key] = row[key].replace("'","")
			elif len(row[key]) == 0:
				if pa.t:
					if(key in float_keys): 
						row[key] = float(0)
					elif(key in int_keys): 
						row[key] = int(0)
			elif key == 'AreaSurveyed_m2':
				if isfloat(row[key]):
					row[key] = float(row[key])
				elif row[key].endswith(' m'):
					row[key] = float(row[key][:-2])
				elif row[key].endswith('m'):
					row[key] = float(row[key][:-1])
				else:
					row[key] = float(0)
			elif (key=='Bleaching_YNas10' or key=='DataProvidedNow_YNas10' or key=='PublicMandate_YNas10'):
				if isint(row[key]):
					row[key] = int(row[key])
				elif row[key] == 'Y': row[key] = 1
				elif row[key] == 'N': row[key] = 0
			elif isint(row[key]):
				row[key] = int(row[key])
			elif isfloat(row[key]):
				row[key] = float(row[key])

		if lat and long:
			del row[lat_key]
			del row[long_key]
			
			lat_f = float(lat)
			long_f = float(long)

			if lat_f > 90 or lat_f < -90:
				lat_f = float(long)
				long_f = float(lat)

			row['location'] = [long_f, lat_f]
		if date:
			del row[date_key]

			if '/' in date:
				date_list = date.split('/')
				month = date_list[0]
				day = date_list[1]
				year = date_list[2]


				if int(month)>12:
					month = date_list[1]
					day = date_list[0]

				if(len(month)==1): month = '0' + month
				if(len(day)==1): day = '0' + day
				if(len(year)==2): year = '20' + year
			elif ' ' in date:
				date_list = date.split(' ')
				year = date_list[0]
				month = str(month_abbr.index(date_list[1]))

				if(len(year)==2): year = '20' + year
				if(len(month)==1): month = '0' + month
				day = '01'

			correct_date = year+'-'+month+'-'+day

			if time:
				del row[time_key]

				ampm = time[len(time)-3:]
				addition = 0
				if ampm == 'PM': addition = 12

				time_list = time[:-3].split(':')

				hour = time_list[0]
				if(len(hour)==0): hour = '0'
				hour = str(int(hour)+addition)
				if(len(hour)==1): hour = '0' + hour

				minute = time_list[1]
				if(len(minute)==1): minute = '0' + minute

				correct_time = hour+':'+minute+':00.000-1000'

				correct_date += 'T' + correct_time
					
			row['date'] = correct_date

			#print(date+' '+time)
			#print(correct_date)

		if "" in row:
			del row[""]

		json_file = open(os.path.join(pa.o,str(counter)+'.json'), "w") 
		json.dump(row, json_file)
		json_file.close()

if __name__ == "__main__":
    main()

