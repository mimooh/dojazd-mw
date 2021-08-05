ls symulacje/office123/sesja1/s_* | while read i; do
	cp $i symulacje/office123/sesja1/scenariusz.json	
	python3 mw.py "office123/sesja1"
done
