import os
import subprocess
import read

beganDoc = "\\begin{document}\n"
endDoc = "\\end{document}\n"
newLine = "\n"
nl = lambda file: file.write("\n")
tab = "\t"
floatBarrier = "\\FloatBarrier"

BEGAN_DOC = lambda file: file.write(newLine + beganDoc)
END_DOC = lambda file: file.write(newLine + endDoc)

tof = lambda file: file.write(newLine +
                              "\\renewcommand*\contentsname{Table of Contents}" + newLine +
                              "\\tableofcontents" + newLine +
                              "\\renewcommand{\listfigurename}{Illustrations}" + newLine +
                              "\\listoffigures" + newLine +
                              "\\newpage"
                              + newLine)

headTex = ["\\documentclass{article}",
           "\\usepackage[T1]{fontenc}"
           "\\usepackage[utf8]{inputenc}",
           "\\usepackage{lmodern}",
           "\\usepackage{graphicx}",
           "\\usepackage{textcomp}",
           "\\usepackage{lastpage}",
           "\\usepackage[section]{placeins}",
           "\\usepackage[hidelinks]{hyperref}",
           "\\usepackage{fancyhdr}",
           "\\usepackage{nameref}"]

newCMD = lambda file: file.write(newLine
                                 + "\\makeatletter" + newLine
                                 + "\\newcommand*{\currentname}{\@currentlabelname}" + newLine
                                 + "\\makeatother"
                                 + newLine)

section = [lambda nM: "\\section{" + nM + "}",
           lambda ID: "\\label{sec:" + ID + "}"]

subSection = [lambda nM: "\\subsection{" + nM + "}",
              lambda ID: "\\label{subsec:" + ID + "}"]

addPic = lambda file, width, level, caption, name: file.write(newLine +
                                                              tab * level + "\FloatBarrier" + newLine +
                                                              tab * level + "\\begin{figure}[h!]" + newLine +
                                                              tab * (level + 1) + "\\centering" + newLine +
                                                              tab * (
                                                                      level + 1) + "\\frame{\\includegraphics[width=" + str(
    width) + "\\textwidth]{" + name + "}}" + newLine +
                                                              tab * (
                                                                      level + 1) + "\\caption{" + caption + "}" + newLine +
                                                              tab * level + "\\end{figure}" + newLine +
                                                              tab * level + "\FloatBarrier" + newLine
                                                              + newLine)

pageSyle = {1: "\\pagestyle{fancy}",
            2: "\\fancyhf{}",
            3: "\\fancyhead[L]{Page ends at \\currentname}",
            4: "\\fancyfoot[C]{Page \\thepage}",
            5: "\\renewcommand{\headrulewidth}{1pt}"}


def addHead(file):
    nl(file)
    for i in headTex:
        file.write(i + newLine)


def addPgStyle(file):
    nl(file)
    for i in pageSyle.values():
        file.write(i + newLine)


def addSection(file, id, name):
    nl(file)
    file.write(section[0](id) + newLine)
    file.write(section[1](name) + newLine)


def addSubSection(file, id, name):
    nl(file)
    file.write(tab + floatBarrier + newLine)
    file.write(tab + subSection[0](id) + newLine)
    file.write(tab + subSection[1](name) + newLine)


def addText(file, text, levels):
    nl(file)
    file.write(tab * levels + text)


tt = "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin " \
     "literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney " \
     "College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, " \
     "and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum " \
     "comes from sections 1.10.32 and 1.10.33 of \"de Finibus Bonorum et Malorum\" (The Extremes of Good and Evil) by " \
     "Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. " \
     "The first line of Lorem Ipsum, \"Lorem ipsum dolor sit amet..\", comes from a line in section 1.10.32. "
