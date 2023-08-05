![Mal4py API Banner](https://image.myanimelist.net/ui/OK6W_koKDTOqqqLDbIoPAphlZzlTj5CPK0fFssPvFnc)
![Python Lang](https://pbs.twimg.com/media/DALAHaRVoAASaTr.png)
# MAL4Py 

MAL API
An unofficial MyAnimeList API for Python 3.
  
Currently, MAL4Py is a small package for download and sync information from MyAnimeList.

#### Version 0.1.3

## API Documentation
[MAL API v2 Beta Documentation](https://myanimelist.net/apiconfig/references/api/v2)

## Installation and Usage

To install the library:

```

pip install -U mal4py

```

To import the library:

```python

from mal4py import *

```

## Example

To call the API, first you need to create an object Auth.

#### Auth Login Example

  

```python

import  asyncio
from mal4py import Auth, get_new_code_verifier, MalToken

"""
	For all cases you must declarate Auth object
"""
# ID Client MAL App Android, recomend replace for own ID Client
auth = Auth("6114d00ca681b7701d1e15fe11a4987e") 
# if your APP has a Client Secret; OMIT in all other cases (i.e. you selected "Android", "iOS", or "Other" as App Type)
auth = Auth("my_clientID","my_clientSecret") 

# UNOFFICIAL WAY TO LOGIN
"""
	This way login can execute basic querys to MAL API, but only unstable_login can you edit user info.
"""

# If you use this way, must load Id Client MAL "6114d00ca681b7701d1e15fe11a4987e" others Id Client Don't Support way

# login with user and password unstable way
account = asyncio.run(auth.unstable_login("my_user","my_password"))

# Guest login without user and password unstable way
account = asyncio.run(auth.guest_login())


# OFFICIAL WAY TO LOGIN (recomended)
""" 
	OAUTH Way generate Code
"""
code_verifier = get_new_code_verifier()
url = auth.get_oauth_url(code_verifier)
print(url)

# Open returned url, accept oauth and use returned code to authorize

authorization_code = input('Copy-paste the Authorization Code: ').strip()
account = asyncio.run(auth.authorize_with_code(authorization_code,code_verifier))

"""
	Load Token saved previously
"""

# Load Token from saved String

jsontoken = '{"token_type":"Bearer","expires_in":xxx,"access_token":"my_access_Token","refresh_token":"my_refresh_token"}'
account = auth.authorize_with_json_string(jsontoken)

# Load Token from saved Dict

token = {"token_type":"Bearer","expires_in":xxx,"access_token":"my_access_Token","refresh_token":"my_refresh_token"}
account = auth.authorize_with_json_obj(token)

# Other way to Load Token load from MalToken object saved

mal_token = MalToken._from_json_string(jsontoken)
# Or
mal_token = MalToken._from_json_obj(token)
# Load MalToken
account = auth.load_token(mal_token)

```
You can generate Token and load usign this script of [ZeroCrystal](https://gitlab.com/-/snippets/2039434)

#### Search Query Example

```python

from mal import MalAccount


# Query Anime for all login types

search = account.anime.get_details(anime_id=44511)
search = account.anime.get_list("chainsaw",limit=3)
search = account.anime.get_seasonal(2022,"winter",limit=3)
search = account.anime.get_ranking(limit=3)


# Query Anime for oAuth only or password and login user

search = account.anime.get_suggested(limit=3)


# Query Manga for all login types

search = account.manga.get_details(manga_id=13)
search = account.manga.get_list("chainsaw",limit=3)
search = account.manga.get_ranking(limit=3)


# Query Forum for all login types
# Actually MAL API have problems with integrity the object returned. (THIS BETA)

search = account.forum.get_board()
search = account.forum.get_topic_detail(topic_id=41)
search = account.forum.get_topics(q="love",subboard_id=2,board_id=0)


# Query User for only oAuth or user and password login 

search = account.user.get_my_info()
search = account.user.update_mangalist_status(13,{"status":"reading","is_rereading":False,"score":8,"num_volumes_read":1,"num_chapters_read":2,"priority":1,"num_times_reread":0,"reread_value":0,"tags":"Myread","comments":"Amazing Manga"})
search = account.user.delete_mangalist_item(13)
search = account.user.get_mangalist()
search = account.user.update_animelist_status(21,{"status":"on_hold","is_rewatching":False,"score":9,"num_watched_episodes":110,"priority":0,"num_times_rewatched":0,"rewatch_value":0,"tags":"","comments":"Me gusta la serie"})
search = account.user.delete_animelist_item(21)
search = account.user.get_animelist(status="watching")

```

## References

For each parameter required in any query you can review the documentation at [MAL API](https://myanimelist.net/apiconfig/references/api/v2)

This project was inspired by [Node-MyAnimeList](https://github.com/PolyMeilex/node-myanimelist) and [Python MAL API](https://github.com/darenliang/mal-api) projects. 

Thanks to them.