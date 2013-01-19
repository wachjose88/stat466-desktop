from distutils.core import setup

files = ["resources/lang/*", "resources/icons/*"]

setup(name = "Stat466",
    version = "0.2",
    description = "Statistics for Bauernschnapsen",
    author = "Josef Wachtler",
    author_email = "josef.wachtler@gmail.com",
    url = "https://github.com/wachjose88/stat466-desktop",
    
    packages = ['gui', 'database'], 
    
    package_data = {'gui' : files },
    
    scripts = ["stat466.py"], 
)  
