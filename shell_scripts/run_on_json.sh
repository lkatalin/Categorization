for file in rally_traces_json/*
do
  python json_dag.py "$file" 1>> script_results.out 2>>error.txt
done || exit 1
