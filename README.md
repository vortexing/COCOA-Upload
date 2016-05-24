# COCOA-Upload

### Installing dependencies

*Installing pip*

ubuntu:
`sudo apt-get install python-pip`

linux:
`sudo yum install python-pip`

*Installing python modules*
```
pip install synapseclient
pip install pandas 
```

### How to run 

```
./upload.py -i microarray/ -a microarray/Pipeline/Microarray-Synapse-Annotations.csv --dataType exparray

#View ./upload.py -h for more help
```