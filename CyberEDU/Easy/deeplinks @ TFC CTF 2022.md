```
I asked my intern to configure deeplinks for our iOS app. They told me they left an easter egg in the configuration file, can you find it?
```

- I had no idea what `deeplinks` are so I've started googling. 
- After a while, I came across [this](https://docs.expo.dev/guides/deep-linking/) site that described the basic  how-to's and provided a link to Apple's official documentation, [here](https://developer.apple.com/library/archive/documentation/General/Conceptual/AppSearch/UniversalLinks.html).

- Following the documentation we see that there should be an `/apple-app-site-association` endpoint.

- Navigating to that address, we are getting the `apple-app-site-association` file that contains the flag.

