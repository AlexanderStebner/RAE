Retro Asset Extractor ("RAE")
---------------------

Structural ToDos:
- setup.py - installs libraries
- main.py - uses paths from CL (or ask for input), detects platform and game, and outputs to target folder
    - may accept further command line arguments, i.e. file output format
- folder "platforms", subfolders per system, subfolders per game (each including an executable script and ideally a readme.md)
- folder "utils" on every folder level
- file "game_detector.py" with maybe a config file that lists byte offsets/lengths and comparison values + the path & file name of the python library that should handle the extraction
- every extractor script should accept an input path

---

Creating a new extractor:
- create a python script with a function "extract" that takes a byte array and a list of command line arguments
    - e.g. `def extract(data, args)`
    - put it into `platforms/{game console}/{game title}`. If the console sub-folder doesn't exist, create it. 
    - add a README.md file in the game folder that explains what data your code extracts and from where.
- your `extract` function should return an array of `OutputFile` objects. They contain the file data as well as information on file type, file name and relative output path.
- have a look at other extractors to get a feeling for how to structure the extraction code.
- make sure to check for any already created extraction or conversion utils for the same platform, so you can keep your code small and won't need to reinvent the wheel.
- make sure that all output files follow the general structure outlined below.
- make sure that you either extract all available resources (images, animations, sounds, music, level maps etc.) or that you leave a TODO note in the README.md of your code.
- finally add the new extractor to the `game_configs.txt` including a byte extract that helps the `game_detector.py` identify your game.

Basic file formats:
- the array of `OutputFile` objects should consist of the following file types (to be extended if necessary):
    - png: used for almost all graphical output, i.e. sprites, tilesets, backgrounds; anything where correct and lossless pixel data is needed
        - animations and all frames that belong to the same object should be put into the same image (with equal width and height).
            - this would e.g. include Mario's running animation as well as his jumping and ducking image. Small Mario however would constitute a separate object.
    - jpg: may be used for larger photo like images (only when saving space is an issue)
    - wav: used for shorter audio clips, like sound effects. May be used for music
    - mp3: used for longer audio clips, like background music
    - csv: all-purpose format for any kind of tabulated data (e.g. character sheets, monster stats)
    - json: all-purpose format for any other kind of structured / nested data (e.g. map data)
    
    