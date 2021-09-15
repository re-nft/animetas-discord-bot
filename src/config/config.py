import configparser

try:
    with open("cfg.ini", "r") as f:
        pass
except FileNotFoundError:
    raise FileNotFoundError(
        "Config file not found. Please make sure cfg.ini exists.")

cfg = configparser.ConfigParser()
cfg.read("cfg.ini")
