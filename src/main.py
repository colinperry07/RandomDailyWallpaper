import ctypes
import os
import urllib.request
import json
import datetime
import platform
import re


def get_image_url():
    api_key = "DEMO_KEY"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())

    if data != "image":
        raise Exception("AOPD is not an image today.")

    image_url = data["hdurl"] if "hdurl" in data else data["url"]
    image_title = re.sub(r'\\/*?:"<>|]', "", data["title"])
    image_title = image_title.replace(" ", "_")
    filename = f"{datetime.date.today()}_{image_title}.jpg"

    urllib.request.urlretrieve(image_url, filename)

    return filename


def change_wallpaper(image_path):

    if platform.system() == "Windows":
        SPI_SETDESKWALLPAPER = 0x0014
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, image_path, 3
        )

    elif platform.system() == "Darwin":
        script = f'''osascript -e 'tell application "System Events" to set picture of every desktop to "{image_path}"' '''
        os.system(script)

    elif platform.system() == "Linux":
        environment = os.environ.get("XDG_CURRENT_DESKTOP").lower()
        
        image_path = os.path.abspath(image_path)

        if "kde" in environment:
            os.system(f"plasma-apply-wallpaperimage {image_path}")
        elif "xfce" in environment:
            os.system(
                f"xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s {image_path}"
            )
        elif "gnome" in environment:
            os.system(
                f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}"
            )
            os.system(
                f'gsettings set org.gnome.desktop.background picture-uri-dark "file://{image_path}"'
            )
        elif "cinnamon" in environment:
            os.system(
                f"gsettings set org.cinnamon.desktop.background picture-uri file://{image_path}"
            )


def main():
    image = get_image_url()
    change_wallpaper(image)


if __name__ == "__main__":
    main()
