from Helpers import run


def errorRunValidator(error):
    if error.find("not a git repository") != -1:
        print(messages["notGitRepository"])
    elif error.find("did not match any files") != 1:
        print(messages["notafile-error"])
    else:
        print(messages["unknown-error"])


def add(filePaths=[]):
    from pathlib import Path as isFile

    specificFiles = []
    for filePath in filePaths:
        if not isFile(filePath):
            break

        specificFiles.append(filePath)

    if len(specificFiles) > 0:
        run(errorRunValidator, ["git", "add"] + specificFiles)
        return print(messages["add-success"])

    if len(filePaths) > 0:
        return print("file not found")

    from Status import getStatus, setUp as setUpStatus
    from Tools.Inputs import prompts

    setUpStatus(messages)
    status = getStatus()

    options = []
    for statusId in status:
        statusContent = status[statusId]
        if statusId == "branch" or statusId == "added":
            continue

        options = options + statusContent

    if len(options) == 0:
        return print(messages["add-nofiles-error"])

    print()
    answers = prompts().multiSelect(title=messages["add-adition-title"],
                                    finalTitle=messages["file-selection-finaltitle"],
                                    options=options)

    if answers == "UNKNOWN_ERROR":
        return print(messages["unknown-error"])
    if len(answers) == 0:
        return print(messages["add-nofileschoosen-error"])

    from Helpers import removeColors

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(errorRunValidator, ["git", "add"] + choices)
    print(messages["add-success"])


def addAll():
    from Status import getStatus, setUp as setUpStatus
    from Tools.Inputs import prompts

    setUpStatus(messages)
    status = getStatus()

    hasFilesToAdd = False
    for statusId in status:
        if statusId == "branch" or statusId == "added":
            continue

        hasFilesToAdd = True
        break

    if hasFilesToAdd:
        run(errorRunValidator, ["git", "add", "."])
        print(messages["add-all-success"])
    else:
        print(messages["add-all-nofiles"])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "ADD_ALL":
        addAll()
    if subroute == "DEFAULT":
        add(router.leftKeys)
