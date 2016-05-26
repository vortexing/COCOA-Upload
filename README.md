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

### To upload files to synapse

```
./upload.py --synapse_user user --password password upload --input /path/to/file --sampleId sample123 --dataType exparray

#View ./upload.py upload -h for more help
```

### To annotate file in synapse


```
./upload.py annotate --annotation sample123 --dataType exparray

#View ./upload.py annotate -h for more help
```