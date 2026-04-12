# Weblog

Java's Psuedo Random Number Generator at utils.random() uses a linear congruential generator (LCG).

I think the sessionID from the session cookie is involved in winning.
Mine, from DevTools -> Application -> Cookies is: `3ca24aa1-718a-4c70-a755-2d8063c15b45`

```
int[] winning = Lottery.drawNumbers(sessionId);
boolean match = java.util.Arrays.equals(ticket.getNumbers(), winning);
```

```
curl https://00262b91bd1e3ae155ed4f40698cd30f-jackpot.web.cityinthe.cloud/buy \
-H "Content-Type: application/json;" \
-H "cookie: session_id=3ca24aa1-718a-4c70-a755-2d8063c15b45" \
-d '{"numers":"[1,2,3,1,2,3]"}'  
```

curl 'https://www.example.com/api/app/job-status/' \
  -H 'authority: www.example.com' \
  -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.111.111 Safari/111.36' \
  -H 'content-type: application/json' \
  -H 'accept: */*' \
  -H 'origin: https://www.example.com' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.example.com/app/jobs/11111111/' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cookie: menuOpen_v3=true; imageSize=medium;' \
  --data-raw '{"jobIds":["1111111111111"]}' \
  --compressed