memfile="/proc/meminfo"

getmeminfo() {
  a=$(more $memfile)
  FREE=$(echo "$a" | awk 'NR==2{print $2}')
  PHYMEM=$(echo "$a" | awk 'NR==1{print $2}')
  ACTIVE=$(echo "$a" | awk 'NR==7{print $2}')
  Inactive=$(echo "$a" | awk 'NR==8{print $2}')
}
while true; do
  getmeminfo
  echo "Total Mem="$PHYMEM",FREE Mem="$FREE",Active Mem="$ACTIVE", Inactive="$Inactive""
  sleep 2
done
