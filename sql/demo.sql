/*Returns the */
SELECT name,roll_number,linkedin_url,github_url,personal_web_url,blob_storage as profile_url 
FROM 
	(
		(public."TBL_LAB_MEMBER" as LM INNER JOIN public."TBL_PERSON" as person ON LM.person_id = person.id) 
	 						INNER JOIN 
	 	public."TBL_BINARY" as bin ON bin.id = person.profile_binary_id
	)
		
WHERE LM.lab_id = {0} AND person.is_active;
