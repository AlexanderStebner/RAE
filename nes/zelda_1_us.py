import json
import utils.config_handler

inner_palette_start = 0x18490

outer_palette_start = 0x18410

screen_ordering_start = 0x18590

COLUMN_GROUP_POINTER_TABLE = 0x19D1F
COLUMN_GROUPS = 0x15428


def extract(data):
    output_dir = "nes/zelda_1_us"
    files = {}

    # animations and sprites
    with open("nes/zelda_1_us.json", "r") as infile:
        config = json.load(infile)
    for asset in config['assets']:
        if asset['type'] in utils.config_handler.asset_types:
            files[asset['target']] = utils.config_handler.handle(data, config, asset)

    print("creating maps/map_overworld.json ... ", end="")
    files["maps/map_overworld.json"] = create_overworld_map(data)
    print("Done.")
    return output_dir, files


def create_overworld_map(data):
    # column group pointer table
    column_groups = {offset: int.from_bytes(
        data[COLUMN_GROUP_POINTER_TABLE + offset * 2:COLUMN_GROUP_POINTER_TABLE + offset * 2 + 2], 'little') + 0xC010
                     for offset in range(16)}

    def extract_column(pos):
        _column = []
        while len(_column) < 11:
            b = data[pos] & 0x7F  # ignore column start flag
            repeat = b >= 0x40  # repeat flag
            b &= 0x3F  # remove repeat flag
            _column.append(b)
            if repeat:
                _column.append(b)
            pos += 1
        return _column

    # get columns (16 each) for all 120 screens (map is 16x8, but some screens are duplicates)
    screens = []
    for screen_inx, x in enumerate(range(COLUMN_GROUPS, COLUMN_GROUPS + 16 * 121, 16)):
        screen = []
        for y in range(11):
            screen.append([None] * 16)
        columns = data[x:x + 16]
        for x_inx, column in enumerate(columns):
            search_pos = column_groups[column >> 4]
            column_index = column & 0x0F
            while True:
                if data[search_pos] >= 0x80:
                    if column_index == 0:
                        break
                    else:
                        column_index -= 1
                search_pos += 1
            column = extract_column(search_pos)
            for y_inx, cell in enumerate(column):
                screen[y_inx][x_inx] = cell
        screens.append(screen)

    # init output
    tile_mapping = {"5|3": "0|1|1", "6|3": "0|0|1", "7|3": "0|2|1", "8|3": "0|1|0", "9|3": "0|1|2",
                    "10|3": "0|4|0",
                    "11|3": "0|3|7", "14|3": "0|0|9", "19|3": "1|0|0", "21|3": "0|0|0", "22|3": "0|0|2",
                    "23|3": "0|2|0", "24|3": "0|2|2", "25|3": "1|0|1", "26|3": "0|5|1", "27|3": "0|6|1",
                    "28|3": "1|2|0", "29|3": "1|2|1", "30|3": "1|2|2", "31|3": "1|3|0", "32|3": "1|3|2",
                    "33|3": "1|0|3", "34|3": "1|0|5", "35|3": "1|0|6", "36|3": "1|1|3", "37|3": "1|1|6",
                    "45|3": "1|0|4", "46|3": "0|3|3", "47|3": "0|3|4", "48|3": "0|4|3", "49|3": "0|4|4",
                    "50|3": "0|5|0", "51|3": "0|5|2", "52|3": "0|6|0", "53|3": "0|6|2", "54|3": "0|4|7",
                    "55|3": "0|1|7",
                    "5|2": "0|1|4", "6|2": "0|0|4", "7|2": "0|2|4", "8|2": "0|1|3", "9|2": "0|1|5",
                    "10|2": "0|4|1",
                    "11|2": "0|3|8", "14|2": "0|0|9", "19|2": "1|1|0", "25|2": "1|1|1", "26|2": "0|5|4",
                    "27|2": "0|6|4",
                    "28|2": "1|4|0", "29|2": "1|4|0", "30|2": "1|4|2", "31|2": "1|5|0", "32|2": "1|5|2",
                    "33|2": "1|2|3", "34|2": "1|2|5", "35|2": "1|2|6", "36|2": "1|3|3", "37|2": "1|3|6",
                    "45|2": "1|2|4", "46|2": "0|3|5", "47|2": "0|3|6", "50|2": "0|5|3", "51|2": "0|5|5",
                    "52|2": "0|6|3", "53|2": "0|6|5",
                    "10|0": "0|4|2", "14|0": "0|4|8", "20|0": "1|0|2", "21|2": "0|0|3", "22|2": "0|0|5",
                    "23|2": "0|2|3", "24|2": "0|2|5", "25|0": "1|1|2", "26|0": "0|5|7", "27|0": "0|6|7",
                    "53|0": "0|6|8", "33|0": "1|4|3", "34|0": "1|4|5", "35|0": "1|4|6", "36|0": "1|5|3",
                    "37|0": "1|5|6", "45|0": "1|4|4", "50|0": "0|5|6", "51|0": "0|5|8", "52|0": "0|6|6"}

    output = {"tile_size": {"w": 16, "h": 16}, "screen_size": {"w": 14, "h": 11},
              "tile_sets": {"0": "tilesets/overworld.png", "1": "tilesets/overworld_objects.png"}}

    # mapping of game-tile-id & color offset to custom tile location in generated images

    # skip these. background and foreground layer may be needed for stairs / interactable objects.
    event_tiles = ["12|3", "12|2", "12|0", "15|3", "38|2", "38|3", "39|3", "39|2", "40|3", "40|2", "41|0",
                   "44|3", "44|2", "44|0"]

    tile_array = []
    for y in range(8 * 11):
        tile_array.append([None] * 16 * 16)

    offset = -1
    for screen_y in range(8):
        for screen_x in range(16):
            offset += 1
            screen = screens[data[screen_ordering_start + offset] & 0x7F]
            outer_palette = data[outer_palette_start + offset] & 0x3
            inner_palette = data[inner_palette_start + offset] & 0x3

            for y in range(11):
                for x in range(16):
                    palette = inner_palette if 2 <= y <= 8 and 2 <= x <= 13 else outer_palette
                    tile_id = str(screen[y][x]) + "|" + str(palette)
                    if tile_id in event_tiles:
                        continue
                    tile_array[screen_y * 11 + y][screen_x * 16 + x] = tile_id

    # output raw - split by tile set, but use default background tile behind 2nd layer objects
    pattern_to_bg_tile = {"0": "4|8", "2": "0|9", "3": "0|9"}
    bg_rows = []
    obj_rows = []
    for row in tile_array:
        bg_row = []
        obj_row = []
        for tile in row:
            if tile is None:
                bg_row.append("")
                obj_row.append("")
                continue
            locs = tile_mapping[tile].split("|", maxsplit=1)
            if locs[0] == "0":
                bg_row.append(locs[1])
                obj_row.append("")
            else:
                bg_row.append(pattern_to_bg_tile[tile[-1]])
                obj_row.append(locs[1])
        bg_rows.append(",".join(bg_row))
        obj_rows.append(",".join(obj_row))
    output['layers'] = {"0": bg_rows, "1": obj_rows}
    return json.dumps(output).encode(encoding="utf-8")
