import json
import utils.config_handler
import struct


def extract(data):
    output_dir = "gb/mario_land_1_us"
    files = {}

    # animations and sprites
    with open("gb/mario_land_1_us.json", "r") as infile:
        config = json.load(infile)
    for asset in config['assets']:
        if asset['type'] in utils.config_handler.asset_types:
            files[asset['target']] = utils.config_handler.handle(data, config, asset)

    files["maps/levels.json"] = create_map(data)
    print("Done.")
    return output_dir, files


# block data has a fairly simply structure:
# - it consists of 20 columns (=1 screen), separated by 0xFE
# - one byte indicates a y location (right below score = 0) and a count of how many blocks/sprites
# are to be drawn starting from that location going down. E.g. 0x23 means start from y=2 and the next 3 bytes are
# objects to be drawn from there on downwards.
# - the object-bytes are simple 1-to-1 matches with the tile map
# special cases:
# y0 - no byte count = directly add every byte from position y
# y0 FD nn - repeats the block nn from y to screen end
# yt FD nn - repeats the block nn from y, t times
def get_block_data(data, block_pointer):
    columns = []
    column = []
    column_pointer = block_pointer
    while len(columns) < 20:
        next_byte = data[column_pointer]
        column_pointer += 1
        if next_byte == 0xFE:
            columns.append(column)
            column = []
        else:
            column.append(next_byte)

    # screens are 20 bytes wide and 16 bytes high (s.a.)
    byte_map = [[0 for _ in range(20)] for _ in range(16)]

    for x, column in enumerate(columns):
        y = 0
        obj_count = 0
        skip = 0
        direct_mode = False
        for binx, byte in enumerate(column):
            if skip > 0:
                skip -= 1
                continue
            if direct_mode:
                if byte == 0xFD:
                    for y2 in range(y, 0x10):
                        byte_map[y2][x] = column[binx + 1]
                    break
                else:
                    byte_map[y][x] = byte
                    y += 1
                    continue
            if obj_count == 0:  # object list header
                y = byte // 0x10
                obj_count = byte % 0x10
                if obj_count == 0:
                    direct_mode = True
                    continue
            else:
                if byte == 0xFD:
                    for y2 in range(y, y + obj_count):
                        byte_map[y2][x] = column[binx + 1]
                    obj_count = 0
                    skip = 1
                else:
                    byte_map[y][x] = byte
                    obj_count -= 1
                    y += 1
    return byte_map


# memory locations of level tile data
tile_pointers = [0xa192,
                 0xa1b7,
                 0xa1da,
                 0x55bb,
                 0x55e2,
                 0x5605,
                 0xd03f,
                 0xd074,
                 0xd09b,
                 0x5630,
                 0x5665,
                 0x5694]


def create_map(data):
    # 12 levels
    for level in range(12):
        # blocks are used to group same vertical columns
        block_pointers_start = block_pointers_end = tile_pointers[level]
        bank = block_pointers_start // 0x4000
        for loc in range(block_pointers_start, len(data)):
            if data[loc] == 0xFF:
                block_pointers_end = loc
                break
        block_pointers_data = data[block_pointers_start:block_pointers_end]
        block_pointers = [struct.unpack("<H", block_pointers_data[inx:inx + 2])[0] for inx in
                          range(0, len(block_pointers_data), 2)]
        # block pointers point to where the column data for this reusable block is stored
        # (stored in the same rom bank as the block pointer)
        maps = [get_block_data(data, bp + (bank - 1) * 0x4000) for bp in block_pointers]

        # the extracted maps always start with the world's first screen (can be skipped in our case),
        # followed by 2 bonus rooms & then all other screens
        maps = maps[1:]


        print("")
