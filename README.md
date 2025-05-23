# Blacklisted Group Scanner

The Blacklisted Group Scanner is intended and preconfigured to scan for members of CreepySins' SCPF who are in blacklisted [Groups of Interest](https://trello.com/b/alydkLVe/dea-group-of-interest-database). It functions by searching the groups of all members of CreepySins' SCPF that are of the provided ranks.

**DISCLAIMERS:**
- The speed of this application heavily depends on your internet connection and Roblox API rate limiting.
- Results will only be displayed in the terminal *after* the application searches through all of the ranks it was told to. These results are not saved anywhere and will not be accessible if a fatal error occurs.
- It could take around a couple hours just to search all users ranked L-0 through L-5 given the large size of the group, so reduce the search size in the code if needed.
- The application is not very user friendly and there is no real interface. All parameters must be changed in the code, however I made things accessible via global variables at the top of the Python file.

The code might be sloppy, I made this when I was tired.

\- robot2600

## Installation / Usage
The instructions will be for the Windows Command Prompt because I can't be bothered to do it for anything else. This part covers basic things, but you'll still need to have Python installed and configured already.

1. Navigate to the folder that the program is in.
```bash
cd /file/path/to/project
```

2. Create a Python virtual environment.
```bash
python3 -m venv venv
```

3. Activate the virtual environment.
```bash
venv\Scripts\activate
```

4. Install dependencies. There is only one (httpx), which is needed to make the Roblox API calls.
```bash
pip install -r requirements.txt
```

5. Run the Python script.
```bash
python blacklisted-group-scanner.py
```

6. When done, deactivate your virtual environment. Next time you use the program, repeat the steps EXCEPT for step 2 and 4.
```bash
deactivate
```

## Updates
I won't be updating the app unless someone asks because I doubt anyone will use it anyways (lol). If the list of blacklisted groups updates, just edit the global dictionary `BLACKLISTED_GROUPS` based on the format.
