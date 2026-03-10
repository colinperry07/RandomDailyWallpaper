# RandomDailyWallpaper

## What it does
Fetches NASA's Astronomy Picture of the Day (APOD) and automatically sets it as your desktop wallpaper across Windows, macOS, and Linux.

## Why it exists
To provide an easy, cross-platform way to keep your desktop fresh with stunning daily astronomy imagery without manual intervention.

## How to run it

- Clone the repository to a folder of choice:
`git clone https://github.com/colinperry07/RandomDailyWallpaper`

### Windows
- Open **Task Scheduler** and click **Create Task**
- In the **General** tab, give your task a name (i.e. WallpaperChanger)
- Under **Triggers**, click **New** -> Set to "Daily" and choose the time. (midnight recommended)
- In the **Actions** tab, click **New** -> Set:
    - *Program/Script*: Path to Python (e.g. C:\Python39\python.exe)
    - *Add arguments*: Path to the script (e.g. C:\scripts\src\main.py)
    - *Start in*: Directory containing the script
- Optional: Check "Wake the computer to run this task" to run even if the system is asleep.

### Linux/MacOS
- Open the crontab editor `crontab -e`
- Add a line to run the script at a specific time (@daily recommended, runs once at 12:00AM):
`@daily \path\to\python3 \path\to\script.py`
- Write the changes to crontab editor and exit (Ctrl+O, Ctrl+X)

> **Disclaimer**
DO NOT USE THIS MORE THAN NEEDED, UNLESS YOU USE YOUR OWN API KEY.
THERE IS A DAILY USAGE LIMIT FOR THE DEMO KEY PROVIDED IN THE CODE.
