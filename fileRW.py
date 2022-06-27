def file_reader(filename):
    with open(filename, "r+", encoding="UTF-8") as fReader:
        lines = fReader.read()
        context = lines.split('\n')
        return context


def file_writer(filename, input_str):
    with open(filename, "a+", encoding="UTF-8") as fWriter:
        fWriter.write(input_str)


def main():
    filename = "test.txt"
    file_writer("test.txt", "GOOD")
    context = file_reader(filename)
    print(context)



if __name__ == "__main__":
    main()

