from tools.md5 import to_md5


def load_configs():
    with open("game_ids.txt", "r") as infile:
        configs = [line.strip().split(",") for line in infile.readlines() if not line.startswith("#")]
    return configs


def detect(data):
    md5 = to_md5(data)
    configs = load_configs()
    for config in configs:
        if config[1] == md5:
            return config[0]
    exit("Unable to detect game with md5: " + md5)
