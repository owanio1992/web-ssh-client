this repo is a nomorepo
here have 2 project fe/be 
1. FE, all source code in fe/ folder
FE use write by vue, use BE to manage user permission
permission
  - admin: have full permission
  - user: with partial permission

FE home page allow sign in, sign up  
after sign, should have side menu on left, and link to feature page, feature in below
- manage ssh keys: this is admin only feature, here admin can update ssh key, and give a name
  the ssh key need save to BE database
- manage servers: this is admin only feature, here admin can edit a server list, incloud site/server name/user/host/ssh key name
  site is a group for server name, site name need unique
  server name in same site need unique, but if different site can duplicate
  user/host is this server config 
  ssh key need select from server saved ssh key file
- permission manage: this is admin only feature, in default all user don't have permission to connect to server
  this permission use Role-Based Access Control
  admin can select user to a role, then add role allow connect to site/server name  
- connect server: in this feature allow user select server to connect
  this feature implement by Xterm.js
  user can see all site/server name 
  user need select site from first list, then system will update server name in second list
  then user can click a connect button to connect to server, but before connect, system will check permission on this user
  if don't have permission, system retrun permission deny error to user
  if user have permission, system will open a web console terminal in new browser tab, the title should naming by "<site>-<server name>"
  when browser tab opened, console should auto login to server

2. BE, all source code in be/ folder
BE is user python django framework 
BE need provide feature to support FE feature
- manage user by django
- manage ssh key file
- manage site/server info 
