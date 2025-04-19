# describe
This is a web SSH client project that helps users quickly connect to servers via the SSH protocol
Users can select a server from a list  
and the system will provide a web SSH console to connect to the client without additional configuration.

## Authentication

user can't self-register, please ask admin to create account

## manage account 
### create admin account
if no any admin account (inital state)
in be,exec
```
uv run manage.py createsuperuser
```

login to django admin page 
<host>/admin/

create group: admin
add user to admin group


if want add more admin account 
just add user to admin group

### create user account
use admin account 
login to django admin page 
<host>/admin/

create user 
and give "First name", "Last name"



## Manage SSH Keys

in here can add /remove sshkey


## Manage Servers
in here can add /remove Servers

## Manage Permissions
user can connect to which 
