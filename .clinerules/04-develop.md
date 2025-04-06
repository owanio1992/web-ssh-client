in this project use moon to manage

```
# init 
moon :init

# (option) migrate, if any schema change
moon be:makemigrations
moon be:migrate

# (option) create superuser
## user: admin
## pass: admin
moon be:createsuperuser

# test
## be listen 8000
## fe listen 8080
moon :dev

# cleanup
moon :purge
```
