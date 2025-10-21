## Quick Install

<details>
<summary>bash</summary>
<br>

```bash
LATEST_VERSION=$(curl -s "https://api.github.com/repos/New9c/OKey/releases/latest" | grep -oP '"tag_name":\s*"\K(.*)(?=")')
# echo "Latest release version: $LATEST_VERSION"
sudo curl -L "https://github.com/New9c/OKey/releases/download/$LATEST_VERSION/OKey" -o /usr/local/bin/OKey
sudo chmod +x /usr/local/bin/OKey
```
</details>

<details>
<summary>fish</summary>
<br>

```fish
set LATEST_VERSION $(curl -s "https://api.github.com/repos/New9c/OKey/releases/latest" | grep -oP '"tag_name":\s*"\K(.*)(?=")')
# echo "Latest release version: $LATEST_VERSION"
sudo curl -L "https://github.com/New9c/OKey/releases/download/$LATEST_VERSION/OKey" -o /usr/local/bin/OKey
sudo chmod +x /usr/local/bin/OKey
```
<details>

## Quick Start
```sh
pip install -r requirements.txt
python OKey.py
```

## Build with pyinstaller
```sh
# In OKey/ directory
pyinstaller --onefile OKey.py
sudo cp dist/OKey /usr/bin/OKey
```
You can now run OKey anywhere c:
