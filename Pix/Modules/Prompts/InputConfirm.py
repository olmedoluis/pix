def confirm(title="", final_title="", colors={}, error_message=""):
    from .Console import ConsoleControl, getGetch
    from .Tools import get_parsed_char
    from .Theme import INPUT_THEME

    FONT_COLOR = ({**INPUT_THEME, **colors})["font"]
    getch = getGetch()
    input_console = ConsoleControl(1)

    word = False

    while True:
        input_console.setConsoleLine(0, 1, f"{title}")
        input_console.refresh()

        char = getch()
        state = get_parsed_char(char)

        if state == "Y":
            word = True
            break
        elif state == "N":
            word = False
            break
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            input_console.finish()
            print(error_message)
            exit()

    final_title = final_title if final_title != "" else title

    input_console.setConsoleLine(0, 1, f"{final_title} {FONT_COLOR}{word}")
    input_console.refresh()
    input_console.finish()

    return word
