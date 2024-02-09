
#################################################################################
    # sudo fuser -k 8000/tcp    (kill server port 8000)
#################################################################################
'''
1.  su -
2.  sys66$OS
3.  cd /oshome/maheshb/Pipeline_VFX/pms
4.  source os/bin/activate                   ( activate os env)
5.  cd openslate
6.  cd sqlite-autoconf-3240000/
7.  export LD_LIBRARY_PATH=/usr/local/lib
8.  cd ..
9.  python manage.py runserver
'''
#################################################################################
'''
1.  su -
2.  sys66$OS
3.  cd /oshome/maheshb/Pipeline_VFX/pms
4.  source os1/bin/activate                   ( activate os1 env)
5.  cd openslate
6.  python manage.py runserver
'''
#################################################################################
'''
# After os1 activate make changes as below :-
    - settings.py
        1) 'allauth',                             
        2) 'allauth.account',
        3) 'allauth.account.middleware.AccountMiddleware', 

    - user/models.py
        1)  class EmailAddress(models.Model):                                       
                class Meta:
                    app_label = 'allauth'
'''
#################################################################################
'''
# In server machine 192.168.13.2   ( Django project running on 0.0.0.0:8000)

1) In terminal run, python3 pms.py
2) In pms.py file saved command to run django project ( Inside root directory pms.py file saved) 
3) using point 1) project run background also, whenever stop then enter--> ps aux | grep manage.py
4) kill PID

'''

####################################################################################

'''
# In server machine 192.168.13.26   ( Django project running on 0.0.0.0:8000)
1) inside terminal type -->  screen
2) after screen terminal open type --> python3.9 pms.py
3) close screen terminal -->  project run in background
4) whenever close this project enter in terminal --> screen -r  or kill <__id__>
'''

#################################################################################
'''
# Postgre sql start
    1)  sudo systemctl start postgresql
    2)  su - postgres
    3)  psql                         or 
    4)  sudo -u postgres psql

# Postgre sql user ,password & database
    1) user = mahesh
    2) password = test@123
    3) database = os

# Postgre sql user ,password & access to all database
    1) create user mahesh with password 'test@123';
    2) GRANT ALL PRIVILEGES ON database os TO mahesh;
    3) GRANT ALL PRIVILEGES ON SCHEMA public TO mahesh;
    4) GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mahesh;
'''
#################################################################################
'''
# MySQL start
    - systemctl status mysqld
    - systemctl start mysqld
    1) mysql -u root -p 
    2) password = Test@123

# MySQL user,password & database
    1) user = mahesh
    2) password = Test@123    --> Capital letter 
    3) database = os

# Django Superuser
    1) openslate
    2) test@123
'''
####################################################################################
'''
# MongoDB Nosql start
    1) mongo
'''
####################################################################################
'''
# Redis Nosql start
    1) redis-cli     or
    2) redis-cli -h 0.0.0.0 -p 6379
'''
####################################################################################

