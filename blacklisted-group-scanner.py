import httpx
import time

MUTE_ERRORS = False # Determines whether errors are printed to console
BASE_GROUP = 2760782 # CreepySins' SCPF
BASE_RANKS = [15, 60] # [min, max] L0: 15, L1: 20, L2: 30, L3: 40, L4: 50, L5: 60, TA: 95
BLACKLISTED_GROUPS = { 
    # blacklisted-group-id: (min-rank-id, max-rank-id),
    9995222: (60, 255), # Revitic's SCPF: L-0 - TA
    12051382: (4, 255), # dagaurdboss's SCPF: CH - TA
    3698256: (6, 255), # Alterra Industries: Grade-1 - Holder
    4272948: (3, 255), # Metably's SCPF: L-0 - TA
    11577231: (5, 255), # FallingTowers01's Thunder Scientific: L-1 - SA
    32786731: (5, 255), # SwiftPoint's/Emerceful's SCPF: SC-0 - TA
    34221887: (3, 255), # roguued's SCPF: L-0 - TA
    12764252: (4, 255), # Zednov's/Bivotic's SCPF: SC-0 - TA
}

POI = {}
COUNT = [0]

# Retry network requests and use an exponential backoff on failure
def retry_request(url, retries=3, backoff_factor=1.0):
    headers = {"User-Agent": "Mozilla/5.0"}

    for i in range(retries):
        try:
            response = httpx.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            if not MUTE_ERRORS:
                print(f"  [:(] Connection failed. Attempt {i+1}/{retries}")
        except httpx.HTTPStatusError as e:
            if not MUTE_ERRORS:
                print(f"  [:(] HTTP error occurred: {e}")
            return None
        
        if i < retries - 1:
            time.sleep(backoff_factor * (2 ** i)) # Backoff delay

    return None

# Convert the rank range to a list of workable role IDs
def convert_rank_ids(group, ranks):
    converted_ranks = []

    url = f"https://groups.roblox.com/v1/groups/{group}/roles/"
    response = retry_request(url)

    if not response:
        if not MUTE_ERRORS:
            print(f"Failed to get group roles.")
        return []

    roles = response.json()["roles"]
    for rank in roles:
        if ranks[0] <= rank["rank"] <= ranks[1]:
            converted_ranks.append(rank["id"])

    return converted_ranks

# Scans users by role in the base group (SCPF)
def get_base_users(base_ranks):
    for rank in base_ranks:
        start_time = time.time()
        print(f"[!] Searching users for role ID {rank}...")
        url = f"https://groups.roblox.com/v1/groups/{BASE_GROUP}/roles/{rank}/users?limit=100"
        next_page_cursor = None

        while True:
            if next_page_cursor:
                url = f"https://groups.roblox.com/v1/groups/{BASE_GROUP}/roles/{rank}/users?limit=100&cursor={next_page_cursor}"

            response = retry_request(url)

            if not response:
                if not MUTE_ERRORS:
                    print(f"  [:(] Failed to get role members.")
                break

            users_data = response.json()["data"]
            for user in users_data:
                is_user_blacklisted(user["userId"], user["username"])

            next_page_cursor = response.json().get("nextPageCursor")
            if not next_page_cursor:
                break

        end_time = time.time()
        print(f"  [T] Elapsed time: {round((end_time - start_time), 2)} seconds ({round(((end_time - start_time)/60), 2)} minutes).")

# Checks if the user is in a blacklisted group. Appends to PoI dictionary if so
def is_user_blacklisted(user_id, username):
    COUNT[0] += 1
    if COUNT[0] % 250 == 0:
        print(f"  [P] {COUNT[0]} users scanned.")

    url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
    response = retry_request(url)

    if not response:
        if not MUTE_ERRORS:
            print(f"  [:(] Failed to get group roles.")
        return []

    user_groups = response.json()["data"]
    user_blacklisted_groups = []
    for group in user_groups:
        group_id = group.get("group").get("id")
        if group_id in BLACKLISTED_GROUPS:
            if group.get("role").get("id") in BLACKLISTED_GROUPS[group_id]:
                user_blacklisted_groups.append(group_id)

    if user_blacklisted_groups:
        user_blacklisted_groups.insert(0, username)
        POI[user_id] = user_blacklisted_groups
        print(f"\t[X] Blacklisted '{username}' ({user_id}) in groups {', '.join(map(str, user_blacklisted_groups[1:]))}.")

# Checks if a user is banned from Roblox
def is_user_banned():
    banned_list = []
    for user in POI:
        try:
            profile_response = httpx.get(f'https://www.roblox.com/users/{user}/profile', timeout=10)
            if profile_response.status_code == 404:
                print(f"[B] User '{POI[user][0]}' ({user}) is banned from Roblox and was removed from the list.")
                banned_list.append(user)
        except httpx.RequestError:
            if not MUTE_ERRORS:
                print(f"  [:(] Could not check if {user} is banned.")

    for user_id in banned_list:
        del POI[user_id]

# Driver code
if __name__ == "__main__":
    base_ranks = convert_rank_ids(BASE_GROUP, BASE_RANKS)

    for group in BLACKLISTED_GROUPS:
        BLACKLISTED_GROUPS[group] = convert_rank_ids(group, BLACKLISTED_GROUPS[group])

    print("-"*20)
    get_base_users(base_ranks)
    print("-"*20)

    if POI:
        print("[!] Removing banned users...")
        is_user_banned()
        print("-"*20)
    print(f"{COUNT[0]} users reviewed.\n")

    if POI:
        print(f"[USERNAME] ([USER ID]): [BLACKLISTED GROUP ID]")
        for user in POI:
            print(f"{POI[user][0]} ({user}): {', '.join(map(str, POI[user][1:]))}")
    else:
        print("No blacklisted users found.")
    print("-"*20)