# A dwarf-fortress adventure mode-inspired rogue-like Pygame Python3 game
On heavily development, especially the name
https://franchufranchu.itch.io/rogue

## Requirements
	python>=3.0
	autoclass
    pygame
    noise
    dict
All of them can be pip installed

## A chart showing how the classes inherit and contain each other
![alt text](https://raw.githubusercontent.com/FranchuFranchu/silver-rogue-df/master/diagram.png)

## Controls
	Arrow keys: Move
	
## Some clarifications of the code
Volume is measured in liters.
A map tile fits 3 cubic meters or 3k liters

## Tutorial
You are the tiny @ in the middle of the screen
Use the arrow keys to move
Use "rshift + arrow keys" to resize the window
Use "l" to **L**ook
When looking:
- Use "k" to tal**K** 

How to make a human with the command line:
- Enter into look mode and move the cursor to the place where you want to make the human 
- Type "mkhuman" in the command line
- To talk with the human, move the cursor to the place where you put the human and press K



## Editing the tileset
I use GIMP to edit the tileset. Go to Image -> Configure grid and make it 12x12
Make sure View > Show Grid is enabled
There are tiny numbers on the right if you don't want to count from the top
The empty tiles are green, and have a number to get the low half of the position

## Credits
[Tileset author, he hasn't provided any license](https://dwarffortresswiki.org/index.php/User:Alloy)

[I'll assume it's MIT because of the wiki politics](https://dwarffortresswiki.org/index.php/User:Alloy)

I assume this is not a "derivative work" of the tileset because you can change it if you want, correct me and i'll change the license

credits to me for everything else