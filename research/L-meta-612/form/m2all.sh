for f in $FILES; do
while read -r g; do
  n=$(python3 -c "import json;E=json.loads('$g');print(max(max(e) for e in E)+1)")
  r=$(timeout 600 python3 meas2.py $n "$g" 1500 7 | tail -1)
  echo "$n $g $r"
done < $f
done
