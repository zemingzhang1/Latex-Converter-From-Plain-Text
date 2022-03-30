data = {}
currentSection = ""
currentSubsection = ""

def parse(file):
    for i in file.split("\n"):
        print(i)
        if i[:1] == "~":
            if i[:2] == "~~":
                currentSubsection = i[2:].strip("\n").strip("")
                data[currentSection][currentSubsection] = []
            else:
                currentSection = i[1:].strip("\n").strip("")
                data[currentSection] = {}
        else:
            if i.strip("\n") != "":
                data[currentSection][currentSubsection].append(i.strip("\n"))
    return data