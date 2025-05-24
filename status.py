from riotwatcher import LolWatcher, RiotWatcher, ApiError


api_key = 'replace your riot API'  
lol_watcher = LolWatcher(api_key)
riot_watcher = RiotWatcher(api_key)

riot_region = 'asia'      
lol_region = 'jp1'        


# riot_name = 'hosi1001'
# tag_line = 'jp1'

riot_name = input("Riot ID (name): ")
tag_line = input("Tag line (ex: 'jp1'): ")

# get the current version of champions
versions = lol_watcher.data_dragon.versions_for_region(lol_region)
champions_version = versions['n']['champion']

# get riot account inf
account_info = riot_watcher.account.by_riot_id(riot_region, riot_name, tag_line)

# get summoner inf
summoner_info = lol_watcher.summoner.by_puuid(lol_region, account_info['puuid'])
my_puuid = account_info['puuid']
# get rank inf 
rank_info = lol_watcher.league.by_summoner(lol_region, summoner_info['id'])

# 20 matches match id
match_ids = lol_watcher.match.matchlist_by_puuid(lol_region, account_info['puuid'], count=10)

# debug info 
# print("Riot Account Info:", account_info,"\n")
# print("Summoner Info:", summoner_info,"\n")
# print("Rank Info:", rank_info,"\n")

# print("Match IDs:", match_ids)

queue_type_map = {
    420: "Ranked ",
    430: "Normal",
    440: "Ranked Flex",
    450: "ARAM",
}

# rank info
tier = 'Unranked'
rank = ''
for queue in rank_info:
    if queue['queueType'] == 'RANKED_SOLO_5x5':
        tier = queue['tier'].title()  
        rank = queue['rank']          
        break
rank_all = tier + " " + rank


print(f"\nSummoner: {riot_name} #{tag_line} | Rank: {rank_all}\n")
for match_id in match_ids:
    match_detail = lol_watcher.match.by_id(lol_region, match_id)
    # print("Match Detail:", match_detail)
    participants = match_detail['info']['participants']
    queue_id = match_detail['info'].get('queueId', 0)
    match_type = queue_type_map.get(queue_id, "Others")
    kda = match_detail['info']['gameDuration']
    # print("Participants:")
    for participant in participants:
        if participant['puuid'] == my_puuid:
            champ = participant['championName']
            win = participant['win']
            print(f"{match_type:12} | Champ: {champ:10} | KDA: {participant['kills']:2}/{participant['deaths']:2}/{participant['assists']:2}| Win: {'✅' if win else '❌'}")
            # print("\n")
            break
