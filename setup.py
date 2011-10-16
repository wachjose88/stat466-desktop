from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["resources/lang/*", "resources/icons/*"]

setup(name = "Stat466",
    version = "0.2",
    description = "Statistics for Bauernschnapsen",
    author = "Josef Wachtler",
    author_email = "josef.wachtler@gmail.com",
    url = "sourceforge.net/projects/stat466/",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['gui', 'database'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'gui' : files },
    #'runner' is in the root.
    scripts = ["stat466.py"], 
    windows = ["stat466.py"], 
    options={"py2exe": {"skip_archive": True, "includes": ["sip"]}}
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = []     
)  
