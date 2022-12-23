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

    # extract files into cache
    module = None
    try:
        module = importlib.import_module(target)
    except ImportError as e:
        exit(e)
    output_files = module.extract(data, sys.argv[2:])

    # perform any file modifications
    pass

    # write to output directory
    pass

