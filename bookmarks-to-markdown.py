#!/usr/bin/env python3

import json
import sys

def usage():
    print("usage: {0} file".format(sys.argv[0]))

def load_bookmark():
    with open(sys.argv[1]) as f:
        bookmark = json.load(f)

    return bookmark

def filter_draft(bookmark):
    draft_condition = lambda e: e['name'] == 'draft'
    draft_position = lambda b: b['roots']['bookmark_bar']['children']
    draft = list(filter(draft_condition,draft_position(bookmark)))[0]

    return draft['children']

def generate_markdown(draft):
    markdown_str = "- [{name}]({url})"
    markdown_gen = lambda l: markdown_str.format(**l)
    markdown = [ markdown_gen(l) for l in draft ]

    return '\n'.join(markdown)

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    bookmark = load_bookmark()
    draft = filter_draft(bookmark)
    markdown = generate_markdown(draft)
    print(markdown)

if __name__ == '__main__':
    main()