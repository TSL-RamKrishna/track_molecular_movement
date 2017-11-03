# track_molecular_movement
Scientific research often includes studying a molecular movement in a cell. A machine can track each molecule and output a csv file. This program takes a csv file and calculates the molecular movement at every 100ms.

## Usage:

1) python script_to_molecular_movements.py --inputfolder testinputfolder --output outputfolder
2) python script_to_molecular_movements.py  --output outputfolder --inputfile testinputfolder/test1.csv 
3) python script_to_molecular_movements.py  --output outputfolder --inputfile testinputfolder/test1.csv testinputfolder/test2.csv


For each input csv file, there are two output files in output folder. The output filename ends with out1 and out2.
