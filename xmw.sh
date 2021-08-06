ls symulacje/office123/sesja1/s_* | while read i; do
	cp $i symulacje/office123/sesja1/scenariusz.json	
	echo $i
	python3 mw.py "office123/sesja1"
done
