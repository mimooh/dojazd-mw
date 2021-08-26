proj="symulacje/office123/sesja1"

ls $proj/s_* | while read i; do
	cp $i $proj/scenariusz.json	
	echo $i
	python3 mw.py "$proj"
done
