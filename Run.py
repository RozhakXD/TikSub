#!/usr/bin/env python3                            import requests, json, os, sys
from rich.panel import Panel
from rich import print
from rich.console import Console

banner = ("""[bold red]╦╔═╗   ╔═╗┬┌┐┌┌┬┐┌─┐┬─┐
[bold red]║║ ╦───╠╣ ││││ ││├┤ ├┬┘
[bold white]╩╚═╝   ╚  ┴┘└┘─┴┘└─┘┴└─""")

def __Search__(username):
    with requests.Session() as r:
        url = ('https://i.instagram.com/api/v1/users/web_profile_info/?username={}'.format(username))
        r.headers.update({
            'Host': 'i.instagram.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': None,
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        x = json.loads(r.get(url).text)
        if '\'status\': \'ok\'' in str(x):
            biografi = x['data']['user']['biography'].replace('\n',' ')
            pengikut = x['data']['user']['edge_followed_by']['count']
            mengikuti = x['data']['user']['edge_follow']['count']
            nama = x['data']['user']['full_name']
            userid = x['data']['user']['id']
            is_private = x['data']['user']['is_private']
            is_verified = x['data']['user']['is_verified']
            postingan = x['data']['user']['edge_owner_to_timeline_media']['count']
            Console(width=40, style="bold plum4").print(Panel(f"""[bold white]Biography :[bold yellow] {biografi}
[bold white]Follower  : {pengikut}
[bold white]Following : {mengikuti}
[bold white]Name      :[bold green] {nama}
[bold white]Userid    : {userid}
[bold white]Private   : {is_private}
[bold white]Verified  : {is_verified}
[bold white]Postingan : {postingan}"""))
            Console().input("[bold white][[bold green]Kembali[bold white]]");os.system(f"python3 {sys.argv[0]}")
        else:
            Console(width=40, style="bold plum4").print(Panel("[bold red]Terjadi Kesalahan Yang Tidak Diketahui!"));sys.exit()

if __name__ == '__main__':
    os.system('clear')
    Console(width=40, style="bold plum4").print(Panel(banner, title="[bold plum4]RozhakXD"), justify="center")
    try:
        Console(width=40, style="bold plum4").print(Panel("[italic white]Silahkan Masukan Username Dengan Benar, Misalnya :[italic green] Rozhak_Official"))
        username = Console().input("[bold white][[bold green]*[bold white]][bold white] Username : ")
        if len(username) <= 2:
            Console(width=40, style="bold plum4").print(Panel("[bold red]Masukan Username Dengan Benar!"));sys.exit()
        else:
            __Search__(username)
    except Exception as e:
        Console(width=40, style="bold plum4").print(Panel(f"[bold red]{str(e).title()}"));sys.exit()
