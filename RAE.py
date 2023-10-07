import os
import sys
import game_detector
import importlib


if __name__ == "__main__":
    input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_base_dir = sys.argv[2]
    else:
        output_base_dir = "output"

    # read ROM file
    with open(input_file, "rb") as infile:
        data = infile.read()

    # detect game
    target = game_detector.detect(data)
    print("detected game: " + target)
    module = importlib.import_module(target)

    base_path, files = module.extract(data)

    # write to output directory
    if not os.path.exists(output_base_dir + "/" + base_path):
        os.makedirs(output_base_dir + "/" + base_path)
    os.chdir(output_base_dir + "/" + base_path)
    for path, data in files.items():
        folders, file = path.rsplit("/", 1)
        if not os.path.exists(folders):
            os.makedirs(folders)
        with open(folders + "/" + file, "wb") as outfile:
            outfile.write(data)


