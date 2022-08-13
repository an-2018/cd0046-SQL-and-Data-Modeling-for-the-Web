INSERT INTO public.locations(
	city, state)
	VALUES ('San Francisco', 'CA');
	
INSERT INTO public.locations(
	city, state)
	VALUES ('New York', 'NY');

	
INSERT INTO public.artists(
	name, image_link, 
	seeking_talent, location_id)
	VALUES ('Matt Quevedo',
			'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80', 
			false, 1);