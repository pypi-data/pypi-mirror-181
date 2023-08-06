
from tesla.router import Path
from . import views

# your urls path should be here


patterns = [
    Path('', views.index, name='index'),
    Path('login', views.login, name='login'),
    Path('logout', views.logout, name='logout'),
    Path('register', views.register, name='register'),
    Path('reset-password', views.reset_password, name='reset-password'),
    Path('collections', views.collection, name='collections')
    
    
    
    
    
]
                  