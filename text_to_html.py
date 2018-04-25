#!/usr/bin/env python3
# wykys

import argparse
import codecs
import re
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A program for analyzing a text file and generating an HTML file with questions.'
    )
    parser.add_argument(
        '-f',
        '--file',
        dest='path',
        action='store',
        default='test1.txt',
        help='destination text with test',
    )

    with open('templates/top.html', 'r') as fr:
        html_top = fr.read()

    with open('templates/bot.html', 'r') as fr:
        html_bot = fr.read()

    try:
        with open(parser.parse_args().path, 'r') as fr:
            test = fr.readlines()
    except UnicodeDecodeError:
        try:
            with codecs.open(parser.parse_args().path, 'r', 'utf-16') as fr:
                test = fr.readlines()
        except UnicodeDecodeError:
            print('UnicodeDecodeError', file=sys.stderr)

    html = html_top
    start = False
    cnt = 0
    quest_cnt = 0

    for line in test:
        line = line.strip()
        if len(line) > 0 and line[0] == '1':
            start = True
            cnt = 0

        if len(line) == 0:
            continue

        if start:
            cnt += 1
            if cnt % 2 == 1:
                line = re.sub(r'[ .]{2,}', ' ... ', re.sub(r'^\d+.?\s*', '', line))
                if '...' not in line:
                    line += ' ... '
                if not line.endswith('.'):
                    line = line.strip() + ' .'
                question = line
            else:
                choice = re.sub('[A-D]. ', '\n', line).strip().split('\n')
                quest = 4 * '    ' + 'quest(\"' + question + '\",\n    ' + 4 * '    '
                for s in choice:
                    quest += '[\"' + s.strip() + '\", \"\"],'
                quest = quest[:-1] + '\n' + 4 * '    ' + ');\n'
                quest_cnt += 1
                html += '\n' + 4 * '    ' + '// QUEST {:3d}\n'.format(quest_cnt)
                html += quest

    html += html_bot

    with open(parser.parse_args().path.split('.')[0] + '.html', 'w') as fw:
        fw.write(html)
