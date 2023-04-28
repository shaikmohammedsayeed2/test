/* This gives us the list for research page */
SELECT CO.id, conf_title, description, blob_storage, end_date
FROM (
    public."TBL_CONFERENCE" AS CO
    INNER JOIN public."TBL_BINARY" AS bin ON bin.id = CO.conf_binary_id
)
WHERE CO.lab_id = 1 
AND CO.end_date >= CURRENT_DATE
--UNION
--(SELECT CO1.id, conf_title, description, blob_storage, end_date
--FROM (
--    public."TBL_CONFERENCE" AS CO1
--    INNER JOIN public."TBL_BINARY" AS bin1 ON bin1.id = CO1.conf_binary_id
--)
--WHERE CO1.lab_id = 1 
--AND CO1.end_date < CURRENT_DATE
--ORDER BY end_date DESC
--LIMIT 4);