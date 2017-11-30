filename = input("Enter filename")
pattern1 = input("Enter header string to remove")
pattern2 = input("Enter another header string to remove")
rep = ""

## function to filter file
def filter(file):
    newfile = open(file+".filtered","w")
    with open(file,"r") as fin:
        i = 1
        lines=fin.readlines()
        lines[1] = lines[1].replace(pattern1,rep)
        lines[1] = lines[1].replace(pattern2,rep)
        print(lines[1])
        for line in lines:
            # if
            if i > 1:
                if i == 2:
                    newfile.write(line)
                else:
                    # if more than 5 reads on average, write
                    linelist = line.split()
                    if float(linelist[7])+float(linelist[6])>10:
                        newfile.write(line)
            i = i + 1

filter(filename)

print("New, filtered count file created, named:",file+".filtered")
