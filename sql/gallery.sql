/* This gives us the images of an event for the gallery page */
SELECT title,description, ARRAY_AGG(ROW(GA.event_id,GA.ID, blob_storage)) as images
FROM 
	(
		(public."TBL_EVENTS" as EV INNER JOIN public."TBL_GALLERY" as GA ON EV.id = GA.event_id) 
	 						INNER JOIN 
	 	public."TBL_BINARY" as bin ON bin.id = GA.binary_id
	)
		
WHERE EV.lab_id = {0}
GROUP BY title,description;