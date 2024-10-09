---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          THM
# CTF NAME          . 
# DESCRIPTION       Apply your analytical skills to analyze the malicious network traffic using Wireshark.
# DIFFICULTY        Medium
# CTF LINK         https://tryhackme.com/r/room/c2carnage
```

#### What was the date and time for the first HTTP connection to the malicious IP? 
(**answer format**: yyyy-mm-dd hh:mm:ss)

- To get the answer, first change the time display to UTC date and time

![[Pasted image 20240909162136.png]]

- Then, filter by `http` traffic.

![[Pasted image 20240909162209.png]]

```
2021-09-24 16:44:38
```

#### What is the name of the zip file that was downloaded?

- Answered in the question above.

```
documents.zip
```

#### What was the domain hosting the malicious zip file?

- First, enable IP resolution : Edit -> Preferences and enable "Resolve transport names" and "Resolve network (IP) addresses".

![[Pasted image 20240909162747.png]]

```
attirenepal.com
```

#### Without downloading the file, what is the name of the file in the zip file?

- If we use follow stream on the first http frame, we can get the file name from inside the .zip.

![[Pasted image 20240909163817.png]]

```
chart-1530076591.xls
```

#### What is the name of the webserver of the malicious IP from which the zip file was downloaded?

- From the same view as above, take a look at the value for `server`.

#### What is the version of the webserver from the previous question?

- From the same view as above, take a look at the value for `x-powered-by`.

#### Malicious files were downloaded to the victim host from multiple domains. What were the three domains involved with this activity?

- The hint is pointing us to check HTTPS traffic between 16:45:11 and 16:45:30.

![[Pasted image 20240909164522.png]]

- A further narrowing can be done using the following filter

```
tls.handshake.type == 1 and frame.time >= "2021-09-24 16:45:11" and frame.time <= "2021-09-24 16:45:30"
```

#### Which certificate authority issued the SSL certificate to the first domain from the previous question?

- By following the TCP stream of the first domain found above, we can reveal the CA. 

![[Pasted image 20240909165319.png]]

```
GoDaddy
```

#### What are the two IP addresses of the Cobalt Strike servers? Use VirusTotal (the Community tab) to confirm if IPs are identified as Cobalt Strike C2 servers. (answer format: enter the IP addresses in sequential order)

- I went to **Statistics** -> **Conversations** -> **TCP** and filtered in descending order after **Bytes B->** thinking that if the destination is a C2 server, then probably a lot of traffic happened from the destination as well (maybe malware got downloaded on the victim, or commands, or both).

- I started Checking the IP's in Virus Total.

**Hint**: it's in the first 5 IPs returned. 
**Note**: There are more malicious IPs in this list, but we need to look for Cobalt C2s only.

```
185.x.x.x, 185.x.x.x
```

#### What is the Host header for the first Cobalt Strike IP address from the previous question?

- Can be found in Virus Total Community answers as well.

#### What is the domain name for the first IP address of the Cobalt Strike server? You may use VirusTotal to confirm if it's the Cobalt Strike server (check the Community tab).

- Filter by IP in wireshark. Check **Source Address** in IPv4.

![[Pasted image 20240909171615.png]]

#### What is the domain name of the second Cobalt Strike server IP?  You may use VirusTotal to confirm if it's the Cobalt Strike server (check the Community tab).

- Same as above.

![[Pasted image 20240909171604.png]]


#### What is the domain name of the post-infection traffic?

- Filter by POST http traffic.

```
http.request.method == "POST"
```


#### What are the first eleven characters that the victim host sends out to the malicious domain involved in the post-infection traffic?

- From the same view as above, take a look in the **Info** column.

- Get the first 11 chars after **/**.

![[Pasted image 20240909171911.png]]

#### What was the length for the first packet sent out to the C2 server?

- Same as above, take a look at **Length**.

#### What was the Server header for the malicious domain from the previous question?

- Follow TCP stream of the first packet from above. 
- Take a look at **Server**.

![[Pasted image 20240909172039.png]]

#### The malware used an API to check for the IP address of the victim’s machine. What was the date and time when the DNS query for the IP check domain occurred? (**answer format**: yyyy-mm-dd hh:mm:ss UTC)

- Filter by `dns`. 
- As a tip, sort by destination IP. Our victim has the `10.9.23.102` ip.

![[Pasted image 20240909222044.png]]

#### What was the domain in the DNS query from the previous question?

- Answered this as well in the previous question.

#### Looks like there was some malicious spam (malspam) activity going on. What was the first MAIL FROM address observed in the traffic?

- Filter by `smtp` traffic.
- Take a look in the Info column --- look for `MAIL FROM: ` 

#### How many packets were observed for the SMTP traffic?

- 1439

