for file in ../rally_traces_json/*
do
    cat "$file" >> all_jsons.json
done
