CHUNKS = (
	(60 * 60 * 24 * 365, 'y'),
	#(60 * 60 * 24 * 30, 'mon'),
	#(60 * 60 * 24 * 7, 'w'),
	(60 * 60 * 24, 'd'),
	(60 * 60, 'h'),
	(60, 'min'),
	(1, 's'),
)


def seconds_to_other(sec):
	"""
	Converts an integer number of seconds to a string of comma separted
	shorthand labels. Largest unit used is year; the smallest is second.

	Example output: "8h, 5min, 2s"
	"""
	chunks = []
	remainder = sec
	for chunk_secs, label in CHUNKS:
		num, remainder = divmod(remainder, chunk_secs)
		if num:
			chunks.append(u"{count}{label}".format(count=num, label=label))

	return ", ".join(chunks)