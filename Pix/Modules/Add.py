def add(file_paths=[], should_verify=True, messages=""):
    from .Prompts import multi_select
    from .Helpers import run, removeColors, MessageControl
    from .Status import get_status, search_in_status, get_status_paths
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl() if messages == "" else messages
    status = get_status()

    is_individual_path = len(file_paths) == 1
    file_paths = (
        search_in_status(file_paths, status, excluded_files=["branch", "added"])
        if len(file_paths)
        else get_status_paths(status, excluded_files=["branch", "added"])
    )

    if len(file_paths) == 0:
        return m.log("error-add-files_not_found")
    elif not should_verify:
        run(["git", "add"] + file_paths)
        return m.log("add-all-success")
    elif is_individual_path and len(file_paths) == 1:
        return run(["git", "add"] + file_paths)

    print()
    answers = multi_select(
        title=m.getMessage("add-title"),
        final_title=m.getMessage("file-selection-finaltitle"),
        error_message=m.getMessage("error-files_selected_not_found"),
        options=file_paths,
        colors=INPUT_THEME["ADD_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(answers) == 0:
        return m.log("error-files_selected_not_found")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "add"] + choices)
    m.log("add-success")


def add_individually(file_paths):
    from .Helpers import MessageControl

    m = MessageControl()

    if len(file_paths):
        for file_path in file_paths:
            add(file_paths=[file_path], messages=m)

        return m.log("add-success")

    add(should_verify=False, messages=m)


def router(argument_manager, sub_route):
    if sub_route == "ADD_ALL":
        add(should_verify=False)
    if sub_route == "DEFAULT":
        add_individually(argument_manager.left_keys)
