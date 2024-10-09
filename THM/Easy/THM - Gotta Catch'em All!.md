```bash
# PLATFORM          . THM
# CTF NAME          . Gotta Catch'em All!
# DESCRIPTION       . This room is based on the original Pokemon series. Can you obtain all the Pokemon in this room?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/pokemon
```

```
sudo nmap -sSVC -T5 -p- 10.10.36.31 -oN pokemons
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 581475691ea9595fb23a691c6c785c27 (RSA)
|   256 23f5fbe757c2a53ec226290e74db37c2 (ECDSA)
|_  256 f19bb58ab929aab6aaa2524a6e6595c5 (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Can You Find Them All?
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 80

- In the source code, I found the following

```
<pokemon>:<hack_the{REDACTED}n>
    <!--(Check console for extra surprise!)-->
```

- In the console I found an array containing 10 pokemon names. I guess those are the pokemons we need to find.

```
Array(10) [ "Bulbasaur", "Charmander", "Squirtle", "Snorlax", "Zapdos", "Mew", "Charizard", "Grimer", "Metapod", "Magikarp" ]
```

- The presence of the console log above was indicated by the following script

```
 <script type="text/javascript">
    	const randomPokemon = [
    		'Bulbasaur', 'Charmander', 'Squirtle',
    		'Snorlax',
    		'Zapdos',
    		'Mew',
    		'Charizard',
    		'Grimer',
    		'Metapod',
    		'Magikarp'
    	];
    	const original = randomPokemon.sort((pokemonName) => {
    		const [aLast] = pokemonName.split(', ');
    	});
    	console.log(original);
```

- The trick here was to realize that the first line in the HTML comment above represents the actual credentials needed to SSH to the box.

- Under user `pokemon`, we can find :

	- `/home/pokemon/Desktop/P0kEmOn.zip` which holds `grass-type.txt`.

	- `/Videos/Gotta/Catch/Them/ALL!/Could_this_be_what_Im_looking_for.cplusplus`  

```
# include <iostream>

int main() {
	std::cout << "ash : {REDACTED}"
	return 0;
}
```

- These seems to be the credentials for user `ash`.

- We need to find the `water` and `fire` types. I've assumed they follow the format of `grass-type` file.

```
find / -name "*type.txt" 2>/dev/null
```

```
/var/www/html/water-type.txt
/etc/why_am_i_here?/fire-type.txt
/home/pokemon/Desktop/P0kEmOn/grass-type.txt
```

- The last flag is in `/home/roots-pokemon.txt`.
