def get_has_changes(change=""):
    from .Status import get_status

    status = get_status()

    return len(status.keys()) > 1 if change == "" else change in status


def get_remote_origin_name(string):
    start = string.find("/remotes/")
    end = string.find("/", start + 9)

    return string[start + 9 : end]


def get_branch_creator():
    from .Helpers import run

    branch_creator = ""
    current_branch = run(["git", "branch", "--show-current"])[:-1]
    creation_raw = (
        run([f"git", "log", "--walk-reflogs", "--oneline", current_branch])
        .strip()
        .split("\n")
    )

    if "Created" in creation_raw[-1]:
        branch_creator = (
            creation_raw[-1].split(" ")[-1]
            if not "/remotes/" in creation_raw[-1]
            else get_remote_origin_name(creation_raw[-1])
        )

    return branch_creator, current_branch


def branch_switch(branch_search):
    from .Prompts import select
    from .Helpers import run, MessageControl

    m = MessageControl()
    has_changes = get_has_changes()

    if has_changes:
        return m.log("error-haschanges")

    branches_raw = run(["git", "branch"])
    branches_spaced = branches_raw.rstrip().split("\n")

    if branches_spaced[0] == "":
        return m.log("error-branch-branches_not_found")

    if branch_search != "":
        branch_match = []
        for branch in branches_spaced:
            if branch.find(branch_search) != -1:
                branch_match.append(branch)

        if len(branch_match) == 0:
            return m.log("error-branch-match_not_found", {"pm_branch": branch_search})

        branches_spaced = branch_match

    branches = []
    actual_branch = ""
    for branch in branches_spaced:
        if branch[0] == "*":
            branch = branch[1:]
            actual_branch = branch.lstrip()

        branches.append(branch.lstrip())

    branch_selected = branches[0]

    if len(branches) > 1:
        from Configuration.Theme import INPUT_THEME, INPUT_ICONS

        print()
        branch_selected = select(
            title=m.get_message("branch-selection-title"),
            options=branches,
            error_message=m.get_message("operation-cancel"),
            colors=INPUT_THEME["BRANCH_SELECTION"],
            icons=INPUT_ICONS,
        )

        if branch_selected == "":
            return m.log("error-empty")

    if branch_selected != actual_branch:
        run(["git", "checkout", branch_selected])
        m.log("branch-success", {"pm_branch": branch_selected})
    else:
        m.log("branch-selection-same_branch", {"pm_branch": branch_selected})


def branchCreation():
    from .Prompts import many, confirm
    from .Helpers import run, MessageControl
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    has_changes = get_has_changes()

    if has_changes:
        return m.log("error-haschanges")

    options = ["feature", "refactor", "bugfix", "style"]
    scape_error = m.get_message("operation-cancel")

    print()
    answers = many(
        [
            {
                "type": "select",
                "title": m.get_message("branch-creation-type_title"),
                "options": options,
                "error_message": scape_error,
                "colors": INPUT_THEME["BRANCH_CREATION_TYPE"],
                "icons": INPUT_ICONS,
            },
            {
                "type": "text",
                "title": m.get_message("branch-creation-id_title"),
                "error_message": scape_error,
                "colors": INPUT_THEME["BRANCH_CREATION_ID"],
            },
            {
                "type": "text",
                "title": m.get_message("branch-creation-about_title"),
                "error_message": scape_error,
                "colors": INPUT_THEME["BRANCH_CREATION_ABOUT"],
            },
        ]
    )

    if len(answers) != 3:
        return m.log("error-empty")

    kind, ticket_id, about = answers
    ticket_id = ticket_id.upper().replace(" ", "-")
    about = about.lower().replace(" ", "-")

    branch = f"{kind}/{ticket_id}-{about}"

    m.log("preview", {"pm_preview": branch})

    should_create_branch = confirm(
        title=m.get_message("confirmation"),
        colors=INPUT_THEME["BRANCH_CREATION_CONFIRM"],
    )

    if should_create_branch:
        run(["git", "branch", branch])
        m.log("branch-success", {"pm_branch": branch})
    else:
        return m.log("operation-cancel")

    should_switch = confirm(
        title=m.get_message("branch-creation-shouldswitch"),
        colors=INPUT_THEME["BRANCH_CREATION_SWITCH"],
    )

    if should_switch:
        run(["git", "checkout", branch])
        m.log("branch-creation-switch_success", {"pm_branch": branch})
    else:
        m.log("branch-creation-switch_cancel")


def rename_branch():
    from .Helpers import run, MessageControl
    from .Prompts import text
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    current_branch = run(["git", "branch", "--show-current"])[:-1]

    print()
    new_branch_name = text(
        title=m.get_message("branch-rename-title"),
        error_message=m.get_message("operation-cancel"),
        place_holder=m.get_message("branch-rename-place_holder"),
        colors=INPUT_THEME["BRANCH_RENAME"],
        content=current_branch,
    )

    if new_branch_name == "":
        return print("branch name not valid")

    run(["git", "branch", "-m", new_branch_name])

    m.log(
        "branch-rename-success",
        {"pm_old_name": current_branch, "pm_new_name": new_branch_name},
    )


def router(argument_manager, sub_route):
    if sub_route == "BRANCH_CREATION":
        branchCreation()
    elif sub_route == "BRANCH_RENAME":
        rename_branch()
    elif sub_route == "DEFAULT":
        branch_switch(argument_manager.get_next_route())
