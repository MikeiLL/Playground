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
-d '{"numbers":[1,2,3,1,2,3]}'
```
