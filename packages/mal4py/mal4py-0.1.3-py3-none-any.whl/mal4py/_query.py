from mal4py._basic import _BasicReq
from mal4py._media import set_media, set_media_list, set_forum_list, Anime, Manga, Forum, User, AnimeListItem, MangaListItem, ErrorSearch

class MalAnime():
    def __init__(self, header_session: dict[str,str]):
        self.__slug_type = "anime"
        self.__HEADERS = header_session
        self.__query = _BasicReq(self.__HEADERS)

    @set_media_list(Anime)
    def get_list(self,q:str,limit:int=100,offset:int=0,fields:str="id,title,main_picture") -> list[Anime] | ErrorSearch:
        """Get Anime List by name"""
        payload =  {"q" : q, "limit": limit, "offset": offset, "fields": fields}
        return self.__query._get(self.__slug_type,payload)
    
    @set_media(Anime)
    def get_details(self,anime_id: int,fields: str="id,title,main_picture") -> Anime | ErrorSearch:
        """Get Anime by ID MAL"""
        payload =  {"fields":fields}
        return self.__query._get(self.__slug_type+"/%i"%(anime_id),payload)

    @set_media_list(Anime)
    def get_seasonal(self,year: int,season:str,sort:str="anime_score",limit:int=100,offset:int=0,fields:str="id,title,main_picture")-> list[Anime] | ErrorSearch:
        """Get a List Anime Seasonal actually"""
        payload =  {"sort":sort,"limit": limit, "offset": offset, "fields": fields}
        return self.__query._get(self.__slug_type+"/season/%i/%s"%(year,season),payload)

    @set_media_list(Anime)
    def get_suggested(self,limit:int=100,offset:int=0,fields:str="id,title,main_picture") -> list[Anime] | ErrorSearch:
        """Get a List of Anime suggested"""
        payload =  {"limit": limit, "offset": offset, "fields": fields}
        return self.__query._get(self.__slug_type+"/suggestions",payload)

    @set_media_list(Anime)
    def get_ranking(self,ranking_type:str = "all",limit:int=100,offset:int=0,fields:str="id,title,main_picture") -> list[Anime] | ErrorSearch:
        """Get a List Ranking Anime!"""
        payload =  {"ranking_type":ranking_type,"limit": limit, "offset": offset, "fields": fields}
        return self.__query._get(self.__slug_type+"/ranking",payload)
    
class MalManga():
    def __init__(self, header_session: dict[str,str]):
        self.__slug_type = "manga"
        self.__HEADERS = header_session
        self.__query = _BasicReq(self.__HEADERS)

    @set_media_list(Manga)
    def get_list(self,q:str,limit:int=100,offset:int=0,fields:str="id,title,main_picture") -> list[Manga] | ErrorSearch:
        """Get Manga List by name"""
        payload =  {"q" : q, "limit": limit, "offset": offset, "fields": fields}
        return self.__query._get(self.__slug_type,payload)
    
    @set_media(Manga)
    def get_details(self,manga_id:int,fields: str="id,title,main_picture") -> Manga | ErrorSearch:
        """Get Manga by ID MAL"""
        payload =  {"fields":fields}
        return self.__query._get(self.__slug_type+"/%i"%(manga_id),payload)
    
    @set_media_list(Manga)
    def get_ranking(self,ranking_type:str = "all",limit:int=100,offset:int=0,fields:str="id,title,main_picture") -> list[Manga] | ErrorSearch:
        """Get a List Ranking Manga!"""
        payload =  {"ranking_type":ranking_type,"limit": limit, "offset": offset, "fields": fields}
        return self.__query._get(self.__slug_type+"/ranking",payload)
    
class MalForum():
    
    def __init__(self, header_session: dict[str,str]):
        self.__slug_type = "forum"
        self.__HEADERS = header_session
        self.__query = _BasicReq(self.__HEADERS)
        
    @set_forum_list
    def get_board(self) -> list[Forum] | ErrorSearch:
        """Get forum boards"""
        payload =  {}
        return self.__query._get(self.__slug_type+"/boards",payload)
    
    @set_media(Forum)
    def get_topic_detail(self,topic_id:int,limit:int=100,offset:int=0) -> list[Forum] | ErrorSearch:
        """Get forum topic details"""
        payload =  {"limit": limit, "offset": offset}
        return self.__query._get(self.__slug_type+"/topic/%s" %(topic_id),payload)
    
    def get_topics(self,board_id:int,subboard_id:int,q:str,topic_user_name:str="",user_name:str="",limit:int=100,offset:int=0) -> list:
        """Get forum topic details - Unstable this function return JSON DATA maybe your repair struct!"""
        payload =  {"q":q,"board_id":board_id,"subboard_id":subboard_id,"topic_user_name":topic_user_name,"user_name":user_name,"limit": limit, "offset": offset,"sort":"recent"}
        return self.__query._get(self.__slug_type+"/topics",payload)
    
class MalUser():
    def __init__(self, header_session: dict[str,str]):
        self.__slug_type = "users"
        self.__HEADERS = header_session
        self.__query = _BasicReq(self.__HEADERS)
    
    @set_media(User)
    def get_my_info(self,user_id:str="@me",fields:str="id,name,anime_statistics,is_supporter") -> User | ErrorSearch:
        """Get my user information"""
        payload =  {"fields":fields}
        return self.__query._get(self.__slug_type+"/%s" %(user_id),payload)
    
    @set_media(MangaListItem)
    def update_mangalist_status(self,manga_id,body:dict) -> MangaListItem | ErrorSearch:
        """Add specified manga to my manga list.
            If specified manga already exists, update its status.
            This endpoint updates only values specified by the parameter."""
        return self.__query._patch("manga/%s/my_list_status" %(manga_id),data=body)
    
    def delete_mangalist_item(self,manga_id) -> list:
        """If the specified manga does not exist in user's manga list, this endpoint does nothing and returns 404 Not Found."""
        return self.__query._delete("manga/%s/my_list_status" %(manga_id))[0]
    
    @set_media_list(MangaListItem)
    def get_mangalist(self,user_id:str="@me",fields:str="list_status",status="",sort:str="list_updated_at",limit:int=100,offset:int=0) -> list[MangaListItem] | ErrorSearch:
        """Get Manga list of User"""
        payload =  {"fields":fields,"status":status,"sort":sort,"limit":limit,"offset":offset}
        return self.__query._get(self.__slug_type+"/%s/mangalist" %(user_id),payload)
    
    @set_media(AnimeListItem)
    def update_animelist_status(self,anime_id,body:dict[str,str]) -> AnimeListItem | ErrorSearch:
        """Add specified anime to my anime list.
            If specified anime already exists, update its status.
            This endpoint updates only values specified by the parameter."""
        return self.__query._patch("anime/%s/my_list_status" %(anime_id),data=body)
    
    def delete_animelist_item(self,anime_id) -> list:
        """If the specified anime does not exist in user's anime list, this endpoint does nothing and returns 404 Not Found."""
        return self.__query._delete("anime/%s/my_list_status" %(anime_id))[0]
    
    @set_media_list(AnimeListItem)
    def get_animelist(self,user_id:str="@me",fields:str="list_status",status="",sort:str="list_updated_at",limit:int=100,offset:int=0) -> list[AnimeListItem] | ErrorSearch:
        """Get Manga list of User"""
        payload =  {"fields":fields,"status":status,"sort":sort,"limit":limit,"offset":offset}
        return self.__query._get(self.__slug_type+"/%s/animelist" %(user_id),payload)