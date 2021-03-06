ALIASES = {
    "STATUS": {
        "ALIASES": ["w", "st"]
    },
    "ADD": {
        "ALIASES": ["a"], 
        "CHILD_ALIASES": {
            "ADD_ALL": ["."]
        }
    },
    "REMOVE": {
        "ALIASES": ["una", "rm"], 
        "CHILD_ALIASES": {
            "REMOVE_ALL": ["."]
        }
    },
    "COMMIT": {
        "ALIASES": ["s", "c"],
    },
    "BRANCH": {
        "ALIASES": ["br"],
        "CHILD_ALIASES": {
            "BRANCH_CREATION": ["cr"],
            "BRANCH_RENAME": ["rn"]
        }
    },
    "STASH": {
        "ALIASES": ["b"],
        "CHILD_ALIASES": {
            "ADD_STASH": ["a", "i"],
            "REMOVE_STASH": ["rm"],
            "POP_STASH": ["o"]
        }
    },
    "PATCH": {
        "ALIASES": ["e"]
    },
    "RESET": {
        "ALIASES": ["rs"],
        "CHILD_ALIASES": {
            "RESET_ALL": ["."]
        }
    },
    "LOG": {
        "ALIASES": ["l"],
    },
}
