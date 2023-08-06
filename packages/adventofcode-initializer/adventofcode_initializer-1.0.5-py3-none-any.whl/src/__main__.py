import argparse
import datetime
import json
import os
import re
import requests
import sys

from bs4 import BeautifulSoup
from markdownify import markdownify as md


CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), '.config', 'advent-initializer')
CONFIG_FILENAME = 'session.cfg'


def parse_args(current_year: int) -> (argparse.ArgumentParser, argparse.ArgumentParser):
    parser = argparse.ArgumentParser(
        description='Download Advent of Code problems as markdown files and also its inputs',
        add_help=True,
        epilog='In order to download inputs or part 2, you have to set the \'session\' cookie.'
    )

    subparsers = parser.add_subparsers()

    download = subparsers.add_parser(
        'download',
        help='Download files',
        add_help=True
    )

    download.add_argument(
        '-a', '--all-days',
        help='Download all problems from a given year',
        action='store_true', required=False
    )

    download.add_argument(
        '-d', '--day',
        help='The problem that is going to be downloaded',
        action='store', type=int, choices=range(1, 26), metavar='[1-25]', required=False
    )

    download.add_argument(
        '-y', '--year',
        help='Advent of Code edition',
        action='store', type=int, default=current_year
    )

    download.add_argument(
        '--both-parts',
        help='Download both parts of the problem and its input (if it is possible)',
        action='store_true', required=False
    )

    download.add_argument(
        '--part-2',
        help='Download part two for the given problem and its input (if it is possible). It appends to part one\'s '
             'README if it exists',
        action='store_true', required=False
    )

    set_cookie = subparsers.add_parser(
        'set-session-cookie',
        help='Set the necessary cookie to download personal inputs or ploblems\' part 2',
        add_help=True,
        epilog='You only have to do save it once'
    )

    set_cookie.add_argument(
        'session_cookie',
        help='Cookie required to download inputs or problems\' part 2',
        action='store', type=str, metavar='session-cookie'
    )

    return parser.parse_args(), parser


def error_args(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


def get_dates(args: argparse.Namespace, current_year: int) -> tuple:
    if args.day is None and not args.all_days:
        error_args('\'--day\' and \'--all-days\' can not be simultaneously ignored')
    elif args.all_days:
        if args.day is not None:
            error_args('\'--day\' and \'--all-days\' can not be used simultaneously')
        days = list(range(1, 26))
    else:
        days = [args.day]

    year = args.year

    if year > current_year:
        error_args('\'year\' can not be posterior to the current year')

    return days, year


def get_session_cookie() -> dict:
    try:
        with open(os.path.join(CONFIG_FILE_PATH, CONFIG_FILENAME), mode='r') as config_file:
            cookies = json.load(config_file)
    except FileNotFoundError:
        print('Warning: \'session\' cookie not set', file=sys.stderr)
        cookies = {}
    except json.decoder.JSONDecodeError:
        print('Error: config file bad formatted', file=sys.stderr)
        sys.exit(2)

    return cookies


def set_session_option(cookie: str) -> None:
    cookies = {'session': cookie}
    os.makedirs(CONFIG_FILE_PATH, exist_ok=True)
    filepath = os.path.join(CONFIG_FILE_PATH, CONFIG_FILENAME)
    with open(filepath, mode='wt') as config_file:
        json.dump(cookies, config_file, indent=4)
    print(f'{filepath} successfully created')


def get_parts_to_download(both: bool, part_2: bool) -> list:
    if both:
        return [1, 2]
    elif part_2:
        return [2]
    return [1]


def replace_internal_links(markdown_text: str) -> str:
    def add_advent_url(match):
        return f'<a href=\"https://adventofcode.com{match.group(1)}\">{match.group(2)}</a>'

    return re.sub(pattern=r'<a href=\"(\/[^>]+)\">([^<>]+)</a>', repl=add_advent_url, string=markdown_text)


def remove_last_code_line(markdown_text: str) -> str:
    return re.sub(pattern=r'\n</code></pre>', repl='</code></pre>', string=markdown_text)


def fix_emphasize_code(markdown_text: str) -> str:
    def interchange(match):
        return f'<em><code>{match.group(1)}</code></em>'

    return re.sub(pattern=r'<code><em>(.*)</em></code>', repl=interchange, string=markdown_text)


def fix_html_format(markdown_text: str) -> str:
    fix_links = replace_internal_links(markdown_text)
    fix_code_section = remove_last_code_line(fix_links)
    return fix_emphasize_code(fix_code_section)


def download_input(day: int, url: str, cookies: dict) -> None:
    url_input = url + '/input'
    replay = requests.get(url_input, cookies=cookies)

    with open(os.path.join(os.getcwd(), f'Day{day}', 'input'), mode='wb') as file:
        file.write(replay.content)


def download_option(days: list, year: int, cookies: dict, parts: list) -> None:
    for day in days:
        url = f'https://adventofcode.com/{year}/day/{day}'
        replay = requests.get(url, cookies=cookies)
        if replay.status_code == 200:
            try:
                os.mkdir(f'Day{day}')
            except FileExistsError:
                if 1 in parts:
                    print(f'Folder \'Day{day}\' already exists. Ignoring')
                    continue
            soup = BeautifulSoup(replay.content, features='html.parser')
            problems = soup.find_all('article', class_='day-desc')
            download_input(day, url, cookies)

            part2_available = True
            if 2 in parts and len(problems) == 1 and cookies:
                print('You have not completed part one yet', file=sys.stderr)
                part2_available = False

            for part in parts:
                if not part2_available and part == 2:
                    break

                md_content = md(fix_html_format(str(problems[part - 1])),
                                heading_style='ATX',
                                bullets='-+*',
                                strong_em_symbol='**')

                with open(os.path.join(os.getcwd(), f'Day{day}', 'README.md'), mode='at') as file:
                    file.write(md_content)

        else:
            print(f'Day {" " if day < 10 else ""}{day}: not found', file=sys.stderr)


def main():
    current_year = datetime.date.today().year
    args, parser = parse_args(current_year)

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    if 'session_cookie' in args:
        set_session_option(args.session_cookie)
    else:
        days, year = get_dates(args, current_year)
        parts = get_parts_to_download(args.both_parts, args.part_2)
        cookies = get_session_cookie()
        if 2 in parts and not cookies:
            print('Error: can not download part two, cookie not set\nExiting')
            sys.exit(1)
        download_option(days, year, cookies, parts)


if __name__ == '__main__':
    main()
