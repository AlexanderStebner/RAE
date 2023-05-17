import json
import utils.config_handler


def extract(data):
    output_dir = "nes/zelda_1_us"
    files = {}

    with open("nes/zelda_1_us.json", "r") as infile:
        config = json.load(infile)
    for asset in config['assets']:
        if asset['type'] in utils.config_handler.asset_types:
            files[asset['target']] = utils.config_handler.handle(data, config, asset)
    return output_dir, files
