# boltdb-dump-to-json
Parser for the BoltDB output that chilts/boltdb-dump makes

## The need
I've used https://github.com/chilts/boltdb-dump in order to dump my BoltDB, it produces specific format which is not really feasable for work when it passes 2 decimal points, thus this parser is created in order to output JSON format from it. One can modify it for latter parsing in Py with dict type.

## Usage
I've went for `stdin` type of input, so if you are using [boltdb-dump](https://github.com/chilts/boltdb-dump) you could simply:
```
boltdb-dump my.db | python3 parse-boltdb-dump.py
```
It spits out JSON so you can later proces it with `jq`

## Version
Tested on `3.7.5` should work on `3.6+` due to f-strings