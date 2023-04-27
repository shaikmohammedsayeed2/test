/* This gives us the list of conferences present*/
SELECT CO.id,conf_title,description,blob_storage
FROM 
	(
		(public."TBL_CONFERENCE" as CO INNER JOIN public."TBL_BINARY" as bin ON bin.id = CO.conf_binary_id)
    )
		
WHERE CO.lab_id = {0}
UNION
SELECT PB.id,pub_title,description,blob_storage
FROM
    (
        (public."TBL_PUBLICATION" as PB INNER JOIN public."TBL_BINARY" as bin ON bin.id = PB.pub_binary_id) 
    )

WHERE PB.lab_id = {0} AND (PB.type LIKE '%conference%');