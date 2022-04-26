This script will export windterm session from zoc ini file.

#### zoc Usage
1. export zoc ini file 'HostDirectory.zocini'
2. run script get windterm session
```shell script
python zoc_to_windterm.py |python -m json.tool
```
3. add session text to windterm session file (eg: ~/.wind/profiles/default.v10/terminal/user.sessions)



#### iterm2 Usage
1. export iterm2 json file 'Profiles.json'
2. run script get windterm session
```shell script
python iterm2_to_windterm.py |python -m json.tool
```
3. add session text to windterm session file (eg: ~/.wind/profiles/default.v10/terminal/user.sessions)



#### securecrt Usage
1. export securecrt xml file 'crt.xml'
2. run script get windterm session
```shell script
python securecrt_to_windterm.py |python -m json.tool
```
3. add session text to windterm session file (eg: ~/.wind/profiles/default.v10/terminal/user.sessions)



