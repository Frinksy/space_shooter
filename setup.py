import py2app.recipes
import py2app.build_app

from setuptools import find_packages, setup

pkgs = find_packages(".")

class recipe_plugin(object):
    @staticmethod
    def check(py2app_cmd, modulegraph):
        local_packages = pkgs[:]
        local_packages += ['pygame']
        return {
            "packages": local_packages,
        }

py2app.recipes.my_recipe = recipe_plugin

APP = ['game.py']
DATA_FILES = ["./img/asteroids/amed.png", "./img/back.png", "./img/bg5.png", "./img/heart.png", "./img/ship.png", "./img/side_frame.png"]
OPTIONS = {}
OPTIONS.update(
    #iconfile="Icon.icns",
    plist=dict(CFBundleIdentifier='com.adam.adam.fun')
)

setup(
    name="Space Asteroids",
    app=APP,
    data_files=DATA_FILES,
    include_package_data=True,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    packages=pkgs,
    package_data={
        "": ["*.gal" , "*.gif" , "*.html" , "*.jar" , "*.js" , "*.mid" ,
             "*.png" , "*.py" , "*.pyc" , "*.sh" , "*.tmx" , "*.ttf" ,
             # "*.xcf"
        ]
    },
)
