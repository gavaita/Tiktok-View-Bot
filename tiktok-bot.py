import requests, sys, json, uuid, time, os, signal
from colorama import init, Fore, Back, Style

os.system('cls' if os.name=='nt' else 'clear')

def signal_a(sig, frame):
    print(f"\n{Fore.YELLOW}[!] Stopped Program{Style.RESET_ALL}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_a)
os.system('cls' if os.name=='nt' else 'clear')
init(autoreset=True)

API = "https://zefame-free.com/api_free.php?action=config"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def safe_json(req):
    try:
        return req.json()
    except Exception:
        print(f"{Fore.RED}The API did not return valid JSON{Style.RESET_ALL}")
        print("Real answer:")
        print(req.text[:500])
        sys.exit()

names = {
    229: "TikTok Views",
    228: "TikTok Followers",
    232: "TikTok Likes",
    235: "TikTok Shares",
    236: "TikTok Favorites"
}

if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        data = json.load(f)
else:
    r = requests.get(API, headers=headers)
    if r.status_code != 200:
        print("Error HTTP:", r.status_code)
        sys.exit()
    data = safe_json(r)

services = data.get('data', {}).get('tiktok', {}).get('services', [])
for i, service in enumerate(services, 1):
    sid = service.get('id')
    name = names.get(sid, service.get('name', '').strip())
    rate = service.get('description', '').strip()
    if rate:
        rate = f"[{rate.replace('vues','views').replace('partages','shares').replace('favoris','favorites')}]"
    status = f"{Fore.GREEN}[WORKING]{Style.RESET_ALL}" if service.get('available') else f"{Fore.RED}[DOWN]{Style.RESET_ALL}"
    print(f"{i}. {name}  -  {status}  {Fore.CYAN}{rate}{Style.RESET_ALL}")

print(f"{Fore.GREEN}Modified By Gavaita{Style.RESET_ALL}")

choice = input('Select number (Enter or 0 to exit): ').strip()
if not choice or choice == "0":
    sys.exit()

try:
    idx = int(choice)
    if idx < 1 or idx > len(services):
        print('Out of range')
        sys.exit()
except:
    print('Invalid')
    sys.exit()

selected = services[idx-1]

video_link = input('Enter video link: ')

id_check = requests.post(
    "https://zefame-free.com/api_free.php",
    data={"action": "checkVideoId", "link": video_link},
    headers=headers
)

id_json = safe_json(id_check)
video_id = id_json.get("data", {}).get("videoId")
print("Parsed Video ID:", video_id)
print()
print(f"{Fore.YELLOW}[i] Press Ctrl+C to stop{Style.RESET_ALL}\n")

while True:
    order = requests.post(
        "https://zefame-free.com/api_free.php?action=order",
        data={
            "service": selected.get('id'),
            "link": video_link,
            "uuid": str(uuid.uuid4()),
            "videoId": video_id
        },
        headers=headers
    )

    result = safe_json(order)
    print(f"{Fore.GREEN}{json.dumps(result, separators=(',',':'))}{Style.RESET_ALL}")

    wait = result.get("data", {}).get("nextAvailable")
    if wait:
        try:
            wait = float(wait)
            if wait > time.time():
                remaining = int(wait - time.time())
                for countdown in range(remaining, -1, -1):
                    print(f"\r{Fore.YELLOW}Waiting {countdown} for next request...{Style.RESET_ALL}", end='', flush=True)
                    time.sleep(1)
                print()
        except:
            pass
