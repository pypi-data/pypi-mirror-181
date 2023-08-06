# hdf5-extractor

Extract mini hdf5 files from an epc and an H5 file. 
The mini-h5 are created by finding Datasets referenced from the epc. Each representation will have its own mini-h5 file.

# installation :

## With poetry :

```console
poetry add hdf5extractor
```

## With pip :

```console
pip install hdf5extractor
```

# Run :

Extract a small h5 from a bigger one, to only have dataset of a specific resqml file : 
```console
extracth5 -i myResqmlFile.xml --h5 myH5File.h5 -o outputFolder
```

Extract every h5 parts from a bigger one, to only have in each, the dataset of a specific resqml file inside an epc : 
```console
extracth5 -i myEPCFile.epc --h5 myH5File.h5 -o outputFolder
```