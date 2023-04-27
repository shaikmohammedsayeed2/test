/* this gives the images for the slider in the homepage*/
SELECT bin.id,blob_storage as image_url
FROM 
	(
		(public."TBL_SLIDER" as SL INNER JOIN public."TBL_BINARY" as bin ON SL.slider_binary_id = bin.id) 
	)
		
WHERE SL.lab_id = {0};