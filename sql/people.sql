/*Returns the details of the lab members given lab id as argument*/
SELECT name,roll_number,LM.id,person_role_name as role_name,linkedin_url,github_url,personal_web_url,blob_storage as profile_url 
FROM 
	((
		(public."TBL_LAB_MEMBER" as LM INNER JOIN public."TBL_PERSON" as person ON LM.person_id = person.id) 
	 						INNER JOIN 
	 	public."TBL_BINARY" as bin ON bin.id = person.profile_binary_id
	) INNER JOIN public."TBL_PERSON_ROLE" as prole ON prole.id = lm.person_role_id)
	
		
WHERE LM.lab_id = {0} AND person.is_active;
