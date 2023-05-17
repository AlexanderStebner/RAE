prefix = "configs/"


def load_configs():
    def sanitize_config_line(line):
        line = line.strip().split(",")
        line[1] = int(line[1], 16)
        line[2] = bytearray.fromhex(line[2])
        return line
    with open("game_ids.txt", "r") as infile:
        configs = [sanitize_config_line(line) for line in infile.readlines() if not line.startswith("#")]
    return configs


def detect(data):
    configs = load_configs()
    for config in configs:
        if len(data) < config[1] + len(config[2]):
            continue
        if data[config[1]:config[1] + len(config[2])] == config[2]:
            return prefix + config[0]
    exit("Unable to detect game.")
