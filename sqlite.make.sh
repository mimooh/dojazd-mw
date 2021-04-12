#echo "select * from cnbop"    | sqlite3 -header mw.db
#echo "select * from generics" | sqlite3 -header mw.db 
#echo ".tables"				   | sqlite3 mw.db

echo "drop table cnbop" | sqlite3 mw.db 2>/dev/null
echo "drop table generics" | sqlite3 mw.db 2>/dev/null
echo "create table cnbop(id serial primary key , cnbop1 text , cnbop2 text, generic text)" | sqlite3 mw.db
for i in `seq 1 53`; do
	echo "insert into cnbop(cnbop1,cnbop2,generic) values('skręt1', 'wysokość1', 'g1')" | sqlite3 mw.db
done
echo "update cnbop set generic='g2' where id>12;" | sqlite3 mw.db;
echo "update cnbop set generic='g3' where id>23;" | sqlite3 mw.db;
echo "update cnbop set generic='g4' where id>48;" | sqlite3 mw.db;

echo "create table generics(id serial primary key,generic text, kraj text , w52 int , w75 int , d10w int, noszaki int)" | sqlite3 mw.db
echo "insert into generics(generic,kraj,w52,w75,d10w,noszaki) values

('g1', 'pl', 10, 12, 7, 1),
('g2', 'pl', 20, 20, 7, 1),
('g3', 'pl', 20, 40, 0, 1),
('g4', 'pl', 20, 40, 0, 0),
('g1', 'en', 10, 12, 7, 1),
('g2', 'en', 20, 20, 7, 1),
('g1', 'de', 20, 40, 0, 1),
('g2', 'de', 20, 40, 0, 0)
;
" | sqlite3 mw.db
