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


##Notes for Developers

Afaik you should install with `pip install -E .` so that you can continously edit the source files. If you add new scripts to `pyproject.toml` then you need to run the install command again.

Feel free to cold-message me if you start using this (or any work based on it). I am interested in reading even tiny pull requests / forks :)

##Notes for Users

I wrote this as a half-day hobby project for myself, whilst making predictions for how much time I will actually need ;). I currently don't plan to invest more time into it, e.g. I don't want to read the XDG desktop standard to decide where to actually put the file, or figure out how to store settings for python programs, or what stuff would break when I switch to windows.
