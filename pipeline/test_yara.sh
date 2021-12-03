docker run --rm -v /Users/holzmano/Documents/Projects/forensicPipeline/rules:/rules \
-v /Users/holzmano/Downloads/test/:/data \
plaso log2timeline --yara_rules=/rules/all.yar --storage_file /data/evidence.plaso /data/evidence

docker run --rm -v /Users/holzmano/Downloads/test/:/data \
plaso pinfo /data/evidence.plaso

docker run --rm -v /Users/holzmano/Downloads/test/:/data \
plaso psort -w /data/output.json -o json --additional-fields yara_match /data/evidence.plaso