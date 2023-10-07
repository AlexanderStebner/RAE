import os
import json
import utils.config_handler

output = {}
files = os.listdir("delete_me")
for file in files:
    with open("delete_me/" + file, "rb") as infile:
        data = infile.read()
    cnt = len(data) / 32.0

    config = """
       {
      "target": "all_sprites/""" + file[:-4] + """.png",
      "type": "png",
      "palettes": {
    "1": {
      "0x0": "000000",
      "0x1": "993300",
      "0x2": "CC8800",
      "0x3": "EEAAAA"
    }},
      "description": "",
      "target_size": {
        "w": """ + str(8 * int(cnt)) + """,
        "h": 16
      },
      "elements": {
        """ + "\n,".join(["\"" + str(x) + """": {
          "module": "2bpp",
          "template": "8x16-sprite",
          "start": \"""" + hex(x * 32) + """",
          "palette": "1"
        }""" for x in range(int(cnt))]) + """
      },
      "encoding": {
        "module": "png",
        "offsets": [
        ]
      }
    }
    """

    asset = json.loads(config)
    asset['encoding']['offsets'] = [str(x) + "|0|" + str(int(x*8)) for x in range(int(cnt))]

    output[asset['target']] = utils.config_handler.handle(data, asset, asset)
output_base_dir = "output"
base_path = "nes/zelda_1_us"
if not os.path.exists(output_base_dir + "/" + base_path):
    os.makedirs(output_base_dir + "/" + base_path)
os.chdir(output_base_dir + "/" + base_path)
for path, data in output.items():
    folders, file = path.rsplit("/", 1)
    if not os.path.exists(folders):
        os.makedirs(folders)
    with open(folders + "/" + file, "wb") as outfile:
        outfile.write(data)
