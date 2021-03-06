KEYS = {
    "STATUS": {
        "KEYS": ["status", "work"]
    },
    "ADD": {
        "KEYS":["add"], 
        "CHILD_KEYS": {
            "ADD_ALL": ["all"]
        }
    },
    "REMOVE": {
        "KEYS": ["remove"], 
        "CHILD_KEYS": {
            "REMOVE_ALL": ["all"]
        }
    },
    "COMMIT": {
        "KEYS": ["commit"],
    },
    "BRANCH": {
        "KEYS": ["branch"],
        "CHILD_KEYS": {
            "BRANCH_CREATION": ["create", "new"],
            "BRANCH_RENAME": ["rename"]
        }
    },
    "STASH": {
        "KEYS": ["stash"],
        "CHILD_KEYS": {
            "ADD_STASH": ["add", "in"],
            "REMOVE_STASH": ["remove"],
            "POP_STASH": ["pop", "out"],
        }
    },
    "PATCH": {
        "KEYS": ["patch", "exam"]
    },
    "RESET": {
        "KEYS": ["reset", "restart"],
        "CHILD_KEYS": {
            "RESET_ALL": ["all"]
        }
    },
    "LOG": {
        "KEYS": ["log", "history"],
    },
}
