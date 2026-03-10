import ctypes
import os
import urllib.request
import json
import datetime
import platform



def get_image_url():
    api_key = "DEMO_KEY"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())

    image_url = data["hdurl"] if "hdurl" in data else data["url"]
    image_title = data["title"].replace(" ", "_").replace(":", "_")
    filename = f"{datetime.date.today()}_{image_title}.jpg"

    urllib.request.urlretrieve(image_url, filename) 

    return filename


def change_wallpaper(image_path):
    if platform.system() == "Windows":
        SPI_SETDESKWALLPAPER = 0x0014
        ctypes.wind11.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, image_path, 3
        )
    elif platform.system() == "Darwin":
        script = f'osascript -e "tell application "Finder" to set desktop picture to POSIX file "{image_path}""'
        os.system(script)
    elif platform.system() == "Linux":
        pass


def main():
    pass


if __name__ == "__main__":
    main()
