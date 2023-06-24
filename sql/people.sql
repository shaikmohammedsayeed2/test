/*Returns the details of the lab members given lab id as argument*/
SELECT name,roll_number,LM.id,person_role_name as user_role_name,linkedin_url,github_url,personal_web_url,blob_storage as profile_url ,role_name as user_access
FROM 
	(((
		(public."TBL_LAB_MEMBER" as LM INNER JOIN public."TBL_PERSON" as person ON LM.person_id = person.id) 
	 						LEFT JOIN 
	 	public."TBL_BINARY" as bin ON bin.id = person.profile_binary_id
	) INNER JOIN public."TBL_PERSON_ROLE" as prole ON prole.id = lm.person_role_id) INNER JOIN
	public."TBL_ROLE" as urole on urole.id = lm.role_id
	)
		
WHERE LM.lab_id = {0} AND person.is_active;
