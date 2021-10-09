# Sprite Extracter On-The-Go
This is an easy GUI (Python based) program that can unpack sprite sheet images (which are in a bundle form packed by texture packer) to separate png images(transparency included) and put them in a folder.
![HeadLabel](https://user-images.githubusercontent.com/89206401/136655387-3a8a7cf4-99ed-4416-bafa-fd0b4bbf9397.png)
<br>You just need the sprite sheet image and the data file(example-.plist files) and then you can use this program to automatically extract all the sprite images in a folder.
<br>HOW TO USE:
<br>1)Download the 'Sprite-Extracter On-The-Go.zip' from the release page. https://github.com/Akascape/Sprite-Extracter-On-The-Go/releases
<br>2)Unzip the 'Sprite Extracter On-The-Go.zip' and run the .py file from there. Make sure that you have all the modules installed.
<br>3)You have to first input the sprite image file(.png) and the main data file in their respective sections.
<br>4)Then just click on the extract button and it will take a few seconds to extract the sprite sheet images.
<br>5)Then check the folder which you will find in the main sprite file's folder.
<br>NOTE:
<br>1)Make sure the base name of both the files are same and they must be in the same directory(any).
<br>2)Please do not paste the main files in the program's folder or else it might get deleted(use that folder to open the program only).
<br>User Interface:
<br>![image](https://user-images.githubusercontent.com/89206401/136655763-ddfb4090-c9cf-4397-bebc-1c5d6a2fff8c.png)
<br>This is a very fast and easy to use program and will be helpful for many game developers who want to change and rebundle their sprite sheet in future. Or you can also use it to get good asset images of games for editing.
<br>(Games using this method have their main files inside their assets folder)
<br>I have tested it many times and it works perfectly (specially with .plist files). It supports plist, xml, json and cocos extensions.
<br>
<br>Modules Used:
<br>1) PIL
<br>2) os
<br>3) tkinter
<br>4) shutil
<br>5) time
<br>6) sys
<br>7) json
<br>8) plistlib
<br>9) xml.etree
<br>
<br>To install the modules, just open cmd and write "pip install module_name".
<br>Just simply run the 'Sprite Extracter On-the-go.py' to enter the GUI. Then just use it as described in the Readme.md
<br>Also make sure you have the project assets too, or else it will not run
<br>Please open an issue if you find any error.
<br>Thanks for visiting! :)
