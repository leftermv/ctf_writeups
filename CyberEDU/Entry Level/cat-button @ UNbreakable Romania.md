```
Are you an admin?
```

- On the main page, we get the Non Stop Nyan Cat app. 
- After checking the source code, we find the `/secret.php` endpoint.

```
Ya' cookie tells me you're not an admin.
```

- Looking at the cookies, we find a JWT cookie.

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6ZmFsc2V9.k2RUNg6FlRlfDjQUAQmDzPLrzZL0_sarBgiWtNr4cpE
```

- I've decoded it using [this](https://jwt.io/) tool.

- The payload --- meaning the string in the middle (strings are separated by `.`) --- is

```
{"admin":false}
```

- Using [Cyberchef's JWT Verify](https://cyberchef.org/#recipe=JWT_Verify('secret')&input=ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SmhaRzFwYmlJNlptRnNjMlY5LmsyUlVOZzZGbFJsZkRqUVVBUW1EelBMcnpaTDBfc2FyQmdpV3ROcjRjcEU) feature, I've found the `secret` key.

- I decided to try the `None Algorithm` attack. This consists of

- Modifying the header and setting `"alg":` to `"none"`; 
- Modifying the payload to `{"admin":True}`
- Base64-encoding the new header and payload.
- Removing any trailing `=` and appending `.` at the end.
- The result is

```
eyJ0eXA{REDACTED}25lIn0.eyJhZ{REDACTED}1ZX0.
```

- Then, I've intercepted the request in Burp and replaced the cookie with my own.

```
Hi admin! Here's ya' flag: CTF{98ed1dfbd{REDACTED}41758708046540237987}
```

