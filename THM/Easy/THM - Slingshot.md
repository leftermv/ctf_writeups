---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          THM
# CTF NAME          Slingshot
# DESCRIPTION       Can you retrace an attacker's steps after they enumerate and compromise a web server?
# DIFFICULTY        Easy
# CTF LINK          https://tryhackme.com/r/room/slingshot
```

### What was the attacker's IP?

- Check the most used remote IP addresses 
	- The field is called `transaction.remote_address`.
	- In this case, the most used value is the attacker's IP

### What was the first scanner that the attacker ran against the web server?

- Filtered logs by `transaction.remote_address: ip` from above question.

- Then, I assumed the tools used by the attacker ran with the default User Agents. 

- Assuming the scanning is made against HTTP endpoints, I've filtered based on the `response.status` and `request.headers.User-Agent`.

- An easy way to do this is to look at the user agent of pages that responded with code `404`, as scanners tend to bruteforce endpoints.

### What was the User Agent of the directory enumeration tool that the attacker used on the web server?

- Same methodology as above  
- Or look directly at the most used user Agents.

### In total, how many requested resources on the web server did the attacker fail to find?

- That means all `404` responses based on the filters from question 2.
- Filter only by 404 and see how many hits you've got.

### What is the flag under the interesting directory the attacker found?

- Since the attacker **found** it, it means the response code was 200.
- Filter by 200 and take a look at `http.url` fields.

### What login page did the attacker discover using the directory enumeration tool?

- Same as above.

### What was the user agent of the brute-force tool that the attacker used on the admin panel?

- Same as above, especially if you left the User Agent field still displayed. If not, add it and take a look at the entry to see its User Agent.

### What username:password combination did the attacker use to gain access to the admin page?

- Take a look at the `request.headers.Authorization` field. You can expand the logs or add the field in the table view.
- The answer is in base 64: `Basic [base64string]`. 
- Decode it :) 

### What flag was included in the file that the attacker uploaded from the admin directory?

- Okay, so we know the url contained `/admin/` since the formulation of this question is letting us know the upload took place from `admin directory`.

I used the following query: `http.url: \\/admin/*` and I've added 
`request.body` as a column in my table view.

- Check the request body for the entry with the url `/admin/upload.php?action=upload`

### What was the first command the attacker ran on the web shell?

- back to filtering only by response status `200`, take a look in `http.url`. 

hint: it's in the `/uploads/`

### What file location on the web server did the attacker extract database credentials from using Local File Inclusion?

- Hint: LFI is using `../` to do path traversal.

### What **directory** did the attacker use to access the database manager?

- Same view, just take a look at the entries.

### What was the name of the database that the attacker **exported**?

- Take a look in the logs, same view. 
- The syntax for the right answer is `/something/something.php?db=ANSWER&another_arg=value`

### What flag does the attacker **insert** into the database?

- Take a look at the `message` field for the log that has the `import.php` page.

- You should see some INSERT queries. For better reading, copy it and paste it to cyberchef or anything similar to URL decode the string.



