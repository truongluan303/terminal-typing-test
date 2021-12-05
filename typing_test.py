try:
    # check if curses is installed or not
    import curses
    from curses import wrapper
except:
    # if not yet install, the automatically install the module
    from install_lib.install_lib import install_required_libraries
    install_required_libraries()
    import curses
    from curses import wrapper

from typing import Tuple, List
import time
import random




# the code for curses color pairs
ERROR_CODE = 1
CORRECT_CODE = 2
HIGHLIGHT_CODE = 3
PROMPT_CODE = 4





def main(stdscr) -> None:
    ''' 
    main function
    '''
    init_color(stdscr)
    
    file_reader = FileReader()
    file_reader.read_file(".input.txt")

    stdscr.clear()
    curses.noecho()

    num_of_sentences = prompt_input(stdscr)
    sentences = file_reader.get_random_sentences(num_of_sentences)


    ''' start the typing test '''

    start_time = time.time()
    total_words = 0
    words_typed = 0
    wrong_words = 0
    wpm = 0

    curses.noecho()


    for i in range(len(sentences)):
        user_sentence = ""
        sentence = sentences[i]
        total_words += len(sentence.split())

        centralize_text(stdscr, sentence)

        stdscr.clear()
        stdscr.refresh()

        while True:

            # calculate the current wpm
            time_passed = (time.time() - start_time) / 60
            if time_passed > 0:
                wpm = (len(user_sentence.split()) + words_typed - wrong_words) // time_passed

            # show the remaining sentences and the current wpm
            stdscr.move(0, 0)
            stdscr.addstr(f"Remaining Sentences: ")
            stdscr.addstr(f"{len(sentences) - i - 1}\n", curses.color_pair(HIGHLIGHT_CODE))
            stdscr.addstr(f"Words per Minute: ")
            stdscr.addstr(f"{wpm:.0f}\n", curses.color_pair(HIGHLIGHT_CODE))
            
            # print the target sentence
            x, y = centralize_text(stdscr, sentence)

            # print the user sentence on top of the target sentence
            stdscr.move(x, y)
            for j in range(len(user_sentence)):

                color = curses.color_pair(CORRECT_CODE)
                if j >= len(sentence) or user_sentence[j] != sentence[j]:
                    color = curses.color_pair(ERROR_CODE)

                stdscr.addstr(user_sentence[j], color)

            # get the user key entered
            key = stdscr.getch()

            if key == 10:                           # if enter/newline
                break
            elif key == 27:                         # if escape
                exit(0)
            elif key == 8:                          # if backspace
                user_sentence = user_sentence[:-1]
            elif 32 <= key <= 126:                  # if text
                user_sentence += chr(key)

        
        words_typed += len(user_sentence.split())

        user_sentence = user_sentence.split()
        target = sentence.split()

        # find the number of wrong words
        for j in range(len(user_sentence)):
            if j < len(target) and user_sentence[j] != target[j]:
                wrong_words += 1
            elif j >= len(target):
                wrong_words += 1
                

    ''' end the typing test and calculate and output the result '''

    duration = time.time() - start_time
    accuracy = (total_words - wrong_words) / total_words
    wpm = total_words // (duration / 60)
    wpm *= accuracy

    stdscr.clear()
    stdscr.addstr("RESULT:\n\n", curses.color_pair(HIGHLIGHT_CODE))
    stdscr.addstr(f"Total Words:\t")
    stdscr.addstr(f"{total_words:.0f}\n", curses.color_pair(HIGHLIGHT_CODE))
    stdscr.addstr(f"Total Errors:\t")
    stdscr.addstr(f"{wrong_words:.0f}\n", curses.color_pair(HIGHLIGHT_CODE))
    stdscr.addstr(f"Accuracy:\t")
    stdscr.addstr(f"{accuracy*100:.2f}%\n", curses.color_pair(HIGHLIGHT_CODE))
    stdscr.addstr(f"Final WPM:\t")
    stdscr.addstr(f"{wpm:.0f}\n\n", curses.color_pair(HIGHLIGHT_CODE))
    
    # prompt the user if they want to replay
    prompt_replay(stdscr)






def centralize_text(stdscr, text:str, color:int=0) -> Tuple[int,int]:
    '''
    put a line of text in the middle of the curse
    args:
        stdscr: the standard screen
        text:   the text to be displayed
    return:
        the coordinate of the text on the curse
    '''
    scrh, scrw = stdscr.getmaxyx()

    x = scrh // 2
    y = (scrw // 2 - len(text) // 2) if (len(text) < scrw) else 0

    stdscr.addstr(x, y, text, color)
    return (x, y)






def prompt_input(stdscr) -> int:
    '''
    prompt the user for the number of sentences to be typed
    args:
        stdscr: the standard screen
    return:
        number of sentences to type
    '''
    MIN = 1
    MAX = 50

    usr_input = ""
    while True:
        stdscr.addstr(0, 0, f"Please enter the number of sentences to type ({MIN}-{MAX}):\n",
                      curses.color_pair(PROMPT_CODE))
        stdscr.move(1, len(usr_input))
        c = stdscr.getch()

        if c == 10:                         # if enter/newline
            break
        elif c == 27:                       # if escape
            exit(0)
        elif c == 8:                        # if backspace
            usr_input = usr_input[:-1]
        elif 48 <= c <= 57:                 # if number
            usr_input += chr(c)
            # input must not exceed 50
            if int(usr_input) > 50:
                usr_input = usr_input[:-1]

        stdscr.clear()
        stdscr.addstr(1, 0, usr_input)

    return int(usr_input)






def prompt_replay(stdscr) -> None:
    '''
    prompt if user wants to replay, if not then quit immediately
    '''
    stdscr.addstr(f"Do you want to replay? (Y/N) ", curses.color_pair(PROMPT_CODE))
    while True:
        response = stdscr.getkey()
        if response == "Y" or response == "y":
            return
        elif response == "N" or response == "n":
            exit(0)
    





def init_color(stdscr) -> None:
    '''
    initialize the color pairs that will be used throughout the application
    '''
    stdscr.clear()
    if not curses.has_colors():
        stdscr.addstr("Warning!!! Your terminal does not support color!\n")
        stdscr.addstr("Press any key to continue...")
        stdscr.getch()
        return
    curses.start_color()
    curses.init_pair(ERROR_CODE, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(CORRECT_CODE, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(HIGHLIGHT_CODE, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(PROMPT_CODE, curses.COLOR_BLUE, curses.COLOR_BLACK)







class FileReader():
    '''
    responsible for reading data from a text file
    '''

    def __init__(self) -> None:
        self._sentences = list()
    

    def read_file(self, filename:str) -> None:
        '''
        create a list of sentence from all the lines in a textfile
        '''
        with open(filename) as file:
            lines = file.readlines()
            self._sentences = [line.strip() for line in lines]


    def get_random_sentences(self, amount) -> List[str]:
        '''
        return a list of random sentences picked from all the sentences created
        '''
        result = list()
        added = set()
        for i in range(amount):
            rand_idx = random.randint(0, len(self._sentences) - 1)
            while rand_idx in added:
                rand_idx = random.randint(0, len(self._sentences) - 1)
            result.append(self._sentences[rand_idx])
            added.add(rand_idx)
        return result






if __name__ == "__main__":
    wrapper(main)




''' end of typing_test.py '''