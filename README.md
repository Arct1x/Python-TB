# Python-TB


This is a Python Trigger Bot for Valorant but its an external so it can work with any shooter games that has a (perferabbly) enemy outline, you may need to edit the code (ITS OPEN SOURCE), you may need to bind your firing key to L or you may edit it to work with other games.

Basically works by looking at a certain Pixel FOV around your mouse currsor (which in shooter games, remains in the center), and puts the colors found witin the FOV in a a list, that list is checked and if there is a detected color, then it starts a specified action. I will not be responsible for huge changes but if you are trying to fix it, i think you can make a pull request

I did use AI on a part of this because of the math for comparing the Color to Target Color in RGB Form



You need a few packages before you can start.

Run the following:
...> Pip install pyautogui
...> Pip install pynput
...> Pip install Pillow

Run the code either from source or using a source code ediotr such as VSC. Do not expect it to work :(
