#!/bin/bash

cd ./capstone/data/NAVADMINS

cat pages.txt | while read page; do
  curl -s "$page" \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -b '_ga=GA1.1.1411441383.1742821864; dnn_IsMobile=False; ARRAffinity=be7b7313be99bcc038c22324f35ed426bb13adeb9cc40a0c0c841cedf7a0f926; .ASPXANONYMOUS=-tJRnqwq4zwnNXbdvotNLPPz8O48klUX-XVQ20AyjFwqhjAVaZZT4ucxE5xOY3M9DQRuwHd0hNEtll-Nr5tJy5j4AgnZtdQ1XXsdGVbmtecOqd4O0; _ga_CSLL4ZEK4L=GS1.1.1742821863.1.1.1742822620.0.0.0' \
  -H 'dnt: 1' \
  -H 'pragma: no-cache' \
  -H 'priority: u=0, i' \
  -H 'referer: https://www.mynavyhr.navy.mil/References/Messages/' \
  -H 'sec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36' | \
  grep -oP 'href="\K[^"]+\.txt\?ver=[^"]+' | \
  sed "s|^|https://www.mynavyhr.navy.mil|"
done | xargs -n 1 -P 10 wget --content-disposition
for file in *.txt*; do mv "$file" "$(echo "$file" | sed 's/\?.*//')"; done