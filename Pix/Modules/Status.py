STATUS_MATCHES = {
    "##": "branch",
    "??": "untracked",
    "UU": "conflicted",
    "U": "conflicted",
    "M": "modified",
    "R": "renamed",
    "A": "added",
    "D": "deleted",
}


def search_in_status(
    files_searching,
    status,
    excluded_files=[],
    included_files=[],
    get_original_structure=False,
):
    matches = {} if get_original_structure else []

    for status_id in status:
        is_excluded_file = status_id in excluded_files
        is_included_file = not status_id in included_files

        if is_excluded_file if len(excluded_files) != 0 else is_included_file:
            continue

        changes = status[status_id]

        for change in changes:
            for file in files_searching:
                if get_original_structure:
                    if file == change:
                        carriedMatches = (
                            matches[status_id] if status_id in matches else []
                        )

                        matches[status_id] = (
                            carriedMatches
                            if change in carriedMatches
                            else [*carriedMatches, change]
                        )
                elif file.lower() in change.lower():
                    matches.append(change)

    return matches


def get_status_paths(
    status, excluded_files=["branch"], included_files=STATUS_MATCHES.values()
):
    file_paths = []

    for status_id in status:
        status_content = status[status_id]

        if not (status_id in excluded_files) and status_id in included_files:
            file_paths = file_paths + status_content

    return file_paths


def parse_change(status, change_id, change_name, path, THEME, ignoreColors):
    carried_change = status[change_name] if change_name in status else []

    if change_id == "R":
        oldFilePaths, newFilePaths = path.split(" -> ")
        oldFilePaths = oldFilePaths.split("/")
        newFilePaths = newFilePaths.split("/")

        for index in range(len(oldFilePaths)):
            if not oldFilePaths[index] == newFilePaths[index]:
                path = (
                    (oldFilePaths[:index] + newFilePaths[index:])
                    if ignoreColors
                    else (
                        oldFilePaths[:index]
                        + [THEME["th_modified"] + newFilePaths[index]]
                        + newFilePaths[index + 1 :]
                    )
                )

                path[-1] += "" if ignoreColors else THEME["th_reset"]

                path = "/".join(path)
                break

    status[change_name] = [*carried_change, path]

    return status


def get_status(ignoreColors=False):
    from .Helpers import run
    from Configuration.Theme import THEME

    status_data = run(["git", "status", "-sb"])
    status_data = status_data.rstrip().split("\n")

    status = {}
    for change_raw in status_data:
        change = change_raw[3:]
        change_id = change_raw[:2]
        first_letter, second_letter = change_id

        if change_id in STATUS_MATCHES:
            parse_change(
                status,
                change_id,
                STATUS_MATCHES[change_id],
                change,
                THEME,
                ignoreColors,
            )
            continue

        if first_letter != " ":
            parse_change(
                status, first_letter, STATUS_MATCHES["A"], change, THEME, ignoreColors
            )

        if second_letter != " ":
            parse_change(
                status,
                second_letter,
                STATUS_MATCHES[second_letter],
                change,
                THEME,
                ignoreColors,
            )

    return status


def show_status():
    from .Helpers import MessageControl

    m = MessageControl()
    status = get_status()

    print()
    if "branch" in status:
        branch_name = status.pop("branch")[0]
        m.log("branch", {"pm_branch": branch_name})

    if len(status) == 0:
        m.log("clean")

    for change_name in status:
        changes = status[change_name]

        m.log(f"{change_name}-title")
        for change in changes:
            m.log(change_name, {"pm_change": change})

    print()


def router(argument_manager, sub_route):
    if sub_route == "DEFAULT":
        show_status()
