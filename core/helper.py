from datetime import *

def goal_to_numEntry(user):
	dict = {}
	entries = user.logentries.all()
	for entry in entries:
		goal_title = str(entry.log.goal.title)
		if goal_title in dict:
			dict[goal_title] += 1
		else:
			dict[goal_title] = 1
	return dict

def date_to_numEntry(user):
	dict = {}
	t = datetime.today()
	t = datetime(year=t.year, month=t.month, day=t.day)
	for i in range(14):
		dict[t] = 0
		t = t - timedelta(days=1)
	entries = user.logentries.all()
	for entry in entries:
		date = entry.entry_date
		date = datetime(year=date.year, month=date.month, day=date.day)
		if date in dict:
			dict[date] += 1
	a = dict.items()
	a.sort()
	return a

def get_streaks(user):
	dict = {}
	entries = user.logentries.all()
	for entry in entries:
		date = entry.entry_date
		date = datetime(year=date.year, month=date.month, day=date.day)
		dict[date] = True

	t = datetime.today()
	t = datetime(year=t.year, month=t.month, day=t.day)
	counter = 0
	while (True):
		if t in dict:
			counter+=1
			t = t - timedelta(days=1)
		else:
			return counter
			

