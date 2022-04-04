import os
import glob


def desktop():
    try:
        desktp = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        return desktp
    except:
        print("path is not Windows; failed")
    else:
        print(desktp)

    try:
        desktp = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        return desktp
    except:
        print("path is not Mac; failed")
    else:
        print(desktp)


def p():
    return desktop() + "/input"


def dirInit():
    pathF = p()
    try:
        os.mkdir(pathF)
    except OSError:
        print("Creation of the directory %s failed" % pathF)
    else:
        print("Successfully created the directory %s" % pathF)


def reName():
    pathF = p()
    image_list = []
    count = 0
    print(pathF)
    for filename in glob.iglob(str(pathF) + "/*.png", recursive=True):
        print(filename)

        # Absolute path of a file
        image_list.append(filename)
        count += 1
        os.rename(filename, str(pathF) + "/figure" + str(count) + ".png")
        # Renaming the filed
    return image_list


# if __name__ == '__main__':
#     reName()
