import read as r
from tex import *


def make(f):
    data = r.parse(f)
    with open("latex/outTexFile.tex", "w") as file:
        addHead(file)
        newCMD(file)
        BEGAN_DOC(file)
        addPgStyle(file)
        tof(file)
        figure = 1
        for sec in data:
            addSection(file, sec, sec + "ID")
            for subsec in data[sec]:
                addSubSection(file, subsec, subsec + "ID")
                string = ""
                printStr = True
                for i in data[sec][subsec]:
                    if i[:2] == "@@":
                        addText(file, string, 1)
                        string = ""
                        printStr = False
                        nl(file)
                        addPic(file, 0.75, 2, "Screenshot of " + i[2:], "figure" + str(figure) + ".png")
                        figure += 1
                    else:
                        string += i

                if printStr:
                    addText(file, string, 1)
                    nl(file)

        END_DOC(file)
    return file
