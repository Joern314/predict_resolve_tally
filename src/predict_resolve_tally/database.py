# load and store all recorded predictions
from datetime import datetime
from os import stat
import os.path
import csv
import datetime
import dataclasses
import readline # better input function


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

@dataclasses.dataclass
class Record:
  statement: str
  probability: float
  resolution_date: datetime.datetime

  # metadata
  submission_date: datetime.datetime

  # resolution
  is_resolved: bool = False
  resolved_value: bool = False

  def __repr__(self) -> str:
    if not self.is_resolved:
      return "Statement: %s\nProbability (%%): %f\nResolution Date: %s" % \
        (self.statement, self.probability, self.resolution_date.strftime("%Y-%m-%d %H:%M"))
    else:
      return "Statement: %s\nProbability (%%): %f\nResolution Date: %s\nResolved: %s" % \
        (self.statement, self.probability, self.resolution_date.strftime("%Y-%m-%d %H:%M"), str(self.resolved_value))

def parse_record(row: list[str]) -> Record:
  return Record(
    statement=row[0],
    probability=float(row[1]),
    resolution_date=datetime.datetime.strptime(row[2], DATETIME_FORMAT),
    submission_date=datetime.datetime.strptime(row[3], DATETIME_FORMAT),
    is_resolved=str2bool(row[4]),
    resolved_value=str2bool(row[5])
  )  

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def dump_record(rec: Record) -> list[str]:
  return [
    rec.statement,
    str(rec.probability),
    rec.resolution_date.strftime(DATETIME_FORMAT),
    rec.submission_date.strftime(DATETIME_FORMAT),
    str(rec.is_resolved),
    str(rec.resolved_value)
  ]

def load_records(filename: str) -> list[Record]:
  with open(filename, "r") as file:
    records = [parse_record(row) for row in csv.reader(file)]
  return records

def store_records(filename: str, records: list[Record]) -> None:
  rows = [dump_record(rec) for rec in records]
  with open(filename, "w") as file:
    csv.writer(file, quoting=csv.QUOTE_ALL).writerows(rows)
