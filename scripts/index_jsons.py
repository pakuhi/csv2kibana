#!/usr/bin/python

import json
import argparse
import os

def main():

	parser = argparse.ArgumentParser( description="Index json files with elastic search" )
	parser.add_argument( "-i", help="The input dir with json files to be processed.", required = True)
	parser.add_argument( "-n", help="The index name.", default = 'caindex')
	parser.add_argument( "-t", help="The type name.", default = 'catype')
	parser.add_argument( "--host", help="Host name.", default = 'http://localhost:9200')

	pa = parser.parse_args()

	cmd_line = "curl -XDELETE '%s/%s/'" % (pa.host, pa.n)
	os.system(cmd_line)

	not_analyzed_template_line = """{
  		"template": "%s",
		  "mappings": {
		    "_default_": {
		      "dynamic_templates": [
			{
			  "strings": {
			    "match_mapping_type": "string",
			    "mapping": {
			      "type": "string",
			      "index": "not_analyzed"
			    }
			  }
			}
		      ]
		    }
		  }
		}""" % pa.n

	template_addr_not_an = pa.host + '/_template/template_not_an'
	cmd_line = "curl -XPUT '" + template_addr_not_an + "'" + " -d " + "'" + not_analyzed_template_line + "'"
	os.system(cmd_line)


	location_mapping_line = """{
	    "mappings": {
		"%s": {
		    "properties": {
		        "location": {"type": "geo_point"},
			"date": {
          			"type":   "date",
          			"format": "date_optional_time"
		    	}
		    }
		}
	    }
	}""" % pa.t

	loc_addr = pa.host + '/' + pa.n
	cmd_line = "curl -XPUT '" + loc_addr + "'" + " -d " + "'" + location_mapping_line + "'"
	os.system(cmd_line)

	#date_mapping_line = """{
	#    "mappings": {
	#	"%s": {
	#	    "date": {
        #  		"type":   "date",
        ##  		"format": "MM/dd/yyyy"
	#	    }
	#	}
	#    }
	#}""" % pa.t

	#date_addr = pa.host + '/' + pa.n
	#cmd_line = "curl -XPUT '" + date_addr + "'" + " -d " + "'" + date_mapping_line + "'"

	#os.system(cmd_line)




	for fileind in range(1,len(os.listdir(pa.i))+1):
		filename = str(fileind) + '.json'
		json_file = open(os.path.join(pa.i,filename), 'r')
		json_line = json_file.readline()

		addr = pa.host + '/' + pa.n + '/' + pa.t + '/' + str(fileind)	
		cmd_line = "curl -XPUT '" + addr + "'" + " -d " + "'" + json_line + "'"
		os.system(cmd_line)


if __name__ == "__main__":
    main()

