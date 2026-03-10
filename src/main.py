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
        # Public NASA APOD demo API key (rate-limited).
        api_key = "DEMO_KEY"
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

        # Request APOD JSON payload.
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())

        # APOD can sometimes be a video; only proceed for images.
        if data["media_type"] != "image":
            raise Exception("APOD is not an image today.")

        # Prefer high-resolution image when available.
        image_url = data["hdurl"] if "hdurl" in data else data["url"]

        # Build a filesystem-safe filename from date + APOD title.
        image_title = re.sub(r'[\\/*?:"<>|]', "", data["title"])
        image_title = image_title.replace(" ", "_")
        filename = f"{datetime.date.today()}_{image_title}.jpg"

        # Download and save the image locally.
        with urllib.request.urlopen(image_url) as response, open(filename, "wb") as f:
            f.write(response.read())

        return filename

    except Exception as e:
        # Log error and signal failure to caller.
        print(f"Error fetching APOD: {e}")
        return None


def change_wallpaper(image_path):
    """Set desktop wallpaper based on the current operating system/desktop."""
    # Normalize to absolute path for OS-specific commands.
    image_path = os.path.abspath(image_path)

    if platform.system() == "Windows":
        # Use Windows API to apply wallpaper.
        SPI_SETDESKWALLPAPER = 0x0014
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, image_path, 3
        )

    elif platform.system() == "Darwin":
        # Use AppleScript for macOS desktops.
        script = f'''osascript -e 'tell application "System Events" to set picture of every desktop to "{image_path}"' '''
        os.system(script)

    elif platform.system() == "Linux":
        # Detect active Linux desktop environment.
        environment = (os.environ.get("XDG_CURRENT_DESKTOP") or "").lower()

        if "kde" in environment:
            # KDE Plasma command.
            subprocess.run(
                ["plasma-apply-wallpaperimage", f"{image_path}"], check=False
            )
        elif "xfce" in environment:
            # XFCE desktop property update.
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
        elif "gnome" in environment:
            # GNOME light theme wallpaper.
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
            # GNOME dark theme wallpaper.
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
        elif "cinnamon" in environment:
            # Cinnamon wallpaper setting.
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
    # Download today's APOD image and set it as wallpaper if successful.
    image = get_image_url()
    if image is not None:
        change_wallpaper(image)


if __name__ == "__main__":
    # Run script entry point.
    main()
