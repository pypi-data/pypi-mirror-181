# transpo-dir

`transpo` is a tool to "transpose" directory structure.

Have you ever needed to create a directory structure that looks like a two-dimensional spreadsheet? For example, let's say you have product sales data stored in a directory where the first level is the product name and the second level is the month.
Now you want to convert this to a directory structure where the first level is the month and the second level is the product name. 
The tool `transpo` supports such a change of directory structure.

## Installation

By installing the package `transpo-dir` with pip, an executable `transpo` will be installed on your system.

```sh
pip install transpo-dir
```


If you get the error `ModuleNotFoundError: No module named 'docopt'` when running `transpo`, install the package docopt-ng or docopt.

```sh
pip install docopt-ng
```

## Usage

```
transpo [options] <src> -d DEST
```

### Options

```
-d DEST       Destination directory.
-i INDICES, --index-order=INDICES     The order of indices for transpose [default: 21].
```

### Walkthrough

```sh
$ cd test-data/test-depth-2

$ tree
.
├── a
│   ├── 1
│   │   └── a-1.txt
│   └── 2
│       └── a-2.txt
└── b
    ├── 1
    │   └── b-1.txt
    └── 2
        └── b-2.txt

6 directories, 4 files

$ transpo . -d hoge
#!/bin/bash
set -ex

mkdir hoge
mkdir -p hoge/1
mv ./a/1 hoge/1/a
mkdir -p hoge/2
mv ./a/2 hoge/2/a
mv ./b/1 hoge/1/b
mv ./b/2 hoge/2/b
rm -rf ./a
rm -rf ./b

$ transpo . -d hoge | bash -
+ mkdir hoge
+ mkdir -p hoge/1
+ mv ./a/1 hoge/1/a
+ mkdir -p hoge/2
+ mv ./a/2 hoge/2/a
+ mv ./b/1 hoge/1/b
+ mv ./b/2 hoge/2/b
+ rm -rf ./a
+ rm -rf ./b

$ tree
.
└── hoge
    ├── 1
    │   ├── a
    │   │   └── a-1.txt
    │   └── b
    │       └── b-1.txt
    └── 2
        ├── a
        │   └── a-2.txt
        └── b
            └── b-2.txt
```

