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
- Check *"Wake the computer to run this task"* to run even if the system is asleep.

### MacOs
- Create a .plist file in your LaunchAgents folder like this:
`~/Library/LaunchAgents/com.user.wallpaper.plist`  
- Put this inside the file:
```<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.wallpaper</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/your/script.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>0</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```
- Save and load it:
`launchctl load ~/Library/LaunchAgents/com.user.wallpaper.plist`

### Linux
- Create a service file in /etc/systemd/system:
```service-file.service
[Unit]
Description=Task Name

[Service]
ExecStart=/path/to/python /path/to/script.py
Type=oneshot
```
- Create a timer file in the same directory
```timer-file.timer
[Unit]
Description=Runs Task Name

[Timer]
OnCalendar=daily
Persistent=true
Unit=service-file.service

[Install]
WantedBy=timers.target
```
- Reload system to recognize new files:
```bash
sudo systemctl daemon-reload
```
- Enable the timer so it starts on boot:
```bash
sudo systemctl enable timer-file.timer
```

> **DISCLAIMER**
THE API KEY PROVIDED IN THE CODE CAN ONLY REQUEST 30 TIMES PER DAY
ANYTHING FURTHER WILL THROW AN ERROR
