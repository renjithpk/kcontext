#!/usr/bin/env python3

import argparse
import curses
import signal
from utils.kube_context_manager import KContextManager
from utils.tags_manager import ContextTags

def initialize_colors():
    curses.start_color()
    for i in range(1, 11):
        curses.init_pair(i, i, curses.COLOR_BLACK)

def exit_gracefully(*args):
    curses.endwin()
    exit(0)

def display_contexts(stdscr, context_manager):
    curses.curs_set(0)
    initialize_colors()
    current_row = 0
    signal.signal(signal.SIGINT, exit_gracefully)

    tags_mgr = ContextTags(context_manager)
    fixed_len = tags_mgr.get_max_tag_len() + 1
    contexts_sorted = tags_mgr.sorted_contexts()

    while True:
        stdscr.clear()
        stdscr.refresh()

        for row, context in enumerate(contexts_sorted):
            column = 0
            for tag in tags_mgr.get_tags(context):
                formatted_tag, color = tags_mgr.get_tag_details(tag)
                if row == current_row:
                    stdscr.addstr(row, column, formatted_tag, curses.color_pair(color) | curses.A_BOLD)
                else:
                    stdscr.addstr(row, column, formatted_tag, curses.color_pair(color))
                column = column + len(formatted_tag)

            padding = fixed_len - column + 1
            stdscr.addstr(row, column, " " * padding, curses.color_pair(0))
            column = column + padding

            if row == current_row:
                stdscr.addstr(row, column, context, curses.color_pair(0) | curses.A_BOLD | curses.A_REVERSE)
            else:
                stdscr.addstr(row, column, context, curses.color_pair(0))

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_row = max(0, current_row - 1)
        elif key == curses.KEY_DOWN:
            current_row = min(len(contexts_sorted) - 1, current_row + 1)
        elif key == 10:  # Enter key
            selected_context = contexts_sorted[current_row]
            error_message = context_manager.set(selected_context)
            if error_message:
                stdscr.addstr(len(contexts_sorted) + 1, 0, f"Error: {error_message}")
                stdscr.refresh()
                stdscr.getch()  # Wait for a key press
            else:
                exit_gracefully(0)
def main():
    description = '''kcontext is a versatile tool for selecting Kubernetes contexts with ease.
    It simplifies context selection by using tags based on context names, making it quick to identify and choose the context you want.
      When a key from a map is found in the context, its corresponding value is shown as a tag before each context name.
    These tags are color-coded for distinction and displayed in the order they are defined. The list of contexts is sorted based on these tags, not their names.
    You can customize the tagging by setting the K_CONTEXT_TAGS_JSON environment variable with your preferred key-value pairs in JSON format.
    example:\n
    export K_CONTEXT_TAGS_JSON='{\n
        "production": "[prod]",\n
        "development": "[dev]",\n
        "west": "[west]",\n
        "central": "[cent]",\n
    }'\n\n
    If K_CONTEXT_TAGS_JSON is not set, kcontext uses a default tag map, including tags like [prod] for production, [dev] for development, and others for different context types.
    '''

    argparse.ArgumentParser(
        prog="kcontext",
        usage="Just run the command without any argument to view and select the kubernetes context",
        description=description).parse_args()
    context_manager = KContextManager()
    curses.wrapper(display_contexts, context_manager)
if __name__ == '__main__':
    main()

