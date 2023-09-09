#!/usr/bin/env python3

import curses
import signal
import json
import os
from utils.stub_kube_context_manager import KContextManager

# Specify the tags you want to include and their shortened format
included_tags = {
    "prod":    "[prod] ",
    "dev":     " [dev] " ,
    "test":    " [tst] ",
    "central": " [cen] ",
    "east":    "[east] ",
    "red":     " [red] ",
    "green":   "[green]"
}


class Tags:
    def __init__(self):
        self.included_tags = self.load_config()
    def load_tags_from_env(self):
        # Access the environment variable for configuration
        tag_json = os.environ.get('K_CONTEXT_TAGS_JSON')

        # Parse the JSON string to obtain the configuration as a dictionary
        if tag_json:
            try:
                config = json.loads(tag_json)
                included_tags = config.get('included_tags', {})
                return included_tags
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON tag information \n    K_CONTEXT_TAGS_JSON={tag_json}")
                print(f"{e}")
        # Use default or empty configuration if environment variable is not set or parsing fails
        return {}
    def parse_context_name(context):
        # Create a list of formatted tags based on included tags present in the context
        formatted_tags = [included_tags[tag] for tag in included_tags if tag in context]
        return formatted_tags

# Default color pair (black text on white background)
default_color_pair = {"foreground": curses.COLOR_BLACK, "background": curses.COLOR_WHITE}


def parse_context_name(context):
    # Create a list of formatted tags based on included tags present in the context
    formatted_tags = [tag for tag in included_tags if tag in context]
    return formatted_tags

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()  # Enable color support
    # Initialize 10 color pairs with black background and different foreground colors
    for i in range(1, 11):  # Start from 1 to avoid the default color pair (0)
        curses.init_pair(i, i, curses.COLOR_BLACK)

    context_manager = KContextManager()
    kube_contexts = context_manager.get_kube_contexts()
    current_row = 0

    def exit_gracefully(*args):
        curses.endwin()
        exit(0)

    signal.signal(signal.SIGINT, exit_gracefully)

    tags = {}
    fixed_len = 0
    for context in kube_contexts:
        tags[context] = parse_context_name(context)
        # Calculate the total length of tags in the context, including brackets and spaces
        tag_len = sum(len(included_tags.get(tag, tag)) for tag in tags[context])
        if tag_len > fixed_len:
            fixed_len = tag_len
    tag_color = {}
    for index, key in enumerate(included_tags.keys()):
        tag_color[key] = index + 1

    # Sort the kube_contexts list based on the concatenated tags
    kube_contexts_sorted = sorted(kube_contexts, key=lambda x: "".join(tags[x]))
    while True:
        stdscr.clear()
        stdscr.refresh()
        for row, context in enumerate(kube_contexts_sorted):
            column = 0
            for tag in tags[context]:
                if row == current_row:
                    stdscr.addstr(row, column, included_tags[tag], curses.color_pair(tag_color[tag]) | curses.A_BOLD)  # Highlight the selected item
                else:
                    # Use the default color pair if the tag doesn't have a specified color
                    stdscr.addstr(row, column, included_tags[tag], curses.color_pair(tag_color[tag]))
                column = column + len(included_tags[tag])
            padding = fixed_len - column + 1
            stdscr.addstr(row, column, " "* padding, curses.color_pair(0))
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
            current_row = min(len(kube_contexts) - 1, current_row + 1)
        elif key == 10:  # Enter key
            selected_context = kube_contexts[current_row]
            error_message = context_manager.set_kube_context(selected_context)
            if error_message:
                stdscr.addstr(len(kube_contexts) + 1, 0, f"Error: {error_message}")
                stdscr.refresh()
                stdscr.getch()  # Wait for a key press
            else:
                exit_gracefully(0)

if __name__ == '__main__':
    curses.wrapper(main)
