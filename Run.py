#!/usr/bin/env python3
try:
    from requests.exceptions import RequestException
    import requests, os, json, time, re, datetime
    from rich import print as Println
    from rich.columns import Columns
    from rich.panel import Panel
    from rich.console import Console
except ModuleNotFoundError as e:
    print(f"Error: {str(e).capitalize()}!")
    exit()

MISI = {"JUMLAH": 0}

class LOGIN:

    def __init__(self) -> None:
        pass

    def TIKSUB(self) -> None:
        TAMPILKAN_BANNER()
        Println(Panel(f"[bold white]Silakan Masukkan Akses Token Traodoisub Pastikan Sudah Benar, Misalnya :[bold green] TDS0nIwEjclBXOzJiOiIXZ2uoiIrIvaFGa69mciojIyV2c1Jye", width=68, style="bold bright_white", title="[bold bright_white]>> [Token TDS] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
        token = Console().input("[bold bright_white]   ╰─> ")
        self.username_traodoisub, self.koin_traodoisub, self.koin_die_traodoisub = self.PERIKSA_KOIN(akses_token=token)
        Println(Panel(f"[bold white]Silahkan Masukan Username Tumbal Akun Tiktok, Pastikan Akun Tersebut Tidak Terkunci, Misalnya :[bold green] @rozhak_official", width=68, style="bold bright_white", title="[bold bright_white]>> [Username TT] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
        username = Console().input("[bold bright_white]   ╰─> ")
        self.username_tiktok, self.userid_tiktok = self.TAMBAH_KONFIGURASI(akses_token=token, username=username)
        Println(
            Panel(f"""[bold white]Username :[bold green] {self.username_traodoisub}
[bold white]Koin :[bold yellow] {self.koin_traodoisub}
[bold white]Tiktok :[bold green] https://www.tiktok.com/@{self.username_tiktok}""", width=68, style="bold bright_white", title="[bold bright_white]>> [Welcome] <<")
        )
        with open('Penyimpanan/Akun.json', 'w') as w:
            w.write(
                json.dumps(
                    {
                        "Username": f"{self.username_tiktok}",
                        "Token": f"{token}",
                        "UniqueID": f"{self.userid_tiktok}",
                    }, indent=4
                )
            )
        time.sleep(5.5)
        return None
    
    def COOKIES(self, cookies: str) -> None:
        try:
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                'Cookie': cookies,
            }
            response = json.loads(requests.get('https://traodoisub.com/view/setting/load.php', headers = headers).text)['tokentds']
        except Exception:
            Println(Panel(f"[bold red]Maaf, Cookies Traodoisub Yang Anda Masukan Tidak Valid, Silakan Coba Lagi!", width=68, style="bold bright_white", title="[bold bright_white]>> [Cookie Invalid] <<"))
            exit()

    def PERIKSA_KOIN(self, akses_token: str) -> tuple:
        params = {
            'access_token': f'{akses_token}',
            'fields': 'profile',
        }
        response = json.loads(requests.get('https://traodoisub.com/api/', params = params).text)
        if '\'success\': 200' in str(response):
            self.username = response['data']['user'].title()
            self.koin = response['data']['xu']
            self.koin_die = response['data']['xudie']
            return (
                self.username, self.koin, self.koin_die
            )
        else:
            Println(Panel(f"[bold red]Maaf, Sepertinya Akses Token Traodoisub Sudah Tidak Valid, Silak\nan Coba Ambil Token Di Pengaturan Akun Traodoisub!", width=68, style="bold bright_white", title="[bold bright_white]>> [Token Invalid] <<"))
            time.sleep(5.5)
            self.TIKSUB()

    def TAMBAH_KONFIGURASI(self, akses_token: str, username: str) -> tuple:
        params = {
            'access_token': f'{akses_token}',
            'id': self.VALIDASI_USERNAME(username) if username.isnumeric() == False else username,
            'fields': 'tiktok_run',
        }
        response = json.loads(requests.get('https://traodoisub.com/api/', params=params).text)
        if 'Thiếu thông tin truyền vào!' in str(response):
            Println(Panel("[bold red]Maaf, Username Tiktok Yang Anda Masukan Tidak Ditemukan, Silakan Coba Masukkan Username Dengan Benar!", width=68, style="bold bright_white", title="[bold bright_white]>> [Wrong Username] <<"))
            exit()
        elif 'Thao tác quá nhanh vui lòng chậm lại' in str(response):
            Println(Panel("[bold red]Maaf, Sistem Kami Terkena Limit Saat Menambahkan Username Ke Kon\nfigurasi, Silakan Coba Lagi Nanti!", width=68, style="bold bright_white", title="[bold bright_white]>> [Username Limits] <<"))
            exit()
        elif 'Cấu hình thành công!' in str(response):
            self.userid, self.username = response['data']['id'], response['data']['uniqueID']
            return (
                self.username, self.userid
            )
        elif 'Vui lòng xác minh bạn không phải robot' in str(response):
            Println(Panel(f"[bold red]Maaf, Anda Belum Menambahkan Akun Tiktok Tersebut Di Konfiguras\ni, Silakan Untuk Menambahkan Akun Ke Konfigurasi Tiktok!", width=68, style="bold bright_white", title="[bold bright_white]>> [Config Failed] <<"))
            exit()
        else:
            Println(Panel(f"[bold red]{str(response).title()}", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            exit()

    def VALIDASI_USERNAME(self, username: str) -> str:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
        }
        response = requests.get('https://tokcount.com/?user={}'.format(username), headers=headers).text
        self.user_id = re.search(r'"userId":"(\d+)"', str(response))
        if self.user_id == None:
            Println(Panel(f"[bold red]Maaf, Username Akun Tiktok Ini Tidak Ditemukan, Silahkan Coba Lagi Dan Masukan ID Tiktok Saja!", width=68, style="bold bright_white", title="[bold bright_white]>> [Wrong Username] <<"))
            exit()
        else:
            return f"{self.user_id.group(1)}"

class TUKARKAN:
    
    def __init__(self) -> None:
        pass

    def PENGIKUT(self, cookies: str, username: str, jumlah: int) -> None: # 140.000 KOIN
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'{cookies}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        data = {
            'dateTime': str(datetime.datetime.now()).split('.')[0],
            'sl': jumlah, # MINIMAL 100 FOLLOWERS
            'id': 'https://www.tiktok.com/@{}'.format(username.replace('@', '')),
        }
        response = requests.post('https://traodoisub.com/mua/tiktok_follow/themid.php', data=data, headers=headers)
        if 'Mua thành công!' in response.text:
            Println(Panel(f"""[bold white]Username :[bold green] {username}
[bold white]Link :[bold yellow] https://www.tiktok.com/@{username.replace('@', '')}
[bold white]Follower :[bold green] +{jumlah}[bold white] >[bold red] Sedang Diproses""", width=68, style="bold bright_white", title="[bold bright_white]>> [Success] <<"))
            exit()
        elif len(response.text) == 0:
            Println(Panel("[bold red]Maaf, Cookies Anda Sudah Tidak Berfungsi Lagi, Silakan Coba Ambil Ulang Cookiesnya!", width=68, style="bold bright_white", title="[bold bright_white]>> [Invalid Cookies] <<"))
            exit()
        elif response.text == '1':
            Println(Panel(f"[bold red]Maaf, Koin Yang Anda Miliki Tidak Cukup Untuk Membeli {jumlah} Pengikut, Silakan Untuk Mencari Koin Dahulu!", width=68, style="bold bright_white", title="[bold bright_white]>> [Insufficient Coins] <<"))
            exit()
        else:
            Println(Panel(f"[bold red]{str(response.text).title()}!", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            exit()

    def LIKE(self, cookies: str, video_link: str, jumlah: int) -> None: # 35.000 KOIN
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'{cookies}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        data = {
            'id': f'{video_link}',
            'dateTime': str(datetime.datetime.now()).split('.')[0],
            'sl': jumlah, # MINIMAL 50 LIKES
        }
        response = requests.post('https://traodoisub.com/mua/tiktok_like/themid.php', data=data, headers=headers)
        if 'Mua thành công!' in response.text:
            self.video_id = re.search(r'/(\d+)', str(video_link)).group(1)
            Println(Panel(f"""[bold white]Username :[bold green] {re.search(r'/@(.*?)/video', str(video_link)).group(1)}
[bold white]Like :[bold green] +{jumlah}[bold white] >[bold red] Sedang Diproses
[bold white]Video ID :[bold yellow] {self.video_id}""", width=68, style="bold bright_white", title="[bold bright_white]>> [Success] <<"))
            exit()
        elif len(response.text) == 0:
            Println(Panel("[bold red]Maaf, Cookies Anda Sudah Tidak Berfungsi Lagi, Silakan Coba Ambil Ulang Cookiesnya!", width=68, style="bold bright_white", title="[bold bright_white]>> [Invalid Cookies] <<"))
            exit()
        elif response.text == '1':
            Println(Panel(f"[bold red]Maaf, Koin Yang Anda Miliki Tidak Cukup Untuk Membeli {jumlah} Likes, Silakan Untuk Mencari Koin Dahulu!", width=68, style="bold bright_white", title="[bold bright_white]>> [Insufficient Coins] <<"))
            exit()
        else:
            Println(Panel(f"[bold red]{str(response.text).title()}!", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            exit()
    
    def VIEWS(self, cookies: str, video_link: str, jumlah: int) -> None: # 150.000 KOIN
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'{cookies}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        data = {
            'id': f'{video_link}',
            'dateTime': str(datetime.datetime.now()).split('.')[0],
            'sl': jumlah, # MINIMAL 1000 VIEWS
        }
        response = requests.post('https://traodoisub.com/mua/tiktok_view/themid.php', data=data, headers=headers)
        if 'Dữ liệu không hợp lệ!' in response.text or len(response.text) == 0:
            Println(Panel(f"[bold red]Maaf, Koin Yang Anda Miliki Tidak Cukup Untuk Membeli {jumlah} Views, Silakan Untuk Mencari Koin Dahulu!", width=68, style="bold bright_white", title="[bold bright_white]>> [Insufficient Coins] <<"))
            exit()
        elif 'Mua thành công!' in response.text:
            self.video_id = re.search(r'/(\d+)', str(video_link)).group(1)
            Println(Panel(f"""[bold white]Username :[bold green] {re.search(r'/@(.*?)/video', str(video_link)).group(1)}
[bold white]Views :[bold green] +{jumlah}[bold white] >[bold red] Sedang Diproses
[bold white]Video ID :[bold yellow] {self.video_id}""", width=68, style="bold bright_white", title="[bold bright_white]>> [Success] <<"))
            exit()
        elif response.text == '1':
            Println(Panel(f"[bold red]Maaf, Koin Yang Anda Miliki Tidak Cukup Untuk Membeli {jumlah} Views, Silakan Untuk Mencari Koin Dahulu!", width=68, style="bold bright_white", title="[bold bright_white]>> [Insufficient Coins] <<"))
            exit()
        else:
            Println(Panel(f"[bold red]{str(response.text).title()}!", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            exit()

class JALANKAN:

    def __init__(self) -> None:
        pass

    def FOLLOW_DAN_LIKE(self, akses_token: str, delay: int, type_misi: str, type_cache: str) -> bool:
        params = {
            'access_token': f'{akses_token}',
            'fields': f'{type_misi}',
        }
        response = json.loads(requests.get('https://traodoisub.com/api/', params=params).text)
        time.sleep(4.5)
        if 'Thao tác quá nhanh vui lòng chậm lại' in str(response):
            Println(f"[bold bright_white]   ──>[bold red] SISTEM KAMI TERKENA LIMIT, SILAKAN COBA LAGI NANTI!     ", end='\r')
            time.sleep(10.5)
            return False
        else:
            self.total_misi_sukses = response.get('cache', 0)
            MISI['JUMLAH'] = int(self.total_misi_sukses or 0)

            for z in response['data']:
                for sleep in range(delay, 0, -1):
                    Println(f"[bold bright_white]   ──>[bold green] TUNGGU {sleep} DETIK!                ", end='\r')
                    time.sleep(1.0)
                self.video_id_akun, self.video_link_profile, self.mission_type = z['id'], z['link'], z['type']
                self.status_misi = "MENGIKUTI" if type_misi == 'tiktok_follow' else "MENYUKAI"
                Println(f"[bold bright_white]   ──>[bold green] {self.status_misi} @{str(self.video_id_akun).split('_')[0]}[bold white]/[bold red]{MISI['JUMLAH']}[bold white]...    ", end='\r')
                time.sleep(2.5)

                os.system(f'xdg-open {self.video_link_profile}')
                time.sleep(5.5)

                params = {
                    'access_token': f'{akses_token}',
                    'type': f'{type_cache}',
                    'id': self.video_id_akun,
                }
                response2 = json.loads(requests.get('https://traodoisub.com/api/coin/', params=params).text)
                MISI['JUMLAH'] = int(response2.get('cache', 0) or 0)

                if int(MISI['JUMLAH']) >= 8:
                    params = {
                        'type': type_cache.split('_CACHE')[0],
                        'id': type_cache.replace('_CACHE', '_API'),
                        'access_token': f'{akses_token}',
                    }
                    response3 = json.loads(requests.get('https://traodoisub.com/api/coin/', params=params).text)
                    if 'Vui lòng công khai danh sách video đã thích trên tài khoản tiktok rồi quay lại nhận!' in str(response3):
                        Println(Panel(f"[bold red]Maaf, Sistem Kami Mendeteksi Bahwa Datar Like Tiktok Di Akun Anda Private, Silakan Ubah Ke Stelan Publik!", width=68, style="bold bright_white", title="[bold bright_white]>> [Like Private] <<"))
                        exit()
                    elif '\'success\':' in str(response3):
                        self.job_success = response3['data']['job_success']
                        self.total_koin = response3['data']['xu']
                        self.tambah_koin = response3['data']['xu_them']
                        Println(Panel(f"""[bold white]Username :[bold green] {self.video_id_akun}
[bold white]Koin :[bold green] +{self.tambah_koin}[bold white] >[bold green] {self.total_koin}
[bold white]Job Sukses :[bold yellow] {self.job_success}[bold white] >[bold red] {type_misi}""", width = 68, style="bold bright_white", title = ">>> Sukses <<<"))
                        time.sleep(2.5)
                        continue
                    else:
                        Println(f"[bold bright_white]   ──>[bold red] TERJADI KESALAHAN SAAT MENDAPATKAN KOIN!     ", end='\r')
                        time.sleep(5.5)
                        continue
                else:
                    Println(f"[bold bright_white]   ──>[bold green] ANDA TELAM MENJALANKAN {MISI['JUMLAH']} MISI!     ", end='\r')
                    time.sleep(2.5)
                    continue
        return True

def TAMPILKAN_BANNER() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    Println(
        Panel(r"""[bold red]●[bold yellow] ●[bold green] ●[bold white]
[bold blue].-,.-.,-. .'(      .'(               )\.--.       .-.     /(,-.  
[bold blue]) ,, ,. ( \  )  ,')\  )  /(         (   ._.'  ,'  /  )  ,' _   ) 
[bold blue]\( |(  )/ ) (  (  '/ /   ) \/(.-,,   `-.`.   (  ) | (  (  '-' (  
[bold blue]   ) \    \  )  )   (   (      _  ) ,_ (  \   ) '._\ )  )  _   ) 
[bold blue]   \ (     ) \ (  .\ \   `._.-' \( (  '.)  ) (  ,   (  (  '-' /  
[bold blue]    )/      )/  )/  )/              '._,_.'   )/ ._.'   )/._.'   
    [underline white]Tiktok Followers With Traodoisub.com - Coded by Rozhak""", style="bold bright_white", width=68)
    )
    return None

while True:
    try:
        if not os.path.exists('Penyimpanan/Subscribe.json'):
            os.system(f'xdg-open {json.loads(requests.get("https://raw.githubusercontent.com/RozhakXD/TikSub/main/Data/Youtube.json").text)["Link"]}')
            time.sleep(3.5)
            with open('Penyimpanan/Subscribe.json', 'w+') as files:
                json.dump(
                    {'Status': True}, files, indent=4
                )
    except:pass
    try:
        TAMPILKAN_BANNER()
        username_tiktok, akses_token, userid_tiktok = json.loads(open('Penyimpanan/Akun.json', 'r').read())['Username'], json.loads(open('Penyimpanan/Akun.json', 'r').read())['Token'], json.loads(open('Penyimpanan/Akun.json', 'r').read())['UniqueID']
        username_traodoisub, koin_traodoisub, koin_die_traodoisub = LOGIN().PERIKSA_KOIN(akses_token=akses_token)
        Println(
            Columns(
                [
                    Panel(f"""[bold white]Username :[bold green] @{username_tiktok[:19]}
[bold white]User :[bold blue] {userid_tiktok[:23]}""", width=34, style = "bold bright_white"),
                    Panel(f"""[bold white]Username :[bold green] {username_traodoisub[:18]}
[bold white]Koin :[bold yellow] {koin_traodoisub}[bold white] >[bold red] {koin_die_traodoisub}""", width=33, style="bold bright_white"),
                ]
            )
        )
    except Exception as e:
        Println(Panel(f"[bold red]{str(e).title()}", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
        time.sleep(4.5)
        LOGIN().TIKSUB()
        continue

    Println(Panel("""
 [bold green]1[bold white]. Tukarkan Koin Ke Followers     [bold green]4[bold white]. Jalankan Misi Like Tiktok
 [bold green]2[bold white]. Jalankan Misi Follow Tiktok    [bold green]5[bold white]. Tukarkan Koin Ke Views
 [bold green]3[bold white]. Tukarkan Koin Ke Likes         [bold green]6[bold white]. Keluar ([bold red]Exit[bold white])
""", width = 68, style = "bold bright_white", title="[bold bright_white]>> [Key Features] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
    choice = Console().input("[bold bright_white]   ╰─> ")
    if choice in ["1", "01"]:
        try:
            if int(koin_traodoisub) > 140000: # 140000
                Println(Panel(f"[bold white]Silakan Masukkan Cookie Akun Traodoisub, Pastikan Akun Dalam Keadaan Di Login, Misalnya :[bold green] PHPSESSID=42e236a1ac143d22", width=68, style="bold bright_white", title="[bold bright_white]>> [Cookie TDS] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                cookies = Console().input("[bold bright_white]   ╰─> ")
                LOGIN().COOKIES(cookies)
                Println(Panel(f"[bold white]Silakan Masukkan Username Tumbal Akun Tiktok, Pastikan Akun Tersebut Tidak Terkunci, Misalnya :[bold green] @rozhak_official", width=68, style="bold bright_white", title="[bold bright_white]>> [Username TT] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                username = Console().input("[bold bright_white]   ╰─> ").strip()
                Println(Panel(f"[bold white]Silahkan Masukan Jumlah Pengikut, Pastikan Hanya Mengisi Angka Dan Untuk Minimum[bold red] 100[bold white] Pengikut, Misalnya :[bold green] 1000 Pengikut", width=68, style="bold bright_white", title="[bold bright_white]>> [Follower Count] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                jumlah = int(Console().input("[bold bright_white]   ╰─> "))
                if jumlah < 100:
                    Println(Panel(f"[bold red]Maaf, Jumlah Minimal Untuk Pembelian Adalah 100, Silakan Coba Untuk Menaikan Jumlah Yang Ingin Anda Beli!", width=68, style="bold bright_white", title="[bold bright_white]>> [Incorrect Quantity] <<"))
                    break
                else:
                    TUKARKAN().PENGIKUT(cookies=cookies, username=username, jumlah=jumlah)
                    break
            else:
                Println(Panel(f"[bold red]Maaf, Minimal Koin Untuk Menukarkan Ke Pengikut Adalah 140k Koin\n, Silakan Jalankan Misi Untuk Mendapatkan Banyak Koin!", width=68, style="bold bright_white", title="[bold bright_white]>> [Insufficient Coins] <<"))
                break
        except Exception as e:
            Println(Panel(f"[bold red]{str(e).title()}", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            break
    elif choice in ["2", "02"]:
        try:
            Println(Panel(f"[bold white]Silakan Masukkan Delay Misi Follow, Gunakan Delay Di Atas[bold red] 10 Detik[bold white] Agar Aman, Misalnya :[bold green] 60 Detik", width=68, style="bold bright_white", title="[bold bright_white]>> [Mission Pause] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
            delay = int(Console().input("[bold bright_white]   ╰─> "))
            Println(Panel(f"[bold white]Jika Anda Tidak Mendapatkan Koin Kemungkinan Akun Tiktok Anda Terblokir Dan Kamu Juga Diwajibkan Untuk Menggunakan[bold red]\nAplikasi Tiktok[bold white] Versi Terbaru Agar Akun Tidak Terkena Spam!", width=68, style="bold bright_white", title="[bold bright_white]>> [Notes] <<"))
            while True:
                try:
                    JALANKAN().FOLLOW_DAN_LIKE(akses_token, delay, 'tiktok_follow', 'TIKTOK_FOLLOW_CACHE')
                except RequestException:
                    Println(f"[bold bright_white]   ──>[bold red] KONEKSI ERROR!     ", end='\r')
                    time.sleep(10.0)
                    continue
                except KeyboardInterrupt:
                    Println(f"[bold bright_white]   ──>[bold red] BERHENTI!     ", end='\r')
                    time.sleep(2.5)
                    break
        except Exception as e:
            Println(Panel(f"[bold red]{str(e).title()}", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            break
    elif choice in ["3", "03"]:
        try:
            if int(koin_traodoisub) > 35000: # 35000
                Println(Panel(f"[bold white]Silakan Masukkan Cookie Akun Traodoisub, Pastikan Akun Dalam Keadaan Di Login, Misalnya :[bold green] PHPSESSID=42e236a1ac143d22", width=68, style="bold bright_white", title="[bold bright_white]>> [Cookie TDS] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                cookies = Console().input("[bold bright_white]   ╰─> ")
                LOGIN().COOKIES(cookies)
                Println(Panel(f"[bold white]Silahkan Masukan Tautan Video Tiktok Pastikan Akun Tidak Terkunci Dan Tautan Benar, Misalnya :[bold green] https://www.tiktok.com/\n@rozhak_official/video/7216193398015905050", width=68, style="bold bright_white", title="[bold bright_white]>> [Video Link] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                video_url = Console().input("[bold bright_white]   ╰─> ").strip()
                Println(Panel(f"[bold white]Silahkan Masukan Jumlah Likes, Pastikan Hanya Mengisi Angka Dan Untuk Minimum[bold red] 50[bold white] Likes, Misalnya :[bold green] 100 Likes", width=68, style="bold bright_white", title="[bold bright_white]>> [Likes Count] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                jumlah = int(Console().input("[bold bright_white]   ╰─> "))
                if jumlah < 50:
                    Println(Panel(f"[bold red]Maaf, Jumlah Minimal Untuk Pembelian Adalah 50 Likes, Silakan Coba Untuk Menaikan Jumlah Yang Ingin Anda Beli!", width=68, style="bold bright_white", title="[bold bright_white]>> [Incorrect Quantity] <<"))
                    break
                else:
                    TUKARKAN().LIKE(cookies=cookies, video_link=video_url, jumlah=jumlah)
                    break
            else:
                Println(Panel(f"[bold red]Maaf, Minimal Koin Untuk Menukarkan Ke Likes Adalah 35k Koin, Silakan Jalankan Misi Untuk Mendapatkan Banyak Koin!", width=68, style="bold bright_white", title="[bold bright_white]>> [Insufficient Coins] <<"))
                break
        except Exception as e:
            Println(Panel(f"[bold red]{str(e).title()}", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            break
    elif choice in ["4", "04"]:
        try:
            Println(Panel(f"[bold white]Silakan Masukkan Delay Misi Follow, Gunakan Delay Di Atas[bold red] 10 Detik[bold white] Agar Aman, Misalnya :[bold green] 60 Detik", width=68, style="bold bright_white", title="[bold bright_white]>> [Mission Pause] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
            delay = int(Console().input("[bold bright_white]   ╰─> "))
            Println(Panel(f"[bold white]Jika Anda Tidak Mendapatkan Koin Kemungkinan Akun Tiktok Anda Terblokir Dan Kamu Juga Diwajibkan Untuk Menggunakan[bold red]\nAplikasi Tiktok[bold white] Versi Terbaru Agar Akun Tidak Terkena Spam!", width=68, style="bold bright_white", title="[bold bright_white]>> [Notes] <<"))
            while True:
                try:
                    JALANKAN().FOLLOW_DAN_LIKE(akses_token, delay, 'tiktok_like', 'TIKTOK_LIKE_CACHE')
                except RequestException:
                    Println(f"[bold bright_white]   ──>[bold red] KONEKSI ERROR!     ", end='\r')
                    time.sleep(10.0)
                    continue
                except KeyboardInterrupt:
                    Println(f"[bold bright_white]   ──>[bold red] BERHENTI!     ", end='\r')
                    time.sleep(2.5)
                    break
        except Exception as e:
            Println(Panel(f"[bold red]{str(e).title()}", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            break
    elif choice in ["5", "05"]:
        try:
            if int(koin_traodoisub) > 150000: # 150000
                Println(Panel(f"[bold white]Silakan Masukkan Cookie Akun Traodoisub, Pastikan Akun Dalam Keadaan Di Login, Misalnya :[bold green] PHPSESSID=42e236a1ac143d22", width=68, style="bold bright_white", title="[bold bright_white]>> [Cookie TDS] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                cookies = Console().input("[bold bright_white]   ╰─> ")
                LOGIN().COOKIES(cookies)
                Println(Panel(f"[bold white]Silahkan Masukan Tautan Video Tiktok Pastikan Akun Tidak Terkunci Dan Tautan Benar, Misalnya :[bold green] https://www.tiktok.com/\n@rozhak_official/video/7216193398015905050", width=68, style="bold bright_white", title="[bold bright_white]>> [Video Link] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                video_url = Console().input("[bold bright_white]   ╰─> ")
                Println(Panel(f"[bold white]Silahkan Masukan Jumlah Views, Pastikan Hanya Mengisi Angka Dan Untuk Minimum[bold red] 1000[bold white] Views, Misalnya :[bold green] 5000 Views", width=68, style="bold bright_white", title="[bold bright_white]>> [Views Count] <<", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                jumlah = int(Console().input("[bold bright_white]   ╰─> "))
                if jumlah < 1000:
                    Println(Panel(f"[bold red]Maaf, Jumlah Minimal Untuk Pembelian Adalah 1k Views, Silakan Coba Untuk Menaikan Jumlah Yang Ingin Anda Beli!", width=68, style="bold bright_white", title="[bold bright_white]>> [Incorrect Quantity] <<"))
                    break
                else:
                    TUKARKAN().VIEWS(cookies=cookies, video_link=video_url, jumlah=jumlah)
                    break
            else:
                Println(Panel(f"[bold red]Maaf, Minimal Koin Untuk Menukarkan Ke Views Adalah 150k Koin, Silakan Jalankan Misi Untuk Mendapatkan Banyak Koin!", width=68, style="bold bright_white", title="[bold bright_white]>> [Insufficient Coins] <<"))
                break
        except Exception as e:
            Println(Panel(f"[bold red]{str(e).title()}", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            break
    elif choice in ["6", "06"]:
        os.remove('Penyimpanan/Akun.json')
        Println(Panel(f"[bold white]Terima Kasih Telah Menggunakan Tools Ini, Semoga Bermanfaat, Sampai Jumpa Lagi!", width=68, style="bold bright_white", title="[bold bright_white]>> [Exit] <<"))
        break
    else:
        Println(Panel(f"[bold red]Maaf, Pilihan Yang Anda Masukan Tidak Tersedia, Silakan Coba Lagi!", width=68, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
        time.sleep(4.5)
        continue
