cd capstone/data/NAVADMINS

cat pages.txt | while read page; do
  curl -s "$page" | \
  grep -oP 'href="\K[^"]+\.txt\?ver=[^"]+' | \
  sed "s|^|https://www.mynavyhr.navy.mil|"
done | xargs -n 1 -P 10 wget --content-disposition
for file in *.txt*; do mv "$file" "$(echo "$file" | sed 's/\?.*//')"; done