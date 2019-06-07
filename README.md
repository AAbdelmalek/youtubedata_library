### YouTube Data
YouTube Data is a library that provides comprehensive scraping video metadata scraping. Results are returned in a dictionary and include likes, dislikes, views, publish dates and more.

Website: [youtubedata.io](https://www.youtubedata.io)

### Usage
##### Arguments
Usage is simple, the first method is to not pass any keyword arguments. In this case, the function will determine whether a channel code was passed. 

*Channel Codes begin with UC. For example, Ariana Grande's channel code is UC9CoOnJkIBMdeijd9qYoT_g*.

If a channel code was passed, YouTube Data will proceed straight to the scraping algorithm and extract the desired data. Otherwise, a step is added to find the channel that best matches the entered argument.

```python
youtubedata("UC9CoOnJkIBMdeijd9qYoT_g")
```

```python
youtubedata("Ariana Grande")
```

##### Keyword Arguments
The second method is to explicity pass the keyword arguments *channel_code* and *best_match*. This way YouTube Data does not have to guess which is being provided.

```python
youtubedata(channel_code = "UC9CoOnJkIBMdeijd9qYoT_g")
```

```python
youtubedata(best_match = "Ariana Grande")
```

### Progress
Progress is indicated through percentage complete print statements. The algorithm works by first identifying all "playlists" associated to the channel and then extracting all video URLs in each playlist and then deduplicating any repeated URLs.