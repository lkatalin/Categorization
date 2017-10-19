for f in $(find . -name '*.json')
do
  python /mnt/traces/tracing/Categorization/new_json_dag.py $f to-file
done
