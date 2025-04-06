here have 2 part FE/BE 
1. FE
FE use write by vue, use BE to manage user permission
permission
  - admin: have full permission
  - user: with partial permission

FE home page allow sign in, sign up  
after sign, should have side menu on left, and link to feature page, feature in below
- upload ssh key: this is admin only feature, here admin can update ssh key, and give a name
  the ssh key need save to BE database
- server list: this is admin only feature, here admin can edit a server list, incloud site/server name/user/host/ssh key name
  site is a group for server name, site name need unique
  server name in same site need unique, but if different site can duplicate
  user/host is this server config 
  ssh key need select from server saved ssh key file
- permission manage: this is admin only feature, in default all user don't have permission to connect to server
  admin can select user in here, add user allow connect to site/server name  
- connect server: in this feature allow user select server to connect
  user can see all site/server name 
  user need select site from first list, then system will update server name in second list
  then user can click a connect button to connect to server, but before connect, system will check permission on this user
  if don't have permission, system retrun permission deny error to user
  if user have permission, system will open a wen console terminal, and auto login to server

2. BE
BE is user python django framework 
BE need provide feature to support FE feature
- manage user by django
- manage ssh key file
- manage site/server info 
