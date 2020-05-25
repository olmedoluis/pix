def console(height):
    import sys
    import os

    if os.name == 'nt':
        import msvcrt
        import ctypes

        class _CursorInfo(ctypes.Structure):
            _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

    def hide_cursor():
        if os.name == 'nt':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(
                handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(
                handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    def show_cursor():
        if os.name == 'nt':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(
                handle, ctypes.byref(ci))
            ci.visible = True
            ctypes.windll.kernel32.SetConsoleCursorInfo(
                handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

    code = "\x1b["
    log = sys.stdout.write

    def cursorUp(times):
        log(f"{code}{times}A")

    def cursorDown(times):
        log(f"{code}{times}B")

    def cleanLine():
        log(f"{code}2K")

    class term():
        def __init__(self, lines):
            self.display = (" " * (lines - 1)).split(" ")

            for emptyValue in self.display:
                print(emptyValue)

        def getCode(self, string):
            return f"\x1b[{string}"

        def show(self, data):
            self.display = data

        def setConsoleLine(self, row=0, column=0, content=""):
            self.display[row] = " " * column + content

        def refresh(self):
            count = len(self.display)
            cursorUp(count)
            for line in self.display:
                cleanLine()
                print(line.replace("$C", "❚"))

        def deleteLastLines(self, lines):
            lastNumberOfLines = len(self.display)
            newNumberOfLines = lastNumberOfLines - lines
            self.display = (" " * (newNumberOfLines)).split(" ")
            for i in range(0, lines):
                cleanLine()
                cursorUp(1)

        def finish(self):
            show_cursor()

    hide_cursor()
    return term(height)


def prompts():
    import getch

    def merge(word, char):
        if char == "\n":
            return word, "FINISH"
        elif ord(char) == 27:
            return word, "BREAK_CHAR"
        elif char == "\x7f":
            return word[:-1], "BACKSPACE"
        elif len(char) == 1:
            return word + char, "VALID_CHAR"
        else:
            return word, "UNKNOWN"

    def getMovement(char):
        charLower = char.lower()

        if charLower == "a":
            return "LEFT"
        elif charLower == "d":
            return "RIGHT"
        elif charLower == "w":
            return "UP"
        elif charLower == "s":
            return "DOWN"
        elif char == "\n":
            return "FINISH"
        elif ord(char) == 27:
            return "BREAK_CHAR"
        else:
            return "UNKNOWN"

    def getResponse(char):
        charLower = char.lower()

        if charLower == "y":
            return "YES"
        elif charLower == "n":
            return "NO"
        elif char == "\n":
            return "FINISH"
        elif ord(char) == 27:
            return "BREAK_CHAR"
        else:
            return "UNKNOWN"

    def getOptionsWithStates(options):
        class opt():
            def __init__(self, content):
                self.state = False
                self.content = content

            def getStateString(self):
                return "❤" if self.state else "⚬"

            def setState(self, newState):
                self.state = newState

        output = []
        for option in options:
            output.append(opt(option))

        return output

    def getOptionsSelected(options):
        output = []
        for option in options:
            if option.state:
                output.append(option)
        return output

    def getOptionContents(options):
        output = []
        for option in options:
            if option.state:
                output.append(option.content)
        return output

    def textInput(title="", content="", placeHolder="", finalTitle="", errorMessage=""):
        inputConsole = console(1)
        finalTitle = finalTitle if finalTitle != "" else title
        word = content

        while True:
            wordToShow = word if word != "" else placeHolder
            inputConsole.setConsoleLine(0, 1, f"{title} {wordToShow}")
            inputConsole.refresh()

            char = getch.getch()
            newWord, state = merge(word, char)
            word = newWord

            if state == "FINISH":
                break
            if state == "BREAK_CHAR":
                print(errorMessage)
                exit()

        inputConsole.setConsoleLine(0, 1, f"{finalTitle} {wordToShow}")
        inputConsole.refresh()

        inputConsole.finish()

        return word if word != "" else placeHolder

    def selectInput(title="", finalTitle="", options=[""], errorMessage=""):
        inputConsole = console(5)
        finalTitle = finalTitle if finalTitle != "" else title
        index = 0
        optionsLen = len(options)

        inputConsole.setConsoleLine(0, 1, title)

        while True:
            inputConsole.setConsoleLine(
                2, 4, options[(index - 1) % optionsLen])
            inputConsole.setConsoleLine(3, 4, options[index % optionsLen])
            inputConsole.setConsoleLine(
                4, 4, options[(index + 1) % optionsLen])
            inputConsole.refresh()

            char = getch.getch()
            state = getMovement(char)

            if state == "DOWN":
                index = index + 1
            elif state == "UP":
                index = index - 1
            elif state == "FINISH":
                break
            elif state == "BREAK_CHAR":
                print(errorMessage)
                exit()

        selectedOption = options[index % optionsLen]
        inputConsole.setConsoleLine(0, 1, f"{finalTitle} {selectedOption}")
        inputConsole.refresh()
        inputConsole.deleteLastLines(4)

        inputConsole.finish()

        return selectedOption

    def confirmInput(title="", content="", finalTitle="", errorMessage=""):
        inputConsole = console(1)
        finalTitle = finalTitle if finalTitle != "" else title
        word = content

        while True:
            inputConsole.setConsoleLine(0, 1, f"{title} {word}")
            inputConsole.refresh()

            char = getch.getch()
            state = getResponse(char)

            if state == "YES":
                word = "yes"
                break
            if state == "NO":
                word = "no"
                break
            if state == "FINISH":
                break
            if state == "BREAK_CHAR":
                print(errorMessage)
                exit()

        inputConsole.setConsoleLine(0, 1, f"{finalTitle} {word}")
        inputConsole.refresh()

        inputConsole.finish()

        return word

    def multiSelectInput(title="", finalTitle="", options=[""], errorMessage=""):
        inputConsole = console(5)
        finalTitle = finalTitle if finalTitle != "" else title
        index = 0
        optionsLen = len(options)
        optionsWithStates = getOptionsWithStates(options)

        inputConsole.setConsoleLine(0, 1, title)

        while True:
            optionAbove = optionsWithStates[(index - 1) % optionsLen]
            optionSelected = optionsWithStates[index % optionsLen]
            optionDown = optionsWithStates[(index + 1) % optionsLen]

            color = "\x1b[32m" if optionAbove.state else "\x1b[2m"
            inputConsole.setConsoleLine(
                2, 4, f"{color}{optionAbove.getStateString()} {optionAbove.content}\x1b[0m")

            color = "\x1b[32m\x1b[1m" if optionSelected.state else "\x1b[1m"
            inputConsole.setConsoleLine(
                3, 4, f"{color}{optionSelected.getStateString()} {optionSelected.content}\x1b[0m")

            color = "\x1b[32m" if optionDown.state else "\x1b[2m"
            inputConsole.setConsoleLine(
                4, 4, f"{color}{optionDown.getStateString()} {optionDown.content}\x1b[0m")

            inputConsole.refresh()

            char = getch.getch()
            state = getMovement(char)

            if state == "DOWN":
                index = index + 1
            elif state == "UP":
                index = index - 1
            elif state == "RIGHT":
                optionSelected.setState(True)
            elif state == "LEFT":
                optionSelected.setState(False)
            elif state == "FINISH":
                break
            elif state == "BREAK_CHAR":
                print(errorMessage)
                exit()

        selectedOptionsWithStates = getOptionsSelected(optionsWithStates)
        selectedOptions = getOptionContents(selectedOptionsWithStates)
        selectedOptionsString = ", ".join(selectedOptions)

        inputConsole.setConsoleLine(
            0, 1, f"{finalTitle} {selectedOptionsString}")
        inputConsole.refresh()
        inputConsole.deleteLastLines(4)

        inputConsole.finish()

        return selectedOptions

    class prompts_ui():
        def text(self, **arg):
            return textInput(**arg)

        def select(self, **arg):
            return selectInput(**arg)

        def confirm(self, **arg):
            return confirmInput(**arg)

        def multiSelect(self, **arg):
            return multiSelectInput(**arg)

    return prompts_ui()