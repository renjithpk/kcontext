#!/usr/bin/env python3

import curses
import signal
from utils.stub_kube_context_manager import KContextManager
from utils.tags_manager import ContextTags


def main(stdscr, context_manager):
    curses.curs_set(0)
    curses.start_color()  # Enable color support
    # Initialize 10 color pairs with black background and different foreground colors
    for i in range(1, 11):  # Start from 1 to avoid the default color pair (0)
        curses.init_pair(i, i, curses.COLOR_BLACK)
    current_row = 0

    def exit_gracefully(*args):
        curses.endwin()
        exit(0)

    signal.signal(signal.SIGINT, exit_gracefully)

    fixed_len = 0
    tags_mgr = ContextTags(context_manager)
    fixed_len = tags_mgr.get_max_tag_len() + 1
    # Sort the kube_contexts list based on the concatenated tags
    contexts_sorted = tags_mgr.sorted_contexts()
    while True:
        stdscr.clear()
        stdscr.refresh()
        for row, context in enumerate(contexts_sorted):
            column = 0
            for tag in tags_mgr.get_tags(context):
                formatted_tag, color = tags_mgr.get_tag_details(tag)
                if row == current_row:
                    stdscr.addstr(row, column, formatted_tag, curses.color_pair(color) | curses.A_BOLD)  # Highlight the selected item
                else:
                    # Use the default color pair if the tag doesn't have a specified color
                    stdscr.addstr(row, column, formatted_tag, curses.color_pair(color))
                column = column + len(formatted_tag)
            padding = fixed_len - column + 1
            stdscr.addstr(row, column, " " * padding, curses.color_pair(0))
            column = column + padding
            if row == current_row:
                stdscr.addstr(row, column, context, curses.color_pair(0) | curses.A_BOLD | curses.A_REVERSE)  # Highlight the selected item
            else:
                # Use the default color pair if the tag doesn't have a specified color
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

if __name__ == '__main__':
    context_manager = KContextManager()
    curses.wrapper(main, context_manager)
