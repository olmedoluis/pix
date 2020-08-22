def patchSelect(errorMessage="", files=[], colors={}, icons={}):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    from .Theme import INPUT_THEME, INPUT_ICONS
    from os import popen

    terminalHeight, terminalWidth = popen("stty size", "r").read().split()
    terminalWidth = int(terminalWidth) - 1
    selectionAreaHeight = int(terminalHeight) - 1

    KEYWORDS = {"+": "modification", "-": "deletation"}
    COLORS = {**INPUT_THEME, **colors}
    ICONS = {**INPUT_ICONS, **icons}
    RESET = COLORS["reset"]

    getch = getGetch()
    inputConsole = ConsoleControl(selectionAreaHeight)
    patchControl = PatchControl(
        offset=0,
        termSizeX=terminalWidth,
        termSizeY=selectionAreaHeight,
        files=files,
        colors=COLORS,
        icons=ICONS,
    )

    patchControl.setPatchesOfFile(1)
    patchControl.setPatchShowing(0)

    def updateConsole():
        state = (
            COLORS["borderSel"]
            if patchControl.getIsPatchSelected()
            else COLORS["border"]
        )

        inputConsole.setConsoleLine(1, 2, patchControl.getFileIndexShown())
        inputConsole.setConsoleLine(3, 1, patchControl.getCurrentFileName())

        for lineNumber in range(5, selectionAreaHeight):
            textToShow = patchControl.getStyledPatchLine(lineNumber)
            color = COLORS["slight"]

            if textToShow != "":
                firstChar = textToShow[0]
                icon = ICONS[firstChar] if firstChar in ICONS else firstChar
                color = COLORS[KEYWORDS[firstChar]] if firstChar in KEYWORDS else color

                textToShow = color + icon + textToShow[1:] + COLORS["reset"]

            inputConsole.setConsoleLine(
                lineNumber, 1, f"{state}❚{RESET}   {textToShow}"
            )

        inputConsole.refresh()

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char, True)

        if state == "DOWN":
            patchControl.increaseOffset()
        elif state == "UP":
            patchControl.decreaseOffset()
        elif state == "RIGHT":
            patchControl.changePage(1)
        elif state == "LEFT":
            patchControl.changePage(-1)
        elif state == "EXTENDED_RIGHT":
            patchControl.addIndexSelectedToPatch()
        elif state == "EXTENDED_LEFT":
            patchControl.removeIndexSelectedToPatch()
        elif state == "YES":
            patchControl.addIndexSelectedToPatch()
            patchControl.changePage(1)
        elif state == "NO":
            patchControl.removeIndexSelectedToPatch()
            patchControl.changePage(1)
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            inputConsole.deleteLastLines(selectionAreaHeight + 4)
            inputConsole.finish()
            print(errorMessage)
            exit()

    inputConsole.deleteLastLines(selectionAreaHeight + 4)
    inputConsole.finish()

    return patchControl.files


class PatchControl:
    def __init__(self, offset, termSizeX, termSizeY, files, colors, icons):
        self._COLORS = colors
        self._RESET = colors["reset"]
        self._ICONS = icons
        self._patches = []
        self._offset = offset
        self._termSizeX = termSizeX
        self._termSizeY = termSizeY
        self._patchIndexSelected = 0
        self._patchShowing = []
        self._textZoneArea = range(0)
        self._fileNameIndex = 0
        self.files = files

    def setPatchesOfFile(self, times):
        self._patches = self.files[self._fileNameIndex].patches
        self._patchIndexSelected = 0 if times > 0 else len(self._patches) - 1

    def setPatchShowing(self, index):
        self._patchShowing = self._patches[index][1:]
        self._textZoneArea = range(0, len(self._patchShowing))

    def decreaseOffset(self):
        newOffset = self._offset - 1
        self._offset = newOffset if newOffset in self._textZoneArea else self._offset

    def increaseOffset(self):
        newOffset = self._offset + 1
        self._offset = (
            newOffset
            if newOffset in self._textZoneArea
            and (len(self._patchShowing) > self._termSizeY)
            and (newOffset < (len(self._patchShowing) * 0.5))
            else self._offset
        )

    def changePage(self, times):
        newIndex = self._patchIndexSelected + times
        self._patchIndexSelected = newIndex % len(self._patches)

        if not (newIndex in range(len(self._patches))) and len(self.files) > 1:
            self._fileNameIndex = (self._fileNameIndex + times) % len(self.files)
            self.setPatchesOfFile(times)

        self.setPatchShowing(self._patchIndexSelected)
        self._offset = 0

    def addIndexSelectedToPatch(self):
        if not self.getIsPatchSelected():
            self.files[self._fileNameIndex].patchesSelected.append(
                self._patchIndexSelected
            )

    def removeIndexSelectedToPatch(self):
        if self.getIsPatchSelected():
            self.files[self._fileNameIndex].patchesSelected.remove(
                self._patchIndexSelected
            )

    def getStyledPatchLine(self, lineNumber):
        index = lineNumber + self._offset - 5
        if not (index in self._textZoneArea):
            return ""

        lineText = self._patchShowing[index]
        return lineText[0 : self._termSizeX - 5]

    def getIsPatchSelected(self):
        return (
            self._patchIndexSelected in self.files[self._fileNameIndex].patchesSelected
        )

    def getCurrentFileName(self):
        return self.files[self._fileNameIndex].fileName

    def getPatchIndexShown(self):
        output = ""

        for index in range(0, len(self._patches)):
            active = (
                self._COLORS["selection"] if index == self._patchIndexSelected else ""
            )
            color = self._COLORS["index"]
            icon = self._ICONS["normal"]

            if index in self.files[self._fileNameIndex].patchesSelected:
                color = self._COLORS["indexSel"]
                icon = self._ICONS["selection"]

            output = f"{output}{color}{active} {icon}{self._RESET}"

        return f"{output} "

    def getFileIndexShown(self):
        output = ""

        for index in range(0, len(self.files)):
            color = self._COLORS["file"]
            extra = ""

            if index == self._fileNameIndex:
                color = self._COLORS["fileAct"]
                extra = self.getPatchIndexShown()

            output = f"{output}{color}|{self._RESET}{extra}"

        return output
