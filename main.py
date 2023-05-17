import json
import sys
import importlib
import game_detector

if __name__ == "__main__":
    input_file = sys.argv[1]

    # read ROM file
    with open(input_file, "rb") as infile:
        data = infile.read()

    # detect game
    target = game_detector.detect(data)

    # load config
    config = json.load(open(target, ))

    # create output file objects
    pass

    # perform any file modifications
    pass

    # write to output directory
    pass

