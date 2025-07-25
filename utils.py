import yaml
import os
import time


def load_yml(filename:str):
    with open(filename) as f:
        return yaml.full_load(f)


def delete_caches(filepath: str):
    for file in os.listdir(filepath):
        if file.split("-")[0] != time.strftime("%Y.%m.%d"):
            os.remove(f"{filepath}/{file}")

def open_folder(path: str):
    os.system(f'open {path}')

def http_respons(status_code: int) -> str:
    match status_code:
        case s if 200 <= s < 300:
            return f"Siker ({s})."
        case 400:
            return "Hibás kérés (400). Ellenőrizd az adatokat."
        case 401:
            return "Jogosulatlan (401). Jelentkezz be.\nValószinűleg hibás az accestoken.\nEllenőrizd a beállításokban!"
        case 403:
            return "Tiltott (403). Nincs jogosultságod."
        case 404:
            return "Nem található (404). Ellenőrizd a címet."
        case c if 400 <= c < 500:
            return f"Kliens hiba ({c}). Ellenőrizd a kérést."
        case s if 500 <= s < 600:
            return f"Szerver hiba ({s}). Próbáld újra később."
        case _:
            return f"Hiba ({status_code})."

def time_format(time_:str) -> str:
    s = time_.split("T")[0].split("-")

    return f"{s[1]}.{s[2]}"


def calc_duration(dur:str) -> str:
    duration = ""
    cleared = float(dur[dur.find("T")+1:dur.find("S")])
    hours = int(cleared // 3600)
    def add_zero(x):
        return f"0{x}"
    if hours != 0:
        duration += str(hours)
        minutes = str(int((cleared - 3600*hours)//60))
        seconds = str(int(cleared - ((hours*3600)+(int(minutes)*60))))

        if int(minutes) < 10:
            minutes = add_zero(minutes)
        if int(seconds) < 10:
            seconds = add_zero(seconds)
        return f"{hours}:{minutes}:{seconds}"
    else:
        minutes =str(int(cleared //60))
        seconds = str(int(cleared - 60*int(minutes)))
        if int(minutes) < 10:
            minutes = add_zero(minutes)
        if int(seconds) < 10:
            seconds = add_zero(seconds)

        return f"{minutes}:{seconds}"

def ap_calc_duration(dur:str) -> str:
    duration = ""
    cleared = float(dur[dur.find("T")+1:dur.find("S")])
    hours = int(cleared // 3600)
    def add_zero(x):
        return f"0{x}"
    if hours != 0:
        duration += str(hours)
        minutes = str(int((cleared - 3600*hours)//60))
        seconds = str(int(cleared - ((hours*3600)+(int(minutes)*60))))

        if int(minutes) < 10:
            minutes = add_zero(minutes)
        if int(seconds) < 10:
            seconds = add_zero(seconds)
        return f"{hours}{minutes}{seconds}"
    else:
        minutes =str(int(cleared //60))
        seconds = str(int(cleared - 60*int(minutes)))
        if int(minutes) < 10:
            minutes = add_zero(minutes)
        if int(seconds) < 10:
            seconds = add_zero(seconds)

        return f"{minutes}{seconds}"




def calc_distance(dis: str)-> str:
    return str(round(float(dis)/1000,2))


def calc_altitude(alt_data:list)-> str:
    ascent = 0
    for i in range(len(alt_data) - 1):
        if (alt_data[i + 1] > alt_data[i]) and alt_data[i] != 0:
            ascent += alt_data[i + 1] - alt_data[i]
    return str(int(ascent))


def time_split(time_:str) -> List[str]:
    s = time_.split("T")
    date = s[0].split("-")
    year = date[0]
    month = date[1]
    day = date[2]
    if int(s[1].split(":")[1]) > 55:
        hour = str(int(s[1].split(":")[0])+1)
    else:
        hour = s[1].split(":")[0]

    if int(hour) < 13:
        hour = f"{int(hour)} AM"
    else:
        hour = f"{int(hour)-12} PM"

    return year, month, day, hour


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
