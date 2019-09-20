import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs

# YouTube Data
def get(*args, **kwargs):
    print("-------------------YouTube Data-------------------")   
    try:
        best_match = args[0]
    
    except:
        for key, value in kwargs.items():
            if key == "youtube_code":
                youtube_code = value                

            if key == "best_match":
                best_match = value
    try:
        best_match
        if best_match[0:2] == "UC":
            youtube_code = best_match
            best_match_binary = False
        else:
            best_match_binary = True      
    except:
        best_match_binary = False
    
    if best_match_binary:
        start_url = "https://www.youtube.com/results?search_query=" + best_match        
        get_youtube_url_response = requests.get(start_url)

        for x in range(10):
            try:
                youtube_name_soup = bs(get_youtube_url_response.text, "lxml")
                raw_youtube_name_link = youtube_name_soup.find_all("div", class_="yt-lockup-byline")[x].a.get("href")
                break

            except:
                pass

        # Convert User Name to UU Format
        about_link = "https://www.youtube.com" + raw_youtube_name_link + "/about"
        youtube_code = raw_youtube_name_link.split("/")[2]

        # Get About Information
        about_html = requests.get(about_link)

        # Parse HTML
        about_soup = bs(about_html.text, "lxml")
        
        if youtube_code[0:2] == "UC":
            youtube_code = raw_youtube_name_link.split("/")[2]
            playlist_link = "https://www.youtube.com" + "/playlist?list=UU" + youtube_code[2:] 

        elif youtube_code[0:2] != "UC":
            youtube_code_raw = about_soup.find("link", rel="canonical").get("href")
            youtube_code = youtube_code_raw.split("/")[4]
            playlist_link = "https://www.youtube.com" + "/playlist?list=UU" + youtube_code[2:]            
            
    raw_months = {"Jan": 1, "Feb": 2, "Mar" : 3, "Apr" : 4, 
                "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8,
                "Sep" : 9, "Oct" : 10, "Nov" : 11, "Dec" : 12}

    def convertDate(raw_date):

        try:
            converted_date = ""
            number_month = raw_months.get(raw_date[0])
            date_str = (str(number_month) + "/" + raw_date[1] + "/" + raw_date[2]).replace(",", "")
            converted_date = datetime.strptime(date_str, '%m/%d/%Y')
            return converted_date

        except:
            print(f"{raw_date} Convert function date is not valid.")

    converted_input_date = datetime.strptime("1944-06-06", '%Y-%m-%d')

    # Get Scrape Date
    scrape_date = datetime.now().strftime("%Y-%m-%d")
    scrape_datetime = datetime.utcnow()

    # First Links
    videos_link = "https://www.youtube.com/channel/" + youtube_code + "/videos"
    about_link = "https://www.youtube.com/channel/" + youtube_code + "/about"

    # Get About Information
    about_html = requests.get(about_link)

    # Parse HTML
    about_soup = bs(about_html.text, "lxml")

    # Artist Image
    artist_image = about_soup.find("img", class_="channel-header-profile-image").get("src")

    # Artist Information
    try:
        artist_name = about_soup.find("meta", property="og:title").get("content")
        subscribers = about_soup.find(class_="yt-subscription-button-subscriber-count-branded-horizontal").text
        subscribers_str = str(subscribers)
        
        try:
            if subscribers_str[-1] == "M":
                subscribers_int = int(float(subscribers_str.replace("M",""))*1000000)
            elif subscribers_str[-1] == "K":
                subscribers_int = int(float(subscribers_str.replace("K",""))*1000)
            else:
                subscribers_int = int(subscribers_str)
        except:
            subscribers_int = 0

        total_views = about_soup.find_all("span", class_="about-stat")[1].text
        total_views_str = total_views[3:len(total_views)].split(" ")[0]

        try:
            total_views_int = int(total_views[3:len(total_views)].split(" ")[0].replace(",",""))
            joined = about_soup.find_all("span", class_="about-stat")[2].text
            joined_temp = joined.split(" ")[1:4]
            joined_convert = convertDate(joined_temp)
            joined_str = str(joined_convert).split(" ")[0]

        except:
            total_views = about_soup.find_all("span", class_="about-stat")[0].text
            total_views_str = total_views[3:len(total_views)].split(" ")[0]
            total_views_int = int(total_views[3:len(total_views)].split(" ")[0].replace(",",""))
            joined = about_soup.find_all("span", class_="about-stat")[1].text
            joined_temp = joined.split(" ")[1:4]
            joined_convert = convertDate(joined_temp)
            joined_str = str(joined_convert).split(" ")[0]
        
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("Artist Information")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(f"Channel: {artist_name}")
        print(f"Subscribers: {subscribers_int}")
        print(f"Views: {total_views_int}")
        print(f"Joined: {joined_str}")

    except Exception as e:
        print(f"Something went wrong getting artist information..{e}")

    # Getting ALL Playlist Names
    videos_response=requests.get(videos_link)
    videos_soup = bs(videos_response.text,"lxml")
    videos_soup.find_all("span",class_="branded-page-module-title-text")

    playlist_names_html = videos_soup.find_all("span",class_="branded-page-module-title-text")
    playlist_names = []

    for name in playlist_names_html:

        if name.text != "\nUploads\n" or name.text != "\nLiked videos\n":
            playlist_names.append(name.text.replace("\n",""))
            
    extra_playlists = videos_soup.find_all("span",class_="branded-page-module-title")
    playlist_names.append("Uploads")

    # Getting ALL Playlist URLS
    playlist_urls_html = videos_soup.find_all("a",class_="branded-page-module-title-link")
    playlist_urls = []
    playlist_uploads_link = "https://www.youtube.com" + "/playlist?list=UU" + youtube_code[2:]

    for playlist in playlist_urls_html:
        if "/user/" not in playlist.get("href"):
            playlist_urls.append("https://www.youtube.com" + playlist.get("href"))
            
    playlist_urls.append(playlist_uploads_link)
    urls_all = []
    counter = 0
    total_videos_all = 0
    
    for playlist_link in playlist_urls:    
        # Get Playlist Response
        playlist_response = requests.get(playlist_link)

        # Create Playlist Soup Object
        playlist_soup = bs(playlist_response.text, 'lxml')

        # Get First Video URL as Starting Point
        try:
            first_video = "https://www.youtube.com" + playlist_soup.find_all("a", class_="pl-video-title-link")[0].get("href").split("&")[0]

        except:
            continue

        first_video_within_playlist = first_video + "&" + playlist_link.split("?")[1]

        # Create Soup Object for First Video Inside Playlist
        playlist_inside_request = requests.get(first_video_within_playlist)
        playlist_inside_soup = bs(playlist_inside_request.text, "lxml")
        total_videos_in_playlist = int(playlist_inside_soup.find("span", id="playlist-length").text.replace(" videos","").replace(" video","").replace(",",""))
        total_videos_all = total_videos_all + total_videos_in_playlist

        if counter == 0:
            print("-------------------------------")
        print(f'Playlist "{playlist_names[counter]}" : {total_videos_in_playlist} videos')
        print("Getting URLs...")
        print("-------------------------------")
    
        if total_videos_in_playlist == 1:
            urls_all.append(first_video)
            
        else:
            number_of_videos_in_page = len(playlist_inside_soup.find_all("span", class_="index")) 
            last_video_index = int(playlist_inside_soup.find_all("span", class_="index")[-1].text.replace("\n        ","").replace("\n    ",""))
            last_shown_link = playlist_inside_soup.find_all("span", class_="index")[-1].find_next("a").get("href")
            link_fix = "https://www.youtube.com" + last_shown_link
            
            for i in range(total_videos_in_playlist):  
                if i == 0:       
                    first_link = playlist_inside_soup.find("span", class_="index", text=f"\n        ▶\n    ")
                    url = "https://www.youtube.com" + first_link.find_next("a").get("href")
                    original_url = url.split("&")[0]
                    if original_url not in urls_all:
                        urls_all.append(original_url)
                    next_link = first_link

                elif i == last_video_index:       
                    playlist_inside_request = requests.get(link_fix)
                    playlist_inside_soup = bs(playlist_inside_request.text, "lxml")
                    last_shown_link = playlist_inside_soup.find_all("span", class_="index")[-1].find_next("a").get("href")
                    link_fix = "https://www.youtube.com" + last_shown_link
                    try:
                        last_video_index = int(playlist_inside_soup.find_all("span", class_="index")[-1].text.replace("\n        ","").replace("\n    ",""))
                    except:
                        pass

                    first_link = playlist_inside_soup.find("span", class_="index", text=f"\n        {i+1}\n    ")

                    if first_link is None:           
                        next_link = playlist_inside_soup.find("span", class_="index", text=f"\n        ▶\n    ")

                    else:          
                        next_link = first_link

                    next_url = "https://www.youtube.com" + next_link.find_next("a").get("href")
                    original_url = next_url.split("&")[0]

                    if original_url not in urls_all:
                        urls_all.append(original_url)

                    number_of_videos_in_page = len(playlist_inside_soup.find_all("span", class_="index")) - 1

                else:

                    if i == 1:
                        first_link = playlist_inside_soup.find("span", class_="index", text=f"\n        ▶\n    ")

                    elif playlist_inside_soup.find("span", class_="index", text=f"\n        {i}\n    ") is None:
                        first_link = playlist_inside_soup.find("span", class_="index", text=f"\n        ▶\n    ")

                    else:
                        first_link = playlist_inside_soup.find("span", class_="index", text=f"\n        {i}\n    ")

                    next_link = first_link
                    next_link = next_link.find_next("span", class_="index")
                    next_url = "https://www.youtube.com" + next_link.find_next("a").get("href")
                    original_url = next_url.split("&")[0]
                    if original_url not in urls_all:
                        urls_all.append(original_url)
                
                urls_complete = round((((i+1)/total_videos_in_playlist)*100),1)
                print(f"{urls_complete}%", end="\r")
                
            counter += 1

    # Cranberries Fix
    if len(urls_all) == 0:
        [playlist_names_html.append(extra) for extra in extra_playlists]
        extra_urls_span = videos_soup.find_all("span", class_="contains-addto")
        extra_urls = []
        urls_all = ["http://www.youtube.com" + url.a.get('href') for url in extra_urls_span]

    # Going to Each Video and Extracting Data
    published_on = []
    published_on_str = []
    raw_published_on = []
    views = []
    date = []
    duration_videos = []
    likes = []
    dislikes = []
    title_videos = []
    categories = []
    paid_list = []
    family_friendly = []
    bump = 0
    
    print("\nDone...")
    print("-------------------------------")
    print("Scraping Data...")
    print("-------------------------------")
    
    for i in range(len(urls_all)):
        try:
            video_url = urls_all[i]
            video_response = requests.get(video_url)
            video_soup = bs(video_response.text, 'lxml')

            # Publish Date
            raw_publish_date = video_soup.find("div", id="watch-uploader-info").text
            raw_published_on.append(raw_publish_date)

            # Handle All Raw Dates "Premiered", ""Published", "Streamed", "X Hours Ago"
            publish_date_format = raw_publish_date.split(" ")[len(raw_publish_date.split(" "))-3:len(raw_publish_date.split(" "))]

            if publish_date_format[1] == "hours":
                publish_date_convert = datetime.strptime(scrape_date, '%Y-%m-%d')

            else:
                publish_date_convert = convertDate(publish_date_format)

            # Break if Date Less than Input Date Range
            if publish_date_convert < converted_input_date:
                break

            else:
                published_on.append(publish_date_convert)
                published_on_str.append(str(publish_date_convert).split(" ")[0])

            # Title
            title = video_soup.find("title").text.replace(" - YouTube", "")
            title_videos.append(title)

            # Views
            string_views = video_soup.find("div", id="watch7-views-info").text.replace(" views", "").replace(",","").replace("\n","")
            int_views = int(string_views)
            views.append(int_views)

            # Duration
            duration = video_soup.find("meta", itemprop="duration").get("content").replace("PT","").split("M")
            duration_mins = int(video_soup.find("meta", itemprop="duration").get("content").replace("PT","").split("M")[0])
            duration_secs = int(duration[1].replace("S",""))
            total_duration = round(duration_mins + duration_secs/60,2)
            duration_videos.append(total_duration)

            # Likes
            string_likes = video_soup.find("button", title="I like this").text
            if string_likes != "":
                int_likes = int(string_likes.replace(",",""))
                likes.append(int_likes)
            else:
                likes.append(0)

            # Dislikes
            string_dislikes = video_soup.find("button", title="I dislike this").text
            if string_dislikes != "":
                int_dislikes = int(string_dislikes.replace(",",""))
                dislikes.append(int_dislikes)
            else:
                dislikes.append(0)

            # Category
            category = video_soup.find("h4", class_="title", text="\n      Category\n    ").find_next("a").text
            categories.append(category)

            # Paid
            try:
                paid = video_soup.find("meta", itemprop="paid").get("content")
                paid_list.append(paid)
            except:
                paid_list.append("")

            # Family Friendly
            family = video_soup.find("meta", itemprop="isFamilyFriendly").get("content")
            family_friendly.append(family)
            
            # Percent Complete            
            percent_complete = round(((i+1) / (len(urls_all)))*100,1)
            percent_complete_str = str(percent_complete)
                
            print(f"{percent_complete}%", end = "\r")

        # Remove any data apended to lists during an exception, account for smaller list size after removal vs. i
        except Exception as e:
            print(f"error in getting data from url...{e}")
            print(f"Skipped {video_url}...")
            try:
                published_on.pop(i-bump)
            except:
                pass            
            try:
                raw_published_on.pop(i-bump)
            except:
                pass            
            try:
                views.pop(i-bump)
            except:
                pass            
            try:
                date.pop(i-bump)
            except:
                pass            
            try:
                duration_videos.pop(i-bump)
            except:
                pass            
            try:
                likes.pop(i-bump)
            except:
                pass
            try:
                dislikes.pop(i-bump)
            except:
                pass
            try:
                title_videos.pop(i-bump)
            except:
                pass
            try:
                categories.pop(i-bump)
            except:
                pass
            try:
                paid_list.pop(i-bump)
            except:
                pass
            try:    
                family_friendly.pop(i-bump)
            except:
                pass
            try:
                urls_all.pop(i-bump)
            except:
                pass
            try:
                published_on_str.pop(i-bump)
            except:
                pass
            bump = bump + 1
            continue
    
    print("\nDone...")
    print("--------------------------------------------------")
    
    dict_output = {"CHANNEL_NAME" : artist_name,
                   "CHANNEL_CODE" : youtube_code,
                   "PUBLISHED" : published_on,
                   "VIEWS" : views,
                   "DURATION" :duration_videos,
                   "LIKES":likes,
                   "DISLIKES":dislikes,
                   "TITLE":title_videos,
                   "CATEGORY":categories,
                   "PAID":paid_list,
                   "FAMILY_FRIENDLY":family_friendly,
                   "URL":urls_all,
                  }
    
    return dict_output