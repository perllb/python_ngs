#!~/anaconda3/bin/python
import sys, getopt
import pandas as pd
import numpy as np
import os.path
import sys

def printUsage():
    print ('usage: \n> python bedToGtf.py -i <bed-file to convert> -f <features> -a <annotation> -l <level> -o <outfile (optional)>')
    print ('-f <feature> : What will you call ID (e.g. gene_name)')
    print ('-a <annotation> : What annotation database is it? (e.g. RepeatMasker)')
    print ('-l <level> : What type of feature is it? (e.g. exon)')
    print ('-o <outfile> : Name of out gtf file. Optional, and a suitable name will be given if not specified.')

def main(argv):
    bedname = ''
    feature = 'all'
    ann = ''
    level = ''
    outfile = None
    outArg = 'F'
    try:
        opts, args = getopt.getopt(argv,"hi:f:a:l:o:",["ifile=","feature=","annotation=","level=","outfile="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)
    if len(opts) > 3:
        for opt, arg in opts:
            if opt == 'gi':
                printUsage()
                sys.exit()
            elif opt in ("-i","--ifile"):
                bedname = arg
                outfile = bedname.replace('.bed','.gtf')
            elif opt in ("-f","--feature"):
                if feature != 'all':
                    feature = arg
            elif opt in ("-a","--annotation"):
                ann = arg
            elif opt in ("-l","--level"):
                level = arg
            elif opt in ("-o","--outfile"):
                outfile = arg
                outArg = 'T'
        print("Inputfile:  "+bedname)
        print("Features:   "+feature)
        print("Annotation: "+ann)
        print("Level:      "+level)
        if outfile==None:
            outfile = gtfname.replace('.gtf','.' + feature + '.bed')
        print("Outfile:   "+outfile)
    else:
        printUsage()
        sys.exit()

    while not os.path.isfile(bedname) :
        print("> '" + bedname + "' does not exist..")
        bedname = input(">> Please enter BED file to convert to GTF or exit ('q'): ")
        if bedname == 'q':
            sys.exit()

    print("> " + bedname + " will be converted to GTF")

    # read bed file
    print("> Reading bed file '" + bedname + "..")
    bed = pd.read_csv(bedname,sep='\t',header=None,comment='#')

    # no specified feature, take the ID used in the bedfile
    if feature=='all':
        annVec = np.repeat(ann,len(bed[0]))
        levVec = np.repeat(level,len(bed[0]))
        i = bed[3].apply(lambda x: level + " \'" + x + "\';")
        gtf = pd.DataFrame({'a':bed[0],'b':annVec,'c':levVec,'d':bed[1],'e':bed[2],'f':bed[4],'g':bed[5],'h':bed[4],'i':i})
        gtf.to_csv(outfile,sep="\t",header=None,index=False)
        print(gtf.head())
        print("> Printed to: " + outfile)

    # featureName (e.g. gene_name) is specified, and has to be added manually
    else:
        featureVec = np.repeat(feature + ' \"',len(bed[0]))
        last = np.repeat('\"',len(bed[0]))
        vec2 = np.core.defchararray.add(featureVec,bed[3])
        vec3 = np.core.defchararray.add(vec2,last)

        df1 = pd.DataFrame(bed[[0,np.repeat(ann,len(bed[0])),np.repeat(level,len(bed[0])),1,2,4,5,4]])
        df2 = pd.DataFrame(vec3)

        gtf = pd.concat([df1,df2],axis=1)
        if outArg == 'F':
            outfile = bedname.place('.bed','.' + feature + '.gtf')
        gtf.to_csv(outfile,sep="\t",header=None,index=False)
        print("> Printed to: " + outfile)


if __name__ == "__main__":
    main(sys.argv[1:])
