"""A World of Warships API wrapper"""
from requests import get
from json import loads
from enum import Enum


class Region(Enum):
    NA = 'com'
    EU = 'ru'
    RU = 'eu'
    AS = 'asia'


class Wows:
    """
    A World of Warships API wrapper
    """
    def __init__(self, key):
        self.__key = key
        self.__blankurl = 'https://api.worldofwarships.' \
                          '{}/wows/{}/{}/?application_id=' + self.__key
        self.region = Region

    def __get_res(self, region: Region, method_block: str, method_name: str,
                  params: dict):
        res = self.__blankurl.format(region.value, method_block, method_name)
        for key, val in params.items():
            if val is not None:
                res += '&' + key + '=' + str(val)
        return loads(get(res).content)

    def players(self, region: Region, search: str,
                fields: str = None, language: str = None, limit: int = None,
                type_: str = None):
        """
        Method returns partial list of players. The list is filtered by initial 
        characters of user name and sorted alphabetically.

        :param region: The region that the method will use.

        :param search: Player name search string. 
        Parameter "type_" defines minimum length and type of search. 
        Using the exact search type, you can enter several names, 
        separated with commas. Maximum length: 24.

        :param fields: Response field. The fields are separated with commas. 
        Embedded fields are separated with dots. To exclude a field, use “-” 
        in front of its name. In case the parameter is not defined, 
        the method returns all fields. Max limit is 100.

        :param language: Localization language. Default depends on region.
        Valid values:
            "cs" — Čeština
            "de" — Deutsch
            "en" — English (Default for NA and EU)
            "es" — Español
            "fr" — Français
            "ja" — 日本語
            "pl" — Polski
            "ru" — Русский (Default for RU)
            "th" — ไทย (Default for AS)
            "zh-tw" — 繁體中文

        :param limit: Number of returned entries (fewer can be returned, 
        but not more than 100). If the limit sent exceeds 100, 
        an limit of None is applied (by default).

        :param type_: Search type. Default is "startswith". 
        Valid values:
            "startswith" — Search by initial characters of player name. 
            Minimum length: 3 characters. 
            Maximum length: 24 characters. (by default)

            "exact" — Search by exact match of player name. Case insensitive. 
            You can enter several names, separated with commas (up to 100).

        :rtype: dict
        """
        param = {
            'search': search,
            'fields': fields,
            'language': language,
            'limit': limit,
            'type': type_
        }
        return self.__get_res(region, 'account', 'list', param)

    def player_personal_data(self, region: Region, account_id,
                             access_token: str = None, extra: str = None,
                             fields: str = None, language: str = None):
        """
        Method returns player details. Players may hide their game profiles, 
        use field hidden_profile for determination.

        :param region: The region that the method will use.

        :param account_id: Player account ID. Max limit is 100. Min value is 1.
        :type account_id: int or List[int]

        :param access_token: Access token for the private data of a user's 
        account; can be received via the authorization method; 
        valid within a stated time period

        :param extra: Extra fields that will be added to the response,
        separated with commas.
        Valid values:
        "private.grouped_contacts"
        "private.port"
        "statistics.club"
        "statistics.pve"
        "statistics.pve_div2"
        "statistics.pve_div3"
        "statistics.pve_solo"
        "statistics.pvp_div2"
        "statistics.pvp_div3"
        "statistics.pvp_solo"
        "statistics.rank_div2"
        "statistics.rank_div3"
        "statistics.rank_solo"

        :param fields: Response field. The fields are separated with commas. 
        Embedded fields are separated with dots. To exclude a field, use “-” in 
        front of its name. In case the parameter is not defined, 
        the method returns all fields. Max limit is 100.

        :param language: Localization language. Default depends on region.
        Valid values:
            "cs" — Čeština
            "de" — Deutsch
            "en" — English (Default for NA and EU)
            "es" — Español
            "fr" — Français
            "ja" — 日本語
            "pl" — Polski
            "ru" — Русский (Default for RU)
            "th" — ไทย (Default for AS)
            "zh-tw" — 繁體中文

        :rtype: dict
        """
        account_id = _lst_of_int(account_id, 'account_id')
        param = {
            'account_id': account_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'language': language
        }
        return self.__get_res(region, 'account', 'info', param)

    def player_achievements(self, region: Region, account_id,
                            access_token: str=None, fields: str=None,
                            language: str=None):
        """
        Method returns information about players' achievements. 
        Accounts with hidden game profiles are excluded from response. 
        Hidden profiles are listed in the field meta.hidden.
        :param region: The region that the method will use.

        :param account_id: Player account ID. Max limit is 100. Min value is 1.
        :type account_id: int or List[int]

        :param access_token: Access token for the private data of a user's 
        account; can be received via the authorization method; 
        valid within a stated time period

        :param fields: Response field. The fields are separated with commas. 
        Embedded fields are separated with dots. To exclude a field, use “-” in 
        front of its name. In case the parameter is not defined, 
        the method returns all fields. Max limit is 100.

        :param language: Localization language. Default depends on region.
        Valid values:
            "cs" — Čeština
            "de" — Deutsch
            "en" — English (Default for NA and EU)
            "es" — Español
            "fr" — Français
            "ja" — 日本語
            "pl" — Polski
            "ru" — Русский (Default for RU)
            "th" — ไทย (Default for AS)
            "zh-tw" — 繁體中文
        
        :rtype: dict
        """
        account_id = _lst_of_int(account_id, 'account_id')
        param = {
            'account_id': account_id,
            'access_token': access_token,
            'fields': fields,
            'language': language
        }
        return self.__get_res(region, 'account', 'achievements', param)

    def player_statistics_by_date(self, region: Region, account_id,
                                  access_token: str=None, dates: str=None,
                                  extra: str=None, fields: str=None,
                                  language: str=None):
        """
        Method returns statistics slices by dates in specified time span.
        :param region: The region that the method will use.

        :param account_id: Player account ID. Max limit is 100. Min value is 1.
        :type account_id: int or List[int]

        :param access_token: Access token for the private data of a user's 
        account; can be received via the authorization method; 
        valid within a stated time period
        
        :param dates: List of dates to return statistics slices for, 
        separated with commas. 
        Format: YYYYMMDD. Max. dates range - 28 days from the current date. 
        Statistics slice for yesterday will be returned by default. 
        Max limit is 10.
        
        :param extra: Extra fields that will be added to the response,
        separated with commas.
        Valid values:
        "pve"

        :param fields: Response field. The fields are separated with commas. 
        Embedded fields are separated with dots. To exclude a field, use “-” in 
        front of its name. In case the parameter is not defined, 
        the method returns all fields. Max limit is 100.

        :param language: Localization language. Default depends on region.
        Valid values:
            "cs" — Čeština
            "de" — Deutsch
            "en" — English (Default for NA and EU)
            "es" — Español
            "fr" — Français
            "ja" — 日本語
            "pl" — Polski
            "ru" — Русский (Default for RU)
            "th" — ไทย (Default for AS)
            "zh-tw" — 繁體中文

        :rtype: dict
        """
        account_id = _lst_of_int(account_id, 'account_id')
        param = {
            'account_id': account_id,
            'access_token': access_token,
            'dates': dates,
            'extra': extra,
            'fields': fields,
            'language': language
        }
        return self.__get_res(region, 'account', 'statsbydate', param)

    def information_about_encyclopedia(self, region: Region,
                                       fields: str=None, language: str=None):
        """
        Method returns information about encyclopedia.
        
        :param region: The region that the method will use.
        
        :param fields: Response field. The fields are separated with commas. 
        Embedded fields are separated with dots. To exclude a field, use “-” in 
        front of its name. In case the parameter is not defined, 
        the method returns all fields. Max limit is 100.        
        
        :param language: Localization language. Default depends on region. 
        Valid values:
            "cs" — Čeština
            "de" — Deutsch
            "en" — English (Default for NA and EU)
            "es" — Español
            "fr" — Français
            "ja" — 日本語
            "pl" — Polski
            "ru" — Русский (Default for RU)
            "th" — ไทย (Default for AS)
            "zh-tw" — 繁體中文
            "tr" — Türkçe
            "zh-cn" — 中文
            "pt-br" — Português do Brasil
            "es-mx" — Español (México)        
            
        :rtype: dict
        """
        param = {
            'fields': fields,
            'language': language
        }
        return self.__get_res(region, 'encyclopedia', 'info', param)

    def warships(self, region: Region,
                 fields, language, nation, ship_id, type_):
        """
        
        :param region: 
        :param fields: 
        :param language: 
        :param nation: 
        :param ship_id: 
        :param type_: 
        :return: 
        """
        pass


def _lst_of_int(id_, name):
    if not isinstance(id_, int) \
            and any(not isinstance(x, int) for x in id_):
        raise ValueError('{} must be an int or a list of ints'.format(name))
    return ','.join(map(str, id_[:])) if isinstance(id_, list) else id_
