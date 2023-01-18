# About
Wargames is a small project to track passwords and 
solutions to the various different games from 
[overthewire]([https://overthewire.org/wargames/).

Wargames is a Command Line Interface (CLI) application 
and provides simple management for credentials storage.

### Database
Wargames uses a filesystem for storage. The structure is as such:

```
database/
    ├── bandit/
    │   ├── level_0
    │   ├── level_1
    │   ...
    │   └── level_12
    │
    ├── ...(other games).../
    │
    └── leviathan/
        ├── level_0
        └── level_1
```
Each game has its own subdirectory. By default, none are created. 
Users can add new games to the database using the `start` command:

```>> wargames start <game-name>```

When you solve a level, save the password with:


```
>> wargames add [game] level passwd [-d details]
```
Example:
```
>> wargames add 1 password -d "Here's some details"
Saved password 'password' to bandit/level_1
```

If you do not specify a game, it will use the value saved in the 
`database/_WARGAMES_CURRENT_GAME` file, which is by default `bandit`.

To see for which levels you have registered solutions, use:

```
>> wargames list [game]
``` 
Example:
```
>> wargames list leviathan
leviathan/
    ├── level_0
    └── level_1
```

To see the solution for a given level, use `peek`, optionally 
adding the `-d` flag for the details:

```>> wargames peek [game] level [-d]```
Example:
```
>> wargames peek bandit 1
Password: 'password'

>> wargames peek bandit 1 -d
Password: 'password'
Details: Here's some details 
```
