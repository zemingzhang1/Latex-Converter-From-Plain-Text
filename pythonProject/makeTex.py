import read as r
from rename import *
from tex import *

def make(f):
    data = r.parse(f)
    print(data)
    retFile = None
    with open("outTexFile.tex", "w") as file:
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
                        addPic(file, 0.5, 2, "Screenshot of " + i[2:], "figure" + str(figure) + ".png")
                        figure += 1
                    else:
                        string += i

                if printStr:
                    addText(file, string, 1)
                    nl(file)

        END_DOC(file)
        retFile = file
        # dirInit()
    return retFile

    # with open("outTexFile.tex", "w") as file:
    #     addHead(file)
    #     newCMD(file)
    #     BEGAN_DOC(file)
    #     addPgStyle(file)
    #     tof(file)
    #
    #     for i in range(0,4):
    #         addSection(file, "secA"+ str(i), "secA"+ str(i))
    #         addSubSection(file, "subA" + str(i), "subB" + str(i))
    #         addText(file, tt, 1)
    #         nl(file)
    #         addPic(file, 0.5, 2, "text pic" + str(i), "download.png")
    #
    #     END_DOC(file)