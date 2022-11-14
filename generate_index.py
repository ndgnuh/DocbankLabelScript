import os
from os import path
from argparse import ArgumentParser


def generate_index(inputdir):

    assert path.isdir(inputdir)

    files = os.listdir(inputdir)
    files = [file for file in files if file.endswith(".txt")]

    outputfile = f"{inputdir.rstrip('/')}.index.txt"
    with open(outputfile, "w", encoding="utf-8") as f:
        f.write("\n".join(files))

    print(f"Output written to {outputfile}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputdir")

    args = parser.parse_args()

    generate_index(args.inputdir)
