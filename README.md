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
  - numpy (required by nmrglue)

```
pip install -r requirements.txt
```

### Execution

```
python3 nmr_meta_main.py --help 
python3 nmr_meta_main.py --nmr-data-local-folder=./data 

```


