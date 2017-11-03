
import sys, os
import math
import argparse

Description="The program outputs two files for every one input file. In the first output, the program calculates movement of a molecule every 100 millisecond. Each molecule has a unique trackid. The script also get the log value of the molecular movement at 400 millisecond. In the second output file, molecular movement at every 100ms for every trackid is recorded in different columns and a mean value is calculated across each trackid for each 100 ms values."
usage="""
python {script} --inputfolder inputfoldername --output outputfoldername
python {script} --inputfolder inputfoldername --output outputfoldername --inputfile inputfilename
python {script} --inputfolder inputfoldername --output outputfoldername --inputfile inputfilename1 --inputfile inputfilename2 --inputfile inputfilename3
""".format(script=sys.argv[0])




parser=argparse.ArgumentParser(description=Description, epilog=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--inputfolder", dest="inputfolder", action="store", help="Input folder name where all csv files resides")
parser.add_argument("--outputfolder", dest="outputfolder", action="store", help="Output folder name where all the output files will be stored. If output folder does not exist, it will be created")
parser.add_argument("--inputfile", dest="inputfile", action="store", nargs='+', help="Specify inputfilename from inputfolder. You can give this option multiple time to specify more files.")

options=parser.parse_args()



def work_on_each_file(filename):
    basefilename=os.path.basename(filename)
    fh=open(filename)
    out1=open(options.outputfolder + "/" + basefilename + ".out1", "w")
    out2=open(options.outputfolder + "/" + basefilename + ".out2", "w")


    header=fh.readline().rstrip()
    firstline=fh.readline()
    linearray=firstline.rstrip().split(",")
    trackid=linearray[3]

    positionx=float(linearray[5])
    positiony=float(linearray[6])

    linearray[7]= str(pow((float(linearray[5]) - positionx ),2) + pow((float(linearray[6]) - positiony),2))

    out1.write(",".join(linearray)+"\n")
    counter=1
    filecounter=1

    data_dict=dict()
    data_dict[trackid]=[linearray[7]]
    for line in fh:
        line=line.rstrip()
        if line=="":
            continue
        array=line.split(",")
        if trackid==array[3]:
            array[7]=str(pow((float(array[5]) - positionx ),2) + pow((float(array[6]) - positiony),2))
            if counter==4:
                out1.write(",".join(array) + "," + str(math.log10(float(array[7])/4 * 0.4)) + "\n")
            else:
                out1.write( ",".join(array) + "\n")


            data_dict[trackid].append(array[7])
        else:
            trackid=array[3]    #new track id
            data_dict[trackid]=[]


            positionx=float(array[5])
            positiony=float(array[6])

            counter=1
            array[7]=str(pow((float(array[5]) - positionx ),2) + pow((float(array[6]) - positiony),2))
            out1.write(",".join(array) + "\n")

            data_dict[trackid].append(array[7])
        counter+=1

    fh.close()
    out1.close()

    #find the data_dict key with longest array
    max=0
    for key in data_dict.keys():
        if len(data_dict[key]) > max:
            max=len(data_dict[key])

    sorted_keys=sorted(data_dict.keys(), key=int)
    out2.write(",".join(sorted_keys) + ",Mean\n")

    for value in range(0, max):
        row_values=[]
        mean_values=[]
        for key in sorted_keys:
            if value <= len(data_dict[key])-1:
                row_values.append(data_dict[key][value])
                mean_values.append(float(data_dict[key][value]))
            else:
                row_values.append("")

        out2.write(",".join(row_values) + "," + str(sum(mean_values)/len(mean_values)) + "\n")
    out2.close()
    return



if not options.inputfolder and not options.inputfile:
    print "Please give the input folder name where there are mulitple csv input files."
    exit(0)
else:
    if not os.path.exists(options.inputfolder):
        print "Input folder does not exist. Please check it."
        exit(0)

if not options.outputfolder:
    print "Please give a output folder name.\n\n"
    exit(0)
else:
    if not os.path.exists(options.outputfolder):
        print "Output folder does not exist."
        print "Creating output folder"
        os.makedirs(options.outputfolder)

if options.inputfile:
    print "list of input files provided"
    print options.inputfile
    for filename in options.filename:
        work_on_each_file(filename)
else:
    # work on all files in inputfolder

    for filename in os.listdir(options.inputfolder):
        work_on_each_file(options.inputfolder + "/" + filename)


exit(0)
