INSERT INTO public.locations(city, state) VALUES ('San Francisco', 'CA');
	
INSERT INTO public.locations(city, state) VALUES ('New York', 'NY');
	
INSERT INTO public.artists(name, image_link, seeking_talent, location_id)
VALUES ('Matt Quevedo','https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80', false, 1);

INSERT INTO public.shows(name, venue_id, artist_id, start_time)
VALUES ('The Musical Hop', 1, 1, '2022-08-30');

INSERT INTO public.venues(
	name, address, 
	image_link, 
	facebook_link, 
	website_link, 
	seeking_talent, seeking_description, 
	location_id)
	VALUES ('The Musical Hop', '1015 Folsom Street', 
			'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60', 
			'https://www.facebook.com/TheMusicalHop', 
			'https://www.themusicalhop.com', 
			false, 
            'We are on the lookout for a local artist to play every two weeks. Please call us.', 
			1
            );