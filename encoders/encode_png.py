import png
import io


def encode(elements, asset, args):
    data = []
    for row in range(asset['target_size']['h']):
        data.append([0, 0, 0, 0] * asset['target_size']['w'])
    for einx, (name, element) in enumerate(elements.items()):
        offsets = [o.split("|") for o in args['offsets'] if not o.startswith("#")]
        copies = [o for o in offsets if o[0] == name or o[0].startswith(name + "/")]
        for offset in copies:
            parts = offset[0].split("/")
            if len(parts) == 2:
                variant = element[parts[1]]
            elif len(parts) == 1:
                variant = list(element.values())[0]
            else:
                exit("There shouldn't be any slashes in element names: " + offset[0])

            flip_h = 'flip_h' in offset
            flip_v = 'flip_v' in offset
            y = int(offset[1])
            for row in reversed(variant) if flip_v else variant:
                x = int(offset[2]) * 4
                row = reversed(row) if flip_h else row
                for pixel in row:
                    if pixel is None:
                        x += 4
                        continue
                    else:
                        if y >= len(data) or x >= len(data[y]):
                            break
                        data[y][x] = int(pixel[0:2], 16)
                        data[y][x+1] = int(pixel[2:4], 16)
                        data[y][x+2] = int(pixel[4:6], 16)
                        data[y][x+3] = 255
                    x += 4
                y += 1

    stream = io.BytesIO()
    w = png.Writer(asset['target_size']['w'], asset['target_size']['h'], greyscale=False, alpha=True)
    w.write(stream, data)
    stream.seek(0)
    return stream.read()
