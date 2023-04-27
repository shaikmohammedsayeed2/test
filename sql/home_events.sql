/* This gives us the images of an event for the gallery page */
SELECT title,description, event_date, blob_storage as url
FROM 

public."TBL_EVENTS" as EV INNER JOIN public."TBL_BINARY" as bin ON bin.id = ev.binary_id
		
WHERE EV.lab_id = {0}
ORDER BY EV.event_date DESC limit 5;