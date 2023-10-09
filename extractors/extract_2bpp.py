def override_if_none(args, field, value):
    if field in args:
        return
    args[field] = value


def enrich_from_template(args):
    template = args['template']
    if template.endswith("-sprite"):
        override_if_none(args, 'bg_color', None)
        override_if_none(args, 'invisible_color', "000000")
    if template == "16x16-sprite":
        override_if_none(args, 'width', 16)
        override_if_none(args, 'height', 16)
    if template == "8x16-sprite":
        override_if_none(args, 'width', 8)
        override_if_none(args, 'height', 16)
    if template == "8x8-sprite":
        override_if_none(args, 'width', 8)
        override_if_none(args, 'height', 8)
    if template == "8x8-gb":
        override_if_none(args, 'width', 8)
        override_if_none(args, 'height', 8)
        override_if_none(args, 'bg_color', "ffffffff")
        override_if_none(args, 'adjacent_bytes', True)
    return args


def extract(data, config, args):
    if "template" in args:
        args = enrich_from_template(args)

    # prepare array and fill it with bg_color
    target = []
    for h in range(args['height']):
        row = []
        for w in range(args['width']):
            row.append(args['bg_color'])
        target.append(row)

    # print(args['adjacent_bytes'])

    # draw pixels
    offset_second_byte = 8 if not args['adjacent_bytes'] else 1
    y_target = 0
    x_target = 0
    start = int(args['start'], 0)
    loc = start
    while loc < start + 2 * 8 * (args['width'] / 8) * (args['height'] / 8):
        for inx, bit in enumerate(reversed(range(8))):
            # go bit by bit from left to right through all pixels in a 8-pixel row. Target color in palette is
            # 'bit of first byte + 2 * bit of second byte'. The second byte may come after each 8-byte block,
            # or directly after the first.
            pixel_part_1 = ((data[loc] >> bit) & 1)
            pixel_part_2 = ((data[loc + offset_second_byte] >> bit) & 1) * 2
            target[y_target][x_target + inx] = pixel_part_1 + pixel_part_2

        # pixel x,y in target image array
        y_target += 1
        if y_target % 8 == 0:
            loc += 8
        if y_target == args['height']:
            y_target = 0
            x_target += 8
        loc += 1 if not args['adjacent_bytes'] else 2

    # apply color palette(s)
    arg_palettes = args['palettes'] if 'palettes' in args else [args['palette']]
    invisible_colors = args['invisible_colors'] if 'invisible_colors' in args else [args['invisible_color']]

    collection = {}
    for inx, p in enumerate(arg_palettes):
        palette = config['palettes'][p]
        invisible = invisible_colors[inx] if inx < len(invisible_colors) else invisible_colors[0]
        palette = {int(k, 0): v if v != invisible else None for k, v in palette.items()}
        output = []
        for rinx, row in enumerate(target):
            output_row = []
            for cinx, column in enumerate(row):
                output_row.append(palette[column])
            output.append(output_row)
        collection[p] = output

    return collection
