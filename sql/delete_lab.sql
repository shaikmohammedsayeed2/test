--for conference
DELETE FROM public."TBL_BINARY" WHERE id = (SELECT conf_binary_id FROM public."TBL_CONFERENCE" WHERE lab_id = {0});
DELETE FROM public."TBL_CONFERENCE" WHERE lab_id = {0};
--for patent
DELETE FROM public."TBL_PATENT" WHERE lab_id = {0};
--for publications
DELETE FROM public."TBL_BINARY" WHERE id = (SELECT pub_binary_id FROM public."TBL_PUBLICATION" WHERE lab_id = {0});
DELETE FROM public."TBL_PUBLICATION" WHERE lab_id = {0};
--for events
DELETE FROM public."TBL_GALLERY" WHERE event_id = (SELECT id FROM public."TBL_EVENTS" WHERE lab_id = {0});
DELETE FROM public."TBL_BINARY" WHERE id = (SELECT binary_id FROM public."TBL_EVENTS" WHERE lab_id = {0});
DELETE FROM public."TBL_EVENTS" WHERE lab_id = {0};
--for lab member
DELETE FROM public."TBL_LAB_MEMBER" WHERE lab_id = {0};
--for poster and demo
DELETE FROM public."TBL_BINARY" WHERE id = (SELECT binary_id FROM public."TBL_POSTER_DEMO" WHERE lab_id = {0});
DELETE FROM public."TBL_POSTER_DEMO" WHERE lab_id = {0};
--for slider
DELETE FROM public."TBL_BINARY" WHERE id = (SELECT slider_binary_id FROM public."TBL_SLIDER" WHERE lab_id = {0});
DELETE FROM public."TBL_SLIDER" WHERE lab_id = {0};
