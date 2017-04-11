"""A World of Warships API wrapper"""
from requests import get
from json import loads
from enum import Enum


class Region(Enum):
    NA = 'com'
    EU = 'ru'
    RU = 'eu'
    AS = 'asia'


def _lst_of_int(id_, name):
    if id_ is None:
        return None
    if not isinstance(id_, int) \
            and any(not isinstance(x, int) for x in id_):
        raise ValueError('{} must be an int or a list of ints'.format(name))
    return ','.join(map(str, id_[:])) if isinstance(id_, list) else id_


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
                 fields: str=None, language: str=None, nation: str=None,
                 ship_id=None, type_: str=None):
        """
        Method returns the list of ships available.
        
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
        
        :param nation: Nations, separated with commas. Max limit is 100.
        
        :param ship_id: Ship ID. Max limit is 100.
        :type ship_id: int or List[int]
        
        :param type_: Ship type, separated with commas. Max limit is 100. 
        Valid values:
            "AirCarrier" — Aircraft carrier
            "Battleship" — Battleship
            "Destroyer" — Destroyer
            "Cruiser" — Cruiser
                
        :rtype: dict
        """
        ship_id = _lst_of_int(ship_id, 'ship_id')
        param = {
            'fields': fields,
            'language': language,
            'nation': nation,
            'ship_id': ship_id,
            'type': type_
        }
        return self.__get_res(region, 'encyclopedia', 'ships', param)

    def achievements(self, region: Region,
                     fields: str=None, language: str=None):
        """
        Method returns information about achievements.
        
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
        return self.__get_res(region, 'encyclopedia', 'achievements', param)

    def ship_parameters(self, region: Region, ship_id: int,
                        artillery_id: int=None, dive_bomber_id: int=None,
                        engine_id: int=None, fields: str=None,
                        fighter_id: int=None, fire_control_id: int=None,
                        flight_control_id: int=None, hull_id: int=None,
                        language: str=None, torpedo_bomber_id: int=None,
                        torpedoes_id: int=None):
        """
        Method returns parameters of ships in all existing configurations.

        :param region: The region that the method will use.
        
        :param ship_id: Ship ID
        
        :param artillery_id: Main Battery ID. 
        If the module is not indicated, module of basic configuration is used.

        :param dive_bomber_id: Dive bombers' ID. 
        If the module is not indicated, module of basic configuration is used.
        
        :param engine_id: Engine ID. 
        If the module is not indicated, module of basic configuration is used.

        :param fields: Response field. The fields are separated with commas. 
        Embedded fields are separated with dots. To exclude a field, use “-” in 
        front of its name. In case the parameter is not defined, 
        the method returns all fields. Max limit is 100.                          
        
        :param fighter_id: Fighters' ID. 
        If the module is not indicated, module of basic configuration is used.

        :param fire_control_id: ID of Gun Fire Control System. 
        If the module is not indicated, module of basic configuration is used.
        
        :param flight_control_id: ID of Flight Control System. 
        If the module is not indicated, module of basic configuration is used.

        :param hull_id: Hull ID. 
        If the module is not indicated, module of basic configuration is used.

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
            
        :param torpedo_bomber_id: Torpedo bombers' ID. 
        If the module is not indicated, module of basic configuration is used.

        :param torpedoes_id: Torpedo tubes' ID. 
        If the module is not indicated, module of basic configuration is used.

        :rtype: dict        
        """
        param = {
            'ship_id': ship_id,
            'artillery_id': artillery_id,
            'dive_bomber_id': dive_bomber_id,
            'engine_id': engine_id,
            'fields': fields,
            'fighter_id': fighter_id,
            'fire_control_id': fire_control_id,
            'flight_control_id': flight_control_id,
            'hull_id': hull_id,
            'language': language,
            'torpedo_bomber_id': torpedo_bomber_id,
            'torpedoes_id': torpedoes_id
        }
        return self.__get_res(region, 'encyclopedia', 'shipprofile', param)

    def modules(self, region: Region, fields: str=None, language: str=None,
                module_id=None, type_: str=None):
        """
        Method returns the list of available modules that can be installed on 
        ships, such as hulls, engines, etc. At least one input filter parameter 
        (module_id or type_) is required to be indicated.

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
            
        :param module_id: Module ID. Max limit is 100.
        :type module_id: int or List[int]
        
        :param type_: Module type. 
        Valid values:
            "Artillery" — Main battery
            "Torpedoes" — Torpedo tubes
            "Suo" — Gun Fire Control System
            "FlightControl" — Flight Control
            "Hull" — Hull
            "Engine" — Engine
            "Fighter" — Fighters
            "TorpedoBomber" — Torpedo Bombers
            "DiveBomber" — Dive bombers
        
        :rtype: dict
        """
        module_id = _lst_of_int(module_id, 'module_id')
        param = {
            'fields': fields,
            'language': language,
            'module_id': module_id,
            'type': type_
        }
        return self.__get_res(region, 'encyclopedia', 'modules', param)

    def exterior_items(self, region: Region, exterior_id=None, fields: str=None,
                       language: str=None, type_: str=None):
        """
        Method returns information about signals & camouflages.

        :param region: The region that the method will use.

        :param exterior_id: Exterior item ID. Max limit is 100.
        :type exterior_id: int or List[int]

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
                 
        :param type_: Exterior item type.

        :rtype: dict
        """
        exterior_id = _lst_of_int(exterior_id, 'exterior_id')
        param = {
            'exterior_id': exterior_id,
            'fields': fields,
            'language': language,
            'type': type_
        }
        return self.__get_res(region, 'encyclopedia', 'exterior', param)

    def upgrades(self, region: Region, fields: str=None, language: str=None,
                 upgrade_id=None):
        """
        Method returns the list of available ship upgrades.

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

        :param upgrade_id: Upgrade ID. Max limit is 100.
        :type upgrade_id: int or List[int]

        :rtype: dict 
        """
        upgrade_id = _lst_of_int(upgrade_id, 'upgrade_id')
        param = {
            'fields': fields,
            'language': language,
            'upgrade_id': upgrade_id
        }
        return self.__get_res(region, 'encyclopedia', 'upgrades', param)

    def service_record_levels_information(self, region: Region,
                                          fields: str=None):
        """
        Method returns information about Service Record levels.

        :param region: The region that the method will use.

        :param fields: Response field. The fields are separated with commas. 
        Embedded fields are separated with dots. To exclude a field, use “-” in 
        front of its name. In case the parameter is not defined, 
        the method returns all fields. Max limit is 100.        
        
        :rtype: dict
        """
        return self.__get_res(region, 'encyclopedia', 'accountlevels',
                              {'fields': fields})

    def commanders(self, region: Region, commander_id=None, fields: str=None,
                   language: str=None):
        """
        Method returns the information about Commanders.
        
        :param region: The region that the method will use.

        :param commander_id: Commander ID. Max limit is 100.

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
        commander_id = _lst_of_int(commander_id, 'commander_id')
        param = {
            'commander_id': commander_id,
            'fields': fields,
            'language': language
        }
        return self.__get_res(region, 'encyclopedia', 'crews', param)

    def commander_skills(self, region: Region, fields: str=None,
                         language: str=None, skill_id=None):
        """
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
      
        :param skill_id: Skill ID. Max limit is 100.
        :type skill_id: int or List[int]
        
        :rtype: dict
        """
        skill_id = _lst_of_int(skill_id, 'skill_id')
        param = {
            'fields': fields,
            'language': language,
            'skill_id': skill_id
        }
        return self.__get_res(region, 'encyclopedia', 'crewskills', param)

    def commanders_ranks(self, region: Region, fields: str=None,
                         language: str=None, nation: str=None):
        """
        Method returns the information about Commanders' ranks.

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

        :param nation: Nation

        :rtype: dict
        """
        param = {
            'fields': fields,
            'language': language,
            'nation': nation
        }
        return self.__get_res(region, 'encyclopedia', 'crewranks', param)

    def battle_types(self, region: Region,
                     fields: str=None, language: str=None):
        """
        The method returns information about battle types.

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
            'language': language,
        }
        return self.__get_res(region, 'encyclopedia', 'battletypes', param)

    def statistics_of_players_ships(self, region: Region, account_id: int,
                                    access_token: str=None, extra: str=None,
                                    fields: str=None, in_garage: bool=None,
                                    language: str=None, ship_id=None):
        """
        Method returns general statistics for each ship of a player. 
        Accounts with hidden game profiles are excluded from response. 
        Hidden profiles are listed in the field meta.hidden.

        :param region: The region that the method will use.

        :param account_id: Player account ID

        :param access_token: Access token for the private data of a user's 
        account; can be received via the authorization method; 
        valid within a stated time period

        :param extra: Extra fields that will be added to the response, 
        separated with commas. 
        Valid values:
            "club"
            "pve"
            "pve_div2"
            "pve_div3"
            "pve_solo"
            "pvp_div2"
            "pvp_div3"
            "pvp_solo"
            "rank_div2"
            "rank_div3"
            "rank_solo"

        :param fields: Response field. The fields are separated with commas. 
        Embedded fields are separated with dots. To exclude a field, use “-” in 
        front of its name. In case the parameter is not defined, 
        the method returns all fields. Max limit is 100.        
        
        :param in_garage: Filter by ship availability in the Port. 
        If the parameter is not specified, all ships are returned. 
        Parameter processing requires a valid access_token 
        for the specified account_id. 

        True — Return ships available in the Port.
        False — Return ships that are no longer in the Port.

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
            
        :param ship_id: Player's ship ID. Max limit is 100.
        :type ship_id: int or List[int]
        
        :rtype: dict
        """
        ship_id = _lst_of_int(ship_id, 'ship_id')
        if in_garage is not None:
            in_garage = '1' if in_garage else '0'
        param = {
            account_id: account_id,
            access_token: access_token,
            extra: extra,
            fields: fields,
            in_garage: in_garage,
            language: language,
            ship_id: ship_id
        }
        return self.__get_res(region, 'ships', 'stats', param)

    def ranked_battles_seasons(self, region: Region, fields: str=None,
                               language: str=None, season_id=None):
        """
        Method returns information about Ranked Battles seasons.

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
            
        :param season_id: Season ID. Max limit is 100.
        :type season_id: int or List[int]
        
        :rtype: dict
        """
        season_id = _lst_of_int(season_id, 'season_id')
        param = {
            'fields': fields,
            'language': language,
            'season_id': season_id
        }
        return self.__get_res(region, 'seasons', 'info', param)

    def ships_statistics_in_ranked_battles(self, region: Region,
                                           account_id: int,
                                           access_token: str=None,
                                           fields: str=None,
                                           language: str=None, season_id=None,
                                           ship_id=None):
        """
        Method returns players' ships statistics in Ranked Battles seasons. 
        Accounts with hidden game profiles are excluded from response. 
        Hidden profiles are listed in the field meta.hidden.

        :param region: The region that the method will use.
        
        :param account_id: Player account ID
        
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
        
        :param season_id: Season ID. Max limit is 100.
        :type season_id: int or List[int]
                
        :param ship_id: Player's ship ID. Max limit is 100.
        :type ship_id: int or List[int]

        :rtype: dict
        """
        season_id = _lst_of_int(season_id, 'season_id')
        ship_id = _lst_of_int(ship_id, 'ship_id')
        param = {
            'account_id': account_id,
            'access_token': access_token,
            'fields': fields,
            'language': language,
            'season_id': season_id,
            'ship_id': ship_id
        }
        return self.__get_res(region, 'seasons', 'shipstats', param)

    def players_statistics_in_ranked_battles(self, region: Region, account_id,
                                             access_token: str=None,
                                             fields: str=None,
                                             language: str=None,
                                             season_id=None):
        """
        Method returns players' statistics in Ranked Battles seasons. 
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
                   
        :param season_id: Season ID. Max limit is 100.
        :type season_id: int or List[int]        
        
        :rtype: dict
        """
        account_id = _lst_of_int(account_id, 'account_id')
        season_id = _lst_of_int(season_id, 'season_id')
        param = {
            'ccount_id': account_id,
            'access_token': access_token,
            'fields': fields,
            'language': language,
            'season_id': season_id
        }
        return self.__get_res(region, 'seasons', 'accountinfo', param)
