Retro Asset Extractor ("RAE")
---------------------

Files:
- setup.py - installs libraries
- main.py - uses paths from CL (or asks for input), detects platform and game, and outputs to target folder
    - may accept further command line arguments, i.e. file output format(?)
- folder "configs", subfolders per system - each containing a list of json configuration files
- file "game_detector.py" with a config file that lists byte offsets/lengths and comparison values + the path & file name of the json file that defines the extraction
- folder "extractors": extraction modules as needed by configuration
- folder "encoders": encoders for turning internal format into final output

---

Structure of a json configuration:
```
{
  title: "Zelda DX (USA)",
  ...other game-related metadata...
  assets: [
    {
      source_file: "relative file path or empty if single file",
      target: "relative filepath in output folder",
      note: "optional note",
      // maybe any output sound info etc. any file-related metadata:
      e.g., element_size: {w: 100, h: 100}, // size info for multi-image animation files
      
      elements: [ // separately extracted images / sounds etc. 
        {
          module: "path/to/py/extractor",
          template: "optional template name with module parameters",
          x: 123,
          y: 321,
          ...other parameters for extractor...
          repeat: 2, // optionally repeat element in elements list so encoding can use it again
        }, ...
      ],
      encoding: {
        module: "path/to/encoder",
        template: "optional template",
        offsets: [{x: 1, y: 1}, ...] // <- any parameters, one per element
      }
    },...
  ]
}
```

- the config is processed by iterating over the asset groups.
- for each group, the source file is loaded
- then each `element` is processed:
  - The module is called with the binary file data and parameters that are a combination of the template and any additional settings.
  - Template configs are optionally stored in an extra file next to the module, e.g. `2bpp.templates.py` for `2bpp.py`.
  - Each extractor returns a simple common modifiable data object. E.g., a bitmap array for image data.
- All returned data objects are collected and send as an array to the module specified in `encoding`.
- Also added are template parameters and any other parameters (that will e.g., contain a list of offsets in the final output file for each separate extracted element.)
- The encoder returns a final binary file.
- This, combined with any metadata from the configuration json, is then later written to the output folder.

Basic file formats (subject to change):
- the output files should consist of the following file types (to be extended if necessary):
    - png: used for almost all graphical output, i.e. sprites, tilesets, backgrounds; anything where correct and lossless pixel data is needed
        - animations and all frames that belong to the same object should be put into the same image (with equal width and height).
            - this would e.g. include Mario's running animation as well as his jumping and ducking image. Small Mario however would constitute a separate object.
    - jpg: may be used for larger photo like images (only when saving space is an issue)
    - wav: used for shorter audio clips, like sound effects. May be used for music
    - mp3: used for longer audio clips, like background music
    - csv: all-purpose format for any kind of tabulated data (e.g. character sheets, monster stats)
    - json: all-purpose format for any other kind of structured / nested data (e.g. map data)
    
    