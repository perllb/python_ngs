#!~/anaconda3/bin/python
import sys, getopt
import pandas as pd
import numpy as np
import os.path
import sys

def main(argv):
    gtfname = ''
    feature = ''
    try:
        opts, args = getopt.getopt(argv,"hi:f:",["ifile=","feat="])
    except getopt.GetoptError:
        print ('usage: test.py -i <gtf-file to convert> -f <features> ')
        sys.exit(2)
    if len(opts) > 1:
        for opt, arg in opts:
            if opt == 'gi':
                print ('usage: test.py -i <gtf-file to convert> -f <features> ')
                sys.exit()
            elif opt in ("-i","--ifile"):
                gtfname = arg
            elif opt in ("-f","--feat"):
                feature = arg
        print("Inputfile: "+gtfname)
        print("Features:  "+feature)
    else:
        print ('usage: test.py -i <gtf-file to convert> -f <features> ')
        sys.exit()

    while not os.path.isfile(gtfname) :
        print("> '" + gtfname + "' does not exist..")
        gtfname = input(">> Please enter GTF file to convert to BED or exit ('q'): ")
        if gtfname == 'q':
            sys.exit()

    print("> " + gtfname + " will be converted to BED")

    # read gtf file
    print("> Reading gtf file '" + gtfname + "..")
    gtf = pd.read_csv(gtfname,sep='\t',header=None,comment='#')

    print('Feature: ' + feature)

    if feature=='all':
        bed = gtf[[0,3,4,8,5,6]]
        bed.to_csv(gtfname.replace('.gtf','.all.bed'),sep="\t",header=None,index=False)
        print("> Printed to: " + gtfname.replace('.gtf','.all.bed'))
    else:
        # function to get feature from each row
        def getFeature(annotation,feature):
            """
            getIndex: get index of the feature in current annotation list
            """
            idx=0
            annot.ind=-1
            for i in annotation:
                if i.strip().find(feature)==0:
                    annot.ind=idx
                idx+=1
            if annot.ind > -1:
                return annotation[annot.ind].strip().split(" ")[1].replace("\"","")
            else:
                return None
        annot = gtf[8].apply(lambda x: x.split(';'))
        a = pd.DataFrame(annot.apply(lambda x: getFeature(x,feature)))

        df1 = pd.DataFrame(gtf[[0,3,4]])
        df2 = pd.DataFrame(a)
        df3 = pd.DataFrame(gtf[[5,6]])

        bed = pd.concat([df1,df2,df3],axis=1)
        bedname = gtfname.replace('.gtf','.' + feature + '.bed')
        bed.to_csv(bedname,sep="\t",header=None,index=False)
        print("> Printed to: " + bedname)





if __name__ == "__main__":
    main(sys.argv[1:])
