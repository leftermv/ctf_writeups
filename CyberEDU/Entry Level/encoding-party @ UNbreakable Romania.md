```
Help us decode the following string:

BQS?8F#ks-B5_]@B5B5<@;p9@@<tUBF])[hA8OkHA4Am[2u

And let’s see what the result will lead us.

Write the decoded string.
```

- After playing around with different encoding types, I've found that this is encoded with `Base85`.

- After decoding the string, we are getting a link to Google Maps. However, the flag is the link itself.

```
https://goo.gl/maps/azL{REDACTED}
```

