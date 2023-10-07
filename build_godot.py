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
    # override = len(sys.argv) > 2 and sys.argv[2] == "override"

    source_path = "output/" + game_id
    godot_path = "godot/" + game_id

    if not os.path.isdir(source_path):
        exit("unable to find game assets in folder {}".format(source_path))

    if not os.path.isdir(godot_path):
        exit("unable to find godot template for game id '{}'".format(game_id))

    if not os.path.isfile(godot_path + "/create.txt"):
        exit("unable to find godot create file (create.txt)")

    # execute create script
    with open(godot_path + "/create.txt", "r", encoding="utf-8") as outfile:
        script = [l.replace("\n", "") for l in outfile.readlines() if not l.startswith("#")]

    for line in script:
        tokens = line.split(" ")
        if tokens[0] == "CP":
            source = tokens[1]
            target = tokens[1] if tokens[2] == "*" else tokens[2]
            target_path = godot_path + "/" + target
            os.makedirs(target_path[:target_path.rfind("/")], exist_ok=True)
            shutil.copy(source_path + "/" + source, target_path)
        elif tokens[0] == "MAP":
            map_file = source_path + "/" + tokens[1]
            target_file = godot_path + "/" + tokens[2]
            with open(map_file, "r", encoding="utf-8") as infile:
                map_data = json.load(infile)
            target_file_template = target_file + "_template"
            if not os.path.isfile(target_file_template):
                exit("unable to find template {}".format(target_file_template))
            with open(target_file_template, "r", encoding="utf-8") as infile:
                data = infile.read()
                for k, v in map_data['tile_sets'].items():
                    data = data.replace("%LAYER_" + k + "%", encode_godot_layer(int(k), map_data['layers'][k]))
            with open(target_file, "w", encoding="utf-8") as outfile:
                outfile.write(data)
