DELETE FROM public."TBL_BINARY" WHERE id = (SELECT conf_binary_id FROM public."TBL_CONFERENCE" WHERE lab_id = {0});
DELETE FROM public."TBL_CONFERENCE" WHERE lab_id = {0};

