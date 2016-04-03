# java -jar stack-titles.jar ~/Downloads/Stackoverflow/Posts.xml title-index/title-tag-5k.out 150000 5000 /Users/adityagaykar/Documents/stackoverflow-index/rsc/1000_tagfreq.in
# java -jar stack-titles.jar ~/Downloads/Stackoverflow/Posts.xml title-index/title-tag-15k.out 25000 15000 /Users/adityagaykar/Documents/stackoverflow-index/rsc/1000_tagfreq.in
# java -jar stack-titles.jar ~/Downloads/Stackoverflow/Posts.xml title-index/title-tag-25k.out 55000 25000 /Users/adityagaykar/Documents/stackoverflow-index/rsc/1000_tagfreq.in
# java -jar stack-titles.jar ~/Downloads/Stackoverflow/Posts.xml title-index/title-tag-30k.out 30000 30000 /Users/adityagaykar/Documents/stackoverflow-index/rsc/1000_tagfreq.in
# java -jar stack-titles.jar ~/Downloads/Stackoverflow/Posts.xml title-index/title-tag-35k.out 75000 35000 /Users/adityagaykar/Documents/stackoverflow-index/rsc/1000_tagfreq.in
# java -jar stack-titles.jar ~/Downloads/Stackoverflow/Posts.xml title-index/title-tag-40k.out 100000 40000 /Users/adityagaykar/Documents/stackoverflow-index/rsc/1000_tagfreq.in
# java -jar stack-titles.jar ~/Downloads/Stackoverflow/Posts.xml title-index/title-tag-45k.out 140000 45000 /Users/adityagaykar/Documents/stackoverflow-index/rsc/1000_tagfreq.in
# java -jar stack-titles.jar ~/Downloads/Stackoverflow/Posts.xml title-index/title-tag-50k.out 180000 50000 /Users/adityagaykar/Documents/stackoverflow-index/rsc/1000_tagfreq.in

# echo "Files created"

# echo " "

# echo "running for 5k"
python py-src/sklearn_test.py title-index/title-tag-5k.out
# echo "running for 10k"
python py-src/sklearn_test.py title-index/title-tag-10k.out
# echo "running for 15k"
python py-src/sklearn_test.py title-index/title-tag-15k.out
# echo "running for 20k"
python py-src/sklearn_test.py title-index/title-tag-20k.out
# echo "running for 25k"
python py-src/sklearn_test.py title-index/title-tag-25k.out
# echo "running for 30k"
python py-src/sklearn_test.py title-index/title-tag-30k.out
# echo "running for 35k"
python py-src/sklearn_test.py title-index/title-tag-35k.out
# echo "running for 40k"
python py-src/sklearn_test.py ./title-index/title-tag-40k.out
# echo "running for 45k"
python py-src/sklearn_test.py ./title-index/title-tag-45k.out
# echo "running for 50k"
python py-src/sklearn_test.py ./title-index/title-tag-50k.out


