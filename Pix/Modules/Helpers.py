def removeColors(string):
    while "\u001b" in string:
        start = string.index("\u001b")
        end = string.index("m", start) + 1
        string = string[:start] + string[end:]

    return string


def _errorRunValidator(error):
    m = MessageControl()

    if error.find("not a git repository") != -1:
        m.log("error-not_git_repository")

    elif error.find("files would be overwritten by merge") != -1:
        m.log("error-conflicting_files_by_merge")

    elif error.find("already exists") != -1:
        m.log("error-branch-rename-repeated_name")

    elif error.find("is not a valid branch name") != -1:
        m.log("error-branch-rename-not_valid")

    else:
        m.log("error-unknown")


def run(command=[], should_expect_error=True):
    from subprocess import Popen, PIPE

    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if should_expect_error and process.returncode != 0:
        _errorRunValidator(error)
        exit()

    return output


def runAll(commands=[]):
    for command in commands:
        run(command)


def check_route(keyword, outsideKeys, outsideAliases):
    childKeys = outsideKeys["CHILD_KEYS"] if "CHILD_KEYS" in outsideKeys else []
    childAliases = (
        outsideAliases["CHILD_ALIASES"] if "CHILD_ALIASES" in outsideAliases else []
    )

    for entityId in childKeys:
        posibleRoutes = childKeys[entityId] + childAliases[entityId]

        if keyword in posibleRoutes:
            return entityId

    return "DEFAULT"


def check_pix_shortcut(keyword, outsideKeys, outsideAliases):
    for entityId in outsideKeys:
        keys = outsideKeys[entityId]["KEYS"]
        aliases = outsideAliases[entityId]["ALIASES"]
        posibleRoutes = keys + aliases

        if keyword in posibleRoutes:
            return entityId

    return False


def parse_selection_options(options):
    parsed_options = []
    index_id = 0

    for option in options:
        parsed_options.append({"value": option, "display_name": option, "id": index_id})
        index_id += 1

    return parsed_options


class MessageControl:
    def __init__(self):
        from Configuration.Theme import THEME, ICONS
        from Configuration.Messages import MESSAGES

        self.THEME = {**THEME, **ICONS}
        self.RESET = THEME["th_reset"]
        self.messages = MESSAGES

    def get_message(self, message_id, params={}):
        return (
            str(self.messages[message_id]).format(**self.THEME, **params) + self.RESET
        )

    def log(self, message_id, params={}):
        print(self.get_message(message_id, params))

    def logMany(self, contents, param_name, message_id, show_last_line=True):
        param = {}

        for content in contents:
            param[param_name] = content
            self.log(message_id=message_id, params=param)

        if show_last_line:
            print()
