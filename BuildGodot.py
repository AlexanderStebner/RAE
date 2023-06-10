import os
import sys
import json
import shutil
from distutils.dir_util import copy_tree


def encode_godot_layer(layer, data):
    entries = []
    base_position = 0
    for y, row in enumerate(data):
        columns = row.split(",")
        for x, column in enumerate(columns):
            position = base_position + x
            if column == "":
                continue
            coords = column.split("|")
            tileset_y = int(coords[0])
            tileset_x = int(coords[1])
            entries.extend([str(position), str(layer + 65536 * tileset_x), str(tileset_y)])
        base_position += 65536
    return ",".join(entries)


if __name__ == "__main__":
    game_id = sys.argv[1]
    asset_base_path = sys.argv[2]
    output_dir = sys.argv[3]
    override = len(sys.argv) > 4 and sys.argv[4] == "override"

    source_path = asset_base_path + "/" + game_id
    godot_path = "godot/" + game_id

    if not os.path.isdir(source_path):
        exit("unable to find game assets in folder {}".format(source_path))

    if not os.path.isdir(godot_path):
        exit("unable to find godot template for game id '{}'".format(game_id))

    if not os.path.isfile(godot_path + "/create.txt"):
        exit("unable to find godot create file (create.txt)")

    if override:
        try:
            shutil.rmtree(output_dir)
        except:
            pass

    if os.path.isdir(output_dir):
        exit("output directory not empty")
    else:
        os.makedirs(output_dir)

    # copy godot template files
    print("copying godot template..")
    copy_tree(godot_path, output_dir)
    os.remove(output_dir + "/create.txt")

    # execute create script
    with open(godot_path + "/create.txt", "r", encoding="utf-8") as outfile:
        script = [l.replace("\n", "") for l in outfile.readlines() if not l.startswith("#")]

    for line in script:
        tokens = line.split(" ")
        if tokens[0] == "CP":
            source = tokens[1]
            target = tokens[1] if tokens[2] == "*" else tokens[2]
            target_path = output_dir + "/" + target
            os.makedirs(target_path[:target_path.rfind("/")], exist_ok=True)
            shutil.copy(source_path + "/" + source, target_path)
        elif tokens[0] == "MAP":
            map_file = source_path + "/" + tokens[1]
            target_file = output_dir + "/" + tokens[2]
            with open(map_file, "r", encoding="utf-8") as infile:
                map_data = json.load(infile)
            with open(target_file, "r", encoding="utf-8") as infile:
                data = infile.read()
                for k, v in map_data['tile_sets'].items():
                    data = data.replace("%LAYER_" + k + "%", encode_godot_layer(int(k), map_data['layers'][k]))
            with open(target_file, "w", encoding="utf-8") as outfile:
                outfile.write(data)
