Folder [scripts](scripts/) contains python scripts for 
* converting csv tables into json files
* indexing json files for elasticsearch and kibana

===================================

**INSTALL**

* [java jdk](http://docs.oracle.com/javase/8/docs/technotes/guides/install/install_overview.html)
* [python](https://www.python.org/downloads/)
* [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)
* [kibana](https://www.elastic.co/downloads/kibana), [setup kibana](https://www.elastic.co/guide/en/kibana/current/setup.html)

=====================================

**RUN locally**

* run elasticsearch in the console by command
```
elasticsearch
```
* run kibana in the console:
```
cd PATH_TO_KIBANA_FOLDER
./bin/kibana
```
* open the address ```localhost:5601``` in the browser

* stop elasticsearch and kiband by pressing CTRL+C in both consoles

=====================================

**CONVERT csv data to json**

```
cd PATH_TO_csv2kibana_FOLDER/scripts
python csv2json.py -i PATH_TO_CSV_FILE -o PATH_TO_FOLDER_WITH_JSON_FILES [-t DATA_TYPE_NAME]
```

The parameter -t is optional, it specifies the data type name, the current possibilities are: 'benthic' (for NOAA data), 'fish' (for NOAA data), 'fishpond' (for Richardson's data).

=====================================

**INDEX json data**

```
python index_jsons.py -i PATH_TO_FOLDER_WITH_JSON_FILES -n INDEX_NAME -t TYPE_NAME [--host HOST_NAME]
```

INDEX_NAME is any name you want to give to your index, later the same name will be specified in kibana. TYPE_NAME is any name of the type of the data you want to give. The parameter --host is optional, it specifies the host name, the default is 'http://localhost:9200'.
