insert into story values (1, 'test_story');
insert into node values (DEFAULT, 1, 'Root', 'root'), (DEFAULT, 1, 'Root1', 'root1');
insert into story_root (id, story, node) values (DEFAULT,1,1);
insert into option values (DEFAULT, 2, 1, 'br1'), (DEFAULT, null, 1, 'br2'),
                          (DEFAULT, null, 2, 'br3'), (DEFAULT, null, 2, 'br4');

-- SELECT setval(pg_get_serial_sequence('story', 'id'), MAX(id)) FROM story;
-- SELECT setval(pg_get_serial_sequence('node', 'id'), MAX(id)) FROM node;
-- SELECT setval(pg_get_serial_sequence('option', 'id'), MAX(id)) FROM option;
