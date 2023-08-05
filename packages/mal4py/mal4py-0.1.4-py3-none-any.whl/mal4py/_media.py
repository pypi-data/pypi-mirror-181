class _Media:
    def __init__(self, **serie):
        self.__dict__.update(serie)
    def __repr__(self):
        return repr((self.id,self.title))
    def __str__(self):
        return f'{self.__dict__}'
    def __gt__(self, other):
        return self.id > other.id
    def __lt__(self, other):
        return self.id < other.id
    def __le__(self, other):
        return self.id <=other.id
    def __ge__(self, other):
        return self.id >=  other.id
    def __ne__(self, other):
        return self.id != other.id 
    def __eq__(self, other):
        return self.id == other.id 
    
class ErrorSearch(Exception):
    def __init__(self, **error):
        self.__dict__.update(error)
    def __str__(self):
        return f'{self.__dict__}'
    def __repr__(self):
        return repr((self.status,self.message,self.error)) 

class Anime(_Media):
    def __init__(self, **serie):
        super().__init__(**serie)
        
class AnimeListItem(_Media):
    def __init__(self, **serie):
        super().__init__(**serie)
        
class Manga(_Media):
    def __init__(self, **serie):
        super().__init__(**serie)

class MangaListItem(_Media):
    def __init__(self, **serie):
        super().__init__(**serie)

class Forum(_Media):
    def __init__(self,**serie):
        super().__init__(**serie)
    def __repr__(self):
        return repr((self.title))

class User(_Media):
    def __init__(self, **serie):
        super().__init__(**serie)
    def __repr__(self):
        return repr((self.id,self.name))
        
def set_media(media_class) -> Anime | Manga | ErrorSearch:
    def set_result(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if(result[0]==200):
                return media_class(**result[1])
            else:
                result[1].update({"status": result[0]})
                return ErrorSearch(**result[1])
        return wrapper
    return set_result

def set_media_list(media_class) -> list[Anime] | list[Manga] | ErrorSearch:
    def set_result(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if(result[0]==200):
                    aset = []
                    for res in result[1]["data"]:
                        try:
                            if not(res["list_status"] is None):
                                res["node"].update(res["list_status"])
                            if not(res["ranking"] is None):
                                res["node"].update(res["ranking"])
                        except:
                            None
                        aset.append(media_class(**res["node"]))
                    return aset
            else:
                result[1].update({"status": result[0]})
                return ErrorSearch(**result[1])
        return wrapper
    return set_result

def set_forum_list(function) -> list[Forum] | ErrorSearch:
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        if(result[0]==200):
                aset = []
                for res in result[1]["categories"]:
                    aset.append(Forum(**res))
                return aset
        else:
            result[1].update({"status": result[0]})
            return ErrorSearch(**result[1])
    return wrapper

def set_topics_forum(function) -> list[Forum] | ErrorSearch:
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        if(result[0]==200):
                aset = []
                for res in result[1]["data"]:
                    aset.append(Forum(**res))
                return aset
        else:
            result[1].update({"status": result[0]})
            return ErrorSearch(**result[1])
    return wrapper