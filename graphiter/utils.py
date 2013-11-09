import pytz
from django.conf import settings

from .attime import parseATTime


def get_times(from_time=None, until_time=None, timezone=None):
	tzinfo = pytz.timezone(settings.TIME_ZONE)
	if timezone:
		try:
			tzinfo = pytz.timezone(timezone)
		except pytz.UnknownTimeZoneError:
			pass

	if until_time:
		_until = parseATTime(until_time, tzinfo)
	else:
		_until = parseATTime('now', tzinfo)

	if from_time:
		_from = parseATTime(from_time, tzinfo)
	else:
		_from = parseATTime('-1d', tzinfo)

	_start = min(_from, _until)
	_end = max(_from, _until)
	assert _start != _end, "Invalid empty time range"

	return _start, _end
