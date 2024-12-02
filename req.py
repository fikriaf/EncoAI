import urllib.parse
import os, re, json, subprocess, random, time
from bs4 import BeautifulSoup as bs
from requests import get,post
from speak import Speak
from hear import Hear



head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}




def JadwalSalat():
    while True:
        Speak("whats your city? type below")
        kota = input("Nama kota : ")
        if not kota:
            continue
        break
    url = "https://www.jadwalsholat.org/adzan/monthly.php"
    get_value = get(url,headers=head).text
    for i in bs(get_value, "html.parser").find_all("option"):
        if i.get_text() == kota.capitalize():
            value = i.get("value")
    
    save = []
    get_jadwal = get(f"{url}?id={value}", headers=head).text
    for j in bs(get_jadwal, "html.parser").find("tr", class_="table_highlight").find_all("td"):
        jadwal = j.get_text()
        save.append(jadwal)
    print(f"""
==========================
        {kota.capitalize()}
==========================
Imsyak  : {save[1]}
Subuh   : {save[2]}
Terbit  : {save[3]}
Dhuha   : {save[4]}
Dzuhur  : {save[5]}
Asar    : {save[6]}
Maghrib : {save[7]}
Isya    : {save[8]}
==========================
""")
    Speak(f"Thats a prayer schedule in {kota.capitalize()}")

def Quran():
    while True:
        Speak("what you want ?")
        surah = input("Surah ke : ")
        ayat = input(("Ayat ke : "))
        if not surah:
            continue
        if surah and not ayat:
            url = f"https://al-quran-8d642.firebaseio.com/surat/{surah}.json?print=pretty"
        url = f"https://al-quran-8d642.firebaseio.com/surat/{surah}.json?print=pretty"
        break

    curl_output = subprocess.check_output(f"curl {url}", shell=True)
    curl_output = curl_output.decode("utf-8")
    json_data = json.loads(curl_output)
    h = 1
    for datas in json_data:
        print(f"""[ {str(h)} ] {datas["ar"]}

     {datas["id"]}
________________________
""")
        h+=1

def News():
    while True:
        Speak("what will search ?")
        q = input("query : ")
        if not q:
            continue
        q = q.replace(" ", "%20")
        break
    try:
        url = f"https://the-lazy-media-api.vercel.app/api/search?search={q}"
        curl_output = subprocess.check_output(f"curl {url}", shell=True)
        curl_output = curl_output.decode("utf-8")
        json_data = json.loads(curl_output)
        h=0
        for item in json_data:
            h+=1
            title = item["title"]
            key = item["key"]
            author = item["author"]
            tag = item["tag"]
            times = item["time"]
            desc = item["desc"]

            print(f"""
--------------------------------------------------------------------------
                                [ {str(h)} ]
--------------------------------------------------------------------------
Title   : {title}
Author  : {author}
Tag     : {tag}
Time    : {times}
Descrip : {desc}
link   : {key}
""")
            Speak(f"Thats news have {str(h)} topic")
        while True:
            Speak("Whats your selected topic number ?")
            num = input("Select num [1,2,3,etc] : ")
            if not num:
                continue
            break
        detail = json_data[int(num)-1]["key"]
        url_select = f"https://the-lazy-media-api.vercel.app/api/detail/{detail}"
        curl_output_select = subprocess.check_output(f"curl {url_select}", shell=True)
        curl_output_select = curl_output_select.decode("utf-8")
        json_data_select = json.loads(curl_output_select)
        berita_save = [x for x in json_data_select["results"]["content"]]
        print(f"""################################
Title : {json_data_select["results"]["title"]}
{berita_save} 
################################""")
        Speak("Thats a topic you want")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Curl command: {e}")
        return None

now_played = []
def Music():
    Speak("can i recommended a music for you ?")
    q = Hear()

    if "no" in q or "nope" in q:
        folder = r"C:\Users\User\Music\all"
        files = os.listdir(folder)

        h=0
        save_list = []
        for file in files:
            if re.search(r"\.mp3$", file):
                print(str(h), file)
                save_list.append(file)
                h+=1

        Speak("This is all list of music, please select number")
        select_num = input("Select Num : ")
        if select_num < h:
            music_path = os.path.join(folder, save_list[select_num])
            os.startfile(music_path)
            with open("now_played.txt", 'w') as file_played:
                file_played.write(save_list[select_num])


    else:
        folder = r"C:\Users\User\Music\all"
        files = os.listdir(folder)
        mp3_files = [file for file in files if re.search(r"\.mp3$", file)]
        
        if mp3_files:
            random_music = random.choice(mp3_files)
            music_path = os.path.join(folder, random_music)
            os.startfile(music_path)
            with open("now_played.txt", 'w') as file_played:
                file_played.write(random_music)
        else:
            print("Tidak ada file musik dalam direktori.")

def NextMusic():
    folder = r"C:\Users\User\Music\all"
    files = os.listdir(folder)

    h=0
    f=0
    now_played  = open("now_played.txt", 'r').read()
    save_played = []
    for file in files:
        if re.search(r"\.mp3$", file):
            h+=1
            save_played.append(file)
            if now_played == file:
                f=h


    if f >= h:
        f = 0
        print("ulang")
    music_path = os.path.join(folder, save_played[f])
    os.startfile(music_path)
    with open("now_played.txt", 'w') as file_played:
        file_played.write(save_played[f])
