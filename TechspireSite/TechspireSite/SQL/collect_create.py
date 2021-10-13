import glob
import os


def collect_create():
    output_paths = glob.glob("*/Create*.sql")
    out_file = open("Create.sql", "w")
    for path in output_paths:
        in_file = open(path)
        out_file.writelines(in_file.readlines())
        out_file.write("\n")


if __name__ == '__main__':
    collect_create()