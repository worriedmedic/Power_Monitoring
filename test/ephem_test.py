#/bin/python

import ephem

verbose = True
dst = True

cutty = ephem.Observer()
cutty.lat = '41.42'
cutty.long = '-70.92'
cutty.elevation = 20

if dst:
	dst_const = (ephem.hour * -4)
else:
	dst_const = (ephem.hour * -5)

planets = 	[ephem.Sun(),
		ephem.Moon(),
		ephem.Mars(),
		ephem.Jupiter(),
		ephem.Saturn(),
		ephem.Venus()]

for o in planets:
	o.compute(cutty)
	if str(o.alt).startswith('-'):
		d[o.name] = {'name'	: o.name,
			    'visible'	: False,
			    'altitude'	: o.alt,
			    'azimuth'	: o.az,
			    'rising'	: ephem.Date(cutty.next_rising(o) + dst_const),
			    'setting'	: ephem.Date(cutty.previous_setting(o) + dst_const)}
		if verbose:
			print('%s IS NOT VISIBLE' %d[o.name]['name'])
			print('%s: alt: %s azm: %s' %(d[o.name]['name'], d[o.name]['altitude'], d[o.name]['azimuth']))
			print('Next Rising: ', ephem.Date(cutty.next_rising(o) + dst_const))
			print('Previous Setting: ', ephem.Date(cutty.previous_setting(o) + dst_const))
	else:
		d[o.name] = {'name'	: o.name,
			    'visible'	: True,
			    'altitude'	: o.alt,
			    'azimuth'	: o.az,
			    'rising'	: ephem.Date(cutty.previous_rising(o) + dst_const),
			    'setting'	: ephem.Date(cutty.next_setting(o) + dst_const)}
		if verbose:
			print('%s IS VISIBLE' %d[o.name]['name'])
			print('%s: alt: %s azm: %s' %(d[o.name]['name'], d[o.name]['altitude'], d[o.name]['azimuth']))
			print('Previous Rising: ', ephem.Date(cutty.previous_rising(o) + dst_const))
			print('Next Setting: ', ephem.Date(cutty.next_setting(o) + dst_const))


for o in d:
	if str(d[o]['altitude']).startswith('-'):
		print('%s IS NOT VISIBLE' %d[o]['name'])
		print('%s: alt: %s azm: %s' %(d[o]['name'], d[o]['altitude'], d[o]['azimuth']))
		print('Next Rising: %s || Previous Setting: %s' %(d[o]['rising'])
		print('Previous Setting: %s' %d[o]['setting'])
	else:
		print('%s IS VISIBLE' %d[o]['name'])
		print('%s: alt: %s azm: %s' %(d[o]['name'], d[o]['altitude'], d[o]['azimuth']))
		print('Previous Rising: %s' %d[o]['rising'])
		print('Next Setting: %s' %d[o]['setting'])
