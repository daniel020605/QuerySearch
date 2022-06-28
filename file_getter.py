import fileRW


def getfile(filename):
   with open(filename, "r+", encoding="UTF-8") as fReader:
        ret = ""
        lines = fReader.read()
        for line in lines:
          ret = ret + (line.rstrip(","))
        context = lines.split('\n')
        return ret

if __name__ == '__main__':
    f1 = getfile("种草文章.txt")
    print(f1)