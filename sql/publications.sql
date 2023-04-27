/* This gives us the list of publications present*/
SELECT PB.id,pub_title,description,blob_storage
FROM 
	(
		(public."TBL_PUBLICATION" as PB INNER JOIN public."TBL_BINARY" as bin ON bin.id = PB.pub_binary_id)
    )
		
WHERE PB.lab_id = {0} AND (PB.type LIKE '%journal%');