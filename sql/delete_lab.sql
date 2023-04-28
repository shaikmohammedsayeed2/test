--for conference
DELETE FROM public."TBL_BINARY" WHERE id = (SELECT conf_binary_id FROM public."TBL_CONFERENCE" WHERE lab_id = {0});
DELETE FROM public."TBL_CONFERENCE" WHERE lab_id = {0};
--for patent
DELETE FROM public."TBL_PATENT" WHERE lab_id = {0};
--for publications
DELETE FROM public."TBL_BINARY" WHERE id = (SELECT pub_binary_id FROM public."TBL_PUBLICATION" WHERE lab_id = {0});
DELETE FROM public."TBL_PUBLICATION" WHERE lab_id = {0};
--for events


