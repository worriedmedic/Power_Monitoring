#/bin/python

import ephem

dst_const = (ephem.hour * -4)

cutty = ephem.Observer()
cutty.lat = '41.42'
cutty.long = '-70.92'
cutty.elevation = 20

planets = 	[ephem.Sun(),
			ephem.Moon(),
			ephem.Mars(),
			ephem.Jupiter(),
			ephem.Saturn(),
			ephem.Venus()]

for planet in planets:
	planet.compute(cutty)
	if str(planet.alt).startswith('-'):
		print('%s IS NOT VISIBLE' %planet.name)
		print('%s: alt: %s azm: %s' %(planet.name, planet.alt, planet.az))
		print('Next Rising: ', ephem.Date(cutty.next_rising(planet) + dst_const))
		print('Next Transit: ', ephem.Date(cutty.next_transit(planet) + dst_const))
		print('Next Setting: ', ephem.Date(cutty.next_setting(planet) + dst_const))
	else:
		print('%s IS VISIBLE' %planet.name)
		print('%s: alt: %s azm: %s' %(planet.name, planet.alt, planet.az))
		print('Previous Rising: ', ephem.Date(cutty.previous_rising(planet) + dst_const))
		print('Next Transit: ', ephem.Date(cutty.next_transit(planet) + dst_const))
		print('Next Setting: ', ephem.Date(cutty.next_setting(planet) + dst_const))
		
	
astro_data  = 		{'sun_rise_pr'		: cutty.previous_rising(sol),
					'sun_trans_pr'		: cutty.previous_transit(sol),
					'sun_setting_pr'	: cutty.previous_setting(sol),
					'sun_rise_nx'		: cutty.next_rising(sol),
					'sun_trans_nx'		: cutty.next_transit(sol),
					'sun_setting_nx'	: cutty.next_setting(sol),
					'moon_rise_pr'		: cutty.previous_rising(moon),
					'moon_trans_pr'		: cutty.previous_transit(moon),
					'moon_setting_pr'	: cutty.previous_setting(moon),
					'moon_rise_nx'		: cutty.next_rising(moon),
					'moon_trans_nx'		: cutty.next_transit(moon),
					'moon_setting_nx'	: cutty.next_setting(moon),
					'mars_rise_pr'		: cutty.previous_rising(mars),
					'mars_trans_pr'		: cutty.previous_transit(mars),
					'mars_setting_pr'	: cutty.previous_setting(mars),
					'mars_rise_nx'		: cutty.next_rising(mars),
					'mars_trans_nx'		: cutty.next_transit(mars),
					'mars_setting_nx'	: cutty.next_setting(mars),
					
