for f in $(find . -name '*.json')
do
  python /mnt/traces/tracing/structural_sort/json_dag.py $f to-file
done
