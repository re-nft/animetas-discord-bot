env_file: str = ".env"


def set_env_file(input_env_file):
    global env_file
    env_file = input_env_file


def get_env_file():
    global env_file
    return env_file
