import dateparser

import textwrap
import sys
import datetime
import dataclasses
import os
import pathlib
from .database import DATETIME_FORMAT, Record, store_records, load_records

DEBUG = True

def predict():
  """main routine for 'predict' command line script"""

  if len(sys.argv)==2 and sys.argv[1] == "-h":
    help()
  
  try:
    statement: str = input("> Statement: ")
    probability: float = parse_prob(input("> Probability (%): "))
    resolution_date: datetime.datetime = parse_date(input("> Resolution Date: "))
    submission_date = datetime.datetime.now()
  except KeyboardInterrupt:
    exit(1) # silently quit

  record = Record(
    statement=statement, 
    probability=probability, 
    resolution_date=resolution_date, 
    submission_date=submission_date, 
    is_resolved=False, 
    resolved_value=False
  )   
  dbfile = get_database_filename()
  records = load_records(dbfile)
  records.append(record)
  store_records(dbfile, records)

def resolve():
  """main routine for 'resolve' command line script"""

  if len(sys.argv)==2 and sys.argv[1] == "-h":
    help()

  dbfile = get_database_filename()
  records = load_records(dbfile)
  now = datetime.datetime.now()
  pending = [rec for rec in records if not rec.is_resolved and rec.resolution_date < now]
  if len(pending) == 0:
    print("No pending predictions to be resolved.")
    return
  else:
    pending = sorted(pending, key=lambda rec: rec.resolution_date) # most overdue first

  while len(pending) > 0:
    record = pending.pop(0)
    
    print(f"{record.statement}")
    if DEBUG:
      print(f"({record.submission_date.strftime(DATETIME_FORMAT)})")

    try:
      value = input(f"> (True/false/skip) ")
    except KeyboardInterrupt:
      exit(1) # silently quit, current progress has been saved

    value = value.strip().lower() # normalize
    if value in ["true","t","yes","y"]:
      record.is_resolved = True
      record.resolution_value = True # also modified in records-variable
      store_records(dbfile, records) # store change
    elif value in ["false","f","no","n"]:
      record.is_resolved = True
      record.resolution_value = False # also modified in records-variable
      store_records(dbfile, records) # store change
    elif value in ["skip","s",""]:
      pass
    else:
      print("Unknown resolution value! Plase try: true/false/skip")
  
  # pending queue has been emptied, we are done

def tally():
  """main routine for 'tally' command line script"""

  if len(sys.argv)==2 and sys.argv[1] == "-h":
    help()

  dbfile = get_database_filename()
  records = load_records(dbfile)
  # count
  count_true = {b: 0 for b in range(10)}
  count_false = {b: 0 for b in range(10)}

  for rec in records:
    if not rec.is_resolved:
      continue
    p = rec.probability
    v = rec.resolved_value
    if p < 0.50: # fold down to 50%-100% interval
      p = 1-p
      v = not v

    for b in range(5, 10):
      if b*10 <= p and p < b*10+10:
        if v == True:
          count_true[b] += 1
        else:
          count_false[b] += 1
  
  for b in range(5,10):
    ct = count_true[b]
    cf = count_false[b]
    
    text = "%3d to %3d : %d Correct and %d Wrong" % (b*10,b*10+10,ct,cf)
    if ct+cf > 0:
      text += " (%3d %%)" % (round(100.0*ct/(ct+cf)))
    else:
      text += " ( -- %)"
    
    print(text)

def help():
  """print help statement for all three commands"""

  print(textwrap.dedent(f"""
    Usage: 
      predict : record a new prediction by answering the prompts.
      resolve : Resolve any due predictions.
      tally   : Show your calibration.
    Notes:
      Ctrl+C to quit any CLI tool. Already resolved predictions are kept.
      Add "-h" flag: show this help message.
      You can also directly edit the database file: {get_database_filename()}
      Dates can be specified in many formats, e.g. "2022-06-30" or "next year" or "in five hours"
      Resolved values can be specified as "true/yes/y" or "false/no/n" or "skip/empty-string"
  """))
  exit(0)


def get_database_filename():
  filename = os.path.expanduser("~/.predict_resolve_tally/database.csv")
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  pathlib.Path(filename).touch(exist_ok=True)
  return filename

def parse_prob(line: str):
  try:
    return float(line)
  except ValueError:
    print("Error: could not parse probability: "+line)
    exit(1)

def parse_date(line: str):
  if line == "":
    return datetime
  try:
    #return parser.parse(line)
    return dateparser.parse(line)
  except ValueError:
    print("Error: could not parse date: "+line)
    exit(1)

