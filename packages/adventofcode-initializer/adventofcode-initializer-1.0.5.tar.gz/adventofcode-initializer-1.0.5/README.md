# Advent of Code Initializer

This utility allows downloading [Advent of Code](https://adventofcode.com) problems as markdown files. It also
downloads the problems' inputs. This tool creates a folder for the required problem and stores the markdown
and the input files.

## Usage

The utility has two main options (`set-session-cookie` and `download`). 

```
usage: adventofcode_initializer [-h] {download,set-session-cookie} ...

Download Advent of Code problems as markdown files and also its inputs

positional arguments:
  {download,set-session-cookie}
    download            Download files
    set-session-cookie  Set the necessary cookie to download personal inputs
                        or ploblems' part 2

options:
  -h, --help            show this help message and exit

In order to download inputs or part 2, you have to set the 'session' cookie.
```

Setting the correspondig cookie the user will be able to download custom inputs and new problem parts.

```
usage: adventofcode_initializer set-session-cookie [-h] session-cookie

positional arguments:
  session-cookie  Cookie required to download inputs or problems' part 2

options:
  -h, --help      show this help message and exit

You only have to do save it once
```

By default, the utility downloads the first part of the problem. In addition, part two can be appended to the README file.

The utility can also download previous editions or already completed days.

```
usage: adventofcode_initializer download [-h] [-a] [-d [1-25]] [-y YEAR]
                                            [--both-parts] [--part-2]

options:
  -h, --help            show this help message and exit
  -a, --all-days        Download all problems from a given year
  -d [1-25], --day [1-25]
                        The problem that is going to be downloaded
  -y YEAR, --year YEAR  Advent of Code edition
  --both-parts          Download both parts of the problem and its input (if
                        it is possible)
  --part-2              Download part two for the given problem and its input
                        (if it is possible). It appends to part one's README
                        if it exists
```

## Installation

Pip:

```zsh
pip install adventofcode-initializer
```

Build from source:
```zsh
git clone https://github.com/Serms1999/advent-initializer.git
cd advent-initializer
pip install .
```