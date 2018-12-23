import argparse
import os
import re


def parse_cmd_file(build_dir, file):
    patterns = r"source_.* := (.*)"
    patterns += r"|\s+\$\(wildcard\s+(.*)\)"
    patterns += r"|\s+(/.*) +"
    patterns += r"|\s+([a-zA-Z]+.*) +"

    built_files = []
    fp = open(file)
    for line in fp:
        m = re.match(patterns, line)
        if m:
            if m.group(1):
                path = m.group(1)
                if not path.startswith("/"):
                    path = os.path.join(build_dir, path)
                built_files.append(path)
            elif m.group(2):
                path = os.path.join(build_dir, m.group(2))
                if os.path.exists(path) and os.path.getsize(path) != 0:
                    built_files.append(path)
            elif m.group(3):
                built_files.append(m.group(3))
            elif m.group(4):
                path = os.path.join(build_dir, m.group(4))
                built_files.append(path)
    fp.close()
    return built_files


def parse_build(source_dir, build_dir):
    built_files = []
    for dirpath, subdirs, files in os.walk(build_dir):
        for file in files:
            if file.endswith(".cmd") and file != "auto.conf.cmd" and not file.endswith(".mod.cmd"):
                built = parse_cmd_file(build_dir, os.path.join(dirpath, file))
                built_files = {}.fromkeys(built + built_files).keys()
    return built_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("build_dir", help="Enter which dir the kernel was build in (Under Linux)", type=str)
    parser.add_argument("-s", "--source_dir",
                        help="Enter kernel source dir (Under Linux); "
                             "If not present it is the same with build dir or can deduced by build dir",
                        type=str)
    parser.add_argument("-o", "--output", help="Enter output file name, default output.txt", default="output.txt", type=str)
    args = parser.parse_args()
    if not os.path.exists(args.build_dir):
        print("Build Dir didn't exist!!!")
        return

    build_dir = os.path.abspath(args.build_dir)
    print("Build DIR:" + build_dir)
    if args.source_dir:
        source_dir = os.path.abspath(args.source_dir)
    else:
        source_dir = os.path.join(build_dir, "source")
        if os.path.exists(source_dir):
            print("Get source dir from build dir source symbolic link")
            source_dir = os.path.realpath(source_dir)
        else:
            print("source symbolic link didn't exists, assume source dir is the same witdh build dir")
            source_dir = build_dir
    print("Source DIR:" + source_dir)

    built_files = parse_build(source_dir, build_dir)
    built_files.sort()

    print("write to file:" + args.output)
    output = open(args.output, "w")
    for file in built_files:
        output.write(os.path.realpath(file)+"\n")
    output.close()
    print("done!!!")


if __name__ == '__main__':
    main()
