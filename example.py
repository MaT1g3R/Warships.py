from wowspy.wowspy import Wows

if __name__ == '__main__':
    api_key = 'YOUR_WOWS_API_KEY'
    my_api = Wows(api_key)
    # We will search for a player and then get its stats in this example
    player_name = 'PotatoSquad'
    # Api response from Wargaming
    # We only want one result, thus it's specified limit
    player_id_response = \
        my_api.players(my_api.region.NA, player_name, fields='account_id',
                       limit=1)
    # Get the player id from the api response
    player_id = player_id_response['data'][0]['account_id']
    # Now we will use this id to search for the player's stats
    # We only want the pvp stats here, it's specified in fields param
    player_stats_response = my_api.player_personal_data(
        my_api.region.NA, player_id, fields='statistics.pvp')
    print(player_stats_response)
