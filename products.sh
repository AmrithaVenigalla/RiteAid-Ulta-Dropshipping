#!/bin/bash
while true
do
	#Getting xhtml files for all products
	store1=$1
	store2=$2

	URLS=$(cat $store1)
	counter=1

	for URL in $URLS
	do
		filename=$URL
		echo $filename
		wget --convert-links --adjust-extension --no-clobber -e robots=off -O $counter.html $URL
		java -jar tagsoup-1.2.1.jar --files $counter.html
		for file in *.html
		do
			rm $file 
		done 
		for file in *.xhtml
		do
			python3 parser.py $file $counter
			rm $file 
		done
		((counter+=1))
	done
	
	URLS=$(cat $store2)
	counter=1

	for URL in $URLS
	do
		filename=$URL
		echo $filename
		wget --convert-links --adjust-extension --no-clobber -e robots=off -O $counter.html $URL
		java -jar tagsoup-1.2.1.jar --files $counter.html
		for file in *.html
		do
			rm $file 
		done 
		for file in *.xhtml
		do
			python3 parser.py $file $counter
			rm $file 
		done
		((counter+=1))
	done
	sleep 6h
done 


