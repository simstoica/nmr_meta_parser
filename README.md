# nmr_meta_parser
Parse metadata of nmr measurements 

## Authors

S. Stoica

University of Groningen


##  Description

This repository contains the code to extract the metadata of NMR measurements performed with the Varian of Brocker machines at the Stratingh Institute. 

The extracted metadata will be attached to the stored data in the RDMS system. 
## Requirements
### Python

- Python 3 (>= 3.8)
- pip-21.1.3
- Python packages
  - nmrglue
  - python-irodsclient


## Virtual environment
```
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Execution

The following command will display the help for using the tool:

```
python3 nmr_meta_main.py --help 

usage: nmr_meta_main.py [-h] [--irods-env-file IRODS_ENV_FILE] [--irods-auth-file IRODS_AUTH_FILE] --nmr-data-local-folder NMR_DATA_LOCAL_FOLDER
                        --nmr-data-rdms-folder NMR_DATA_RDMS_FOLDER [--log-level {info,debug,warning}] [--nmr-csv-name NMR_CSV_NAME]

optional arguments:
  -h, --help            show this help message and exit
  --irods-env-file IRODS_ENV_FILE
                        Local path to the environment file.If no authentication file has been provided, system will select default ~/.irods/irods_environment.json
                        (default: None)
  --irods-auth-file IRODS_AUTH_FILE
                        Local path to the corresponding authentication file.If no authentication file has been provided, system will select default ~/.irods/.irodsA
                        (default: None)
  --nmr-data-local-folder NMR_DATA_LOCAL_FOLDER
                        Local path to the folder with the organized nmr data (default: current working directory)
  --nmr-data-rdms-folder NMR_DATA_RDMS_FOLDER
                        Path on the rdms with the organized nmr data (default: None)
  --log-level {info,debug,warning}
                        Level of information to be given in the logs (default: info)
  --nmr-csv-name NMR_CSV_NAME
                        File name of the summary CSV with metadta (default: )
  --max-depth MAX_DEPTH
                        Max depth level of the experiment folder with respect to the requested folder. (default: 4)
  --analyse-localy ANALYSE_LOCALY
                        Use to investigate the metadata on the local folder.If set to y, the system will only analyse the
                        metadata locally without looking at any irods environment (default: n)

```
When both the `--irods-env-file` and `--irods-auth-file` are empty, the script will automatically select the current active irods connection. Alternatively, one can provide a corresponding pair `--irods-env-file` and `--irods-auth-file` 

#### Remark
 when copying an irods authentication file to a new location, the modification time of that file will change. To restore the original modification time, one can use the foloowing command:
 
 ```
 touch -d "$(date -R -r .irodsA)" test_auth_file_irodsA
 ``` 

`.irodsA` is in this case the original file  and `test_auth_file_irodsA` is the copy file that will at the end have the same modification time as the original. 

#### Example of usage:

When running the following 

```
python3 nmr_meta_main.py --nmr-data-local-folder=./data --nmr-data-rdms-folder=/rugZone/home/user/data
```

the tool searches the local folder `./data` for nmr experiments. For every experiment found, it checks whether the corresponding data is already on the RDMS system and that the metadata has not yet been attached.

if the metadata has not yet been attached on RDMS, the metadata is extracted from the local experiment folder and attached to the corresponding RDMS experiment folder. 

The `--max-depth` parameter can be provided as a paremeter to accelerate the search of the local folder. The depth search for experiments stops when the `max_depth` has been reached.

When investigating the experiments on the local folder and their metadata, or in the absence of and RDMS setup, one can use the `--analyse-localy=y`. This option allows exploring the local folder, and eventually, if requested, prints the collected metadata to the specified CSV file.

```
python nmr_meta_main.py --analyse-localy=y --nmr-data-local-folder=./data --log-level=info --nmr-csv-name=./data/nmr_metadata_v20221214T1200.csv
```