import json
import utils.config_handler

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

    files["map_overworld.csv"] = create_overworld_map(data)
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
    #output = {"tile_size": {"w": 16, "h": 16}, "screen_size": {"w": 14, "h": 11},
    #          "tile_sets": {"0": "tilesets/overworld.png", "1": "tilesets/overworld_objects.png"},
    #          "tile_ids": {"5", "6", "7", "8", "9", "10", "11", "12",
    #                       "14": "0|1|4", "15", "19", "20", "21", "22", "23", "24", "25",
    #                       "26": "0|3|4",
    #                       "27": "0|4|4" "1", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55"}}

    # TODO: make above efficient. Need to create own mapping of tile ids to tileset locations (0|1|4), not based on game.
    # Then create a map in code that maps game-tile-id + palette info (below) to final custom tile-id

    # create custom tile ids (tile set, y, x)
    tile_ids = []
    for y in range(7):
        for x in range(9):
            tile_ids.append("0|{}|{}".format(y, x))
    for y in range(6):
        for x in range(7):
            tile_ids.append("1|{}|{}".format(y, x))

    # mapping of game-tile-id | color offset to custom tile-id
    tile_mapping = {"27":""}

    offset = -1
    for y in range(16):
        for x in range(8):
            offset += 1
            screen = screens[data[0x18590 + offset]]
            outer_palette = data[0x18410 + offset] & 0x3
            inner_palette = data[0x18490 + offset] & 0x3
            print("")

    # get the screen ordering 0x18590
    for p_inx in range(0x18590, 0x18590 + 16 * 8):
        print(str(int(data[p_inx] & 0x7f)) + " ", end="")
        if (p_inx + 1) % 16 == 0:
            print("")

    # get the palette definitions per screen id
    for p_inx in range(0x18410, 0x18410 + 16 * 8):
        print(str(data[p_inx] & 0x3) + " ", end="")
        if (p_inx + 1) % 16 == 0:
            print("")

    # output raw:

    return ""
