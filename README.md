A simple command line tool to record, resolve and tally your own private predictions. Tested only on Linux, programmed in Python3.

Inspired by https://github.com/NunoSempere/PredictResolveTally !

Simply clone the package, and install with `pip install .`. 

It creates three scripts: `predict, resolve, tally`.

Usage instructions/help message ``predict -h``:

```
Usage: 
  predict : record a new prediction by answering the prompts.
  resolve : Resolve any due predictions.
  tally   : Show your calibration.
Notes:
  Ctrl+C to quit any CLI tool. Already resolved predictions are kept.
  Add "-h" flag: show this help message.
  You can also directly edit the database file: <homedir>/.predict_resolve_tally/database.csv
  Dates can be specified in many formats, e.g. "2022-06-30" or "next year" or "in five hours"
  Resolved values can be specified as "true/yes/y" or "false/no/n" or "skip/empty-string"
```
