for f in $(find . -name '*.dot')
do
  cat $f >> /mnt/traces/rally_traces_event_model/all_dots.txt
done
