import importlib


asset_types = ['png']


def handle(data, config, asset):
    print("creating " + asset['target'] + " ... ", end="")

    # extract
    elements = {}
    for name, args in asset['elements'].items():
        module = importlib.import_module("extractors.extract_" + args['module'])
        result = module.extract(data, config, args)
        elements[name] = result

    # encode
    args = asset['encoding']
    module = importlib.import_module("encoders.encode_" + args['module'])
    result = module.encode(elements, asset, args)
    print("Done.")
    return result
