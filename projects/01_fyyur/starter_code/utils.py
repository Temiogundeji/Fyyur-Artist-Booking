import datetime

def get_upcoming_shows(shows):
  return list(filter(lambda x: x.start_time > datetime.datetime.now(), shows))

def get_past_shows(shows):
  return list(filter(lambda x: x.start_time < datetime.datetime.now(), shows))