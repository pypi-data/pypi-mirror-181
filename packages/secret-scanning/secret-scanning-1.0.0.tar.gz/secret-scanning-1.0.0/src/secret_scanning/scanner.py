import tomli
import regex


def load_config_file():
    with open('secrets_config.toml', 'rb') as toml_file:
        try:
            return tomli.load(toml_file)
        except tomli.TOMLDecodeError as toml_error:
            raise Exception(f'Error parsing config file: {toml_error}') from toml_error


class Scanner(object):

    def __init__(self):
        self.config = load_config_file()

    def scan_for_secrets(self, text):
        found_secrets = []
        rules = self.config['rules']
        for rule in rules:
            if 'regex' in rule:
                regex_pattern = rule['regex']
                matches = regex.findall(regex_pattern, text, concurrent=True)
                if matches:
                    found_secrets.append({"description": rule['description'], "matches": matches,
                                          "id": rule['id'], "keywords": rule['keywords']})
        return found_secrets
