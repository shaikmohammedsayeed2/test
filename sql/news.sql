SELECT PB.id,pub_title,description,pub_date,blob_storage
FROM 
	(
		(public."TBL_PUBLICATION" as PB INNER JOIN public."TBL_BINARY" as bin ON bin.id = PB.pub_binary_id)
    )
		
WHERE PB.lab_id = {0} 
ORDER BY PB.pub_date DESC
LIMIT 4;