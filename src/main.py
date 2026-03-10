import ctypes
import os
import urllib.request
import json
import datetime
import platform
import re
import subprocess


def get_image_url():
    """Fetch NASA APOD metadata, download today's image, and return local filename."""
    try:
        api_key = "DEMO_KEY"
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())

        if data["media_type"] != "image":
            raise Exception("APOD is not an image today.")

        # APOD may provide an HD URL; fall back to the standard image URL.
        image_url = data["hdurl"] if "hdurl" in data else data["url"]

        # Remove characters invalid on common filesystems.
        image_title = re.sub(r'[\\/*?:"<>|]', "", data["title"])
        image_title = image_title.replace(" ", "_")
        filename = f"{datetime.date.today()}_{image_title}.jpg"

        with urllib.request.urlopen(image_url) as response, open(filename, "wb") as f:
            f.write(response.read())

        return filename

    except Exception as e:
        print(f"Error fetching APOD: {e}")
        return None


def change_wallpaper(image_path):
    """Set desktop wallpaper based on the current operating system/desktop."""
    # Use an absolute path so desktop commands resolve the image correctly.
    image_path = os.path.abspath(image_path)

    match platform.system():
        case "Windows":
            SPI_SETDESKWALLPAPER = 0x0014
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, image_path, 3
            )
        case "Darwin":
            script = f'''osascript -e 'tell application "System Events" to set picture of every desktop to "{image_path}"' '''
            os.system(script)
        case "Linux":
            environment = (os.environ.get("XDG_CURRENT_DESKTOP") or "").lower()

            match environment:
                case _ if "kde" in environment:
                    subprocess.run(
                        ["plasma-apply-wallpaperimage", f"{image_path}"], check=False
                    )
                case _ if "xfce" in environment:
                    subprocess.run(
                        [
                            "xfconf-query",
                            "-c",
                            "xfce4-desktop",
                            "-p",
                            "/backdrop/screen0/monitor0/workspace0/last-image",
                            "-s",
                            f"{image_path}",
                        ],
                        check=False,
                    )
                case _ if "gnome" in environment:
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.background",
                            "picture-uri",
                            f"file://{image_path}",
                        ],
                        check=False,
                    )
                    # Keep GNOME light/dark backgrounds in sync.
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.background",
                            "picture-uri-dark",
                            f"file://{image_path}",
                        ],
                        check=False,
                    )
                case "x-cinnamon":
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.cinnamon.desktop.background",
                            "picture-uri",
                            f"file://{image_path}",
                        ],
                        check=False,
                    )


def main():
    image = get_image_url()
    if image is not None:
        change_wallpaper(image)


if __name__ == "__main__":
    main()
