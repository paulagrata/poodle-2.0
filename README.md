# poodle 2.0
[WIP]

## description:
a Stardew Valley-inspired RPG, featuring farming, foraging, day-night cycles, weather effects, and a merchant system. Utilizing Tiled for expandability, the game encompasses intricate mechanics such as player movement, tool usage, plant seeding, harvesting, and inventory management. With detailed graphics, dynamic animations, and interactive elements including collisions and particle effects, players embark on a journey filled with challenges, exploration, and commerce.

tutorial version: [[github](https://github.com/paulagrata/poodle/)]

## need: 
- pygame
- pytmx

## install:
- `pip install pygame`
- `pip install pytmx`

## instructions: 
1. install dependencies
2. open `poodle/code` folder
3. run program `python poodle.py`

## keys
[gameplay]
- **ESC:** pause
- **WASD/arrows:** move around
- **SPACE:** use tool
- **F:** plant seed
- **Q:** switches tools
- **E:** switches seeds
- **G:** switches invetory item [will update]
- **B:** eat!! [will update]
- **SHIFT:** turns you into forest gump
- **ENTER:** (near bed) sleep
  
[shop]
- **ENTER:** (near merchant) go into shop
- **arrows:** move up and down
- **SPACE:** purchase/sell
- **ESC:** exit shop
  
[cheats]
- you must figure that out :-)


## current implementations:
- **3.5** shop displays buy items as seeds
- **3.5** shop displays item price and inventory amount
- **3.5** shop pauses sky transition
- **3.6** clock backend + frontend [needs updating]
- **3.6** clock will pause when using shop
- **3.7** clock starts at 10am + stops at 3am, resets upon sleeping
- **3.8** fixed seeds, will place only when at soil + removes from inventory
- **3.8** health/energy backend + frontend
- **3.13** pause menu! successfully pauses the game. [still need needs paused]
- **3.13** need cheat! will reset needs to full amount
- **3.13** added running feature
- **3.13** day # displays
- **3.14** needs pause!
- **3.14** updated needs/stats to go with in-game time
- **3.14** updated some of the UI :D
- **3.14** added inventory items to UI, displays item and amount of item
- **3.14** can go sort through inventory items with G
- **3.14** added energy depletion per axe/hoe/watering
- **3.14** updated sounds to only occur when action takes place [hoe, water]
- **3.15** poodle can now eat [which gains health]

 ## bugs
- tree apples on empty trees displaying when day resets
- hoe should not be able to make a tile on tiles that are already created
- ~~hoe sounds anytime it is used - needs to be only when tile is placed~~ [fixed!]
- ~~seeds plant anywhere [not visably] and deduct from inventory~~ [fixed!]

## future updates:
- UI
  - inventory bar - this will allow user to go through the bar to select tool, seed, item
  - day/clock/season area
  - needs bars + add more needs
  - character ui - maybe similiar to sims style
  - pause menu
- map!!
- NPCs
- enemies
- moodlets??
- mailbox/phones/computer - jobs
- user settings [sounds, screen size, more]
- save/load game
- ~~pause menu~~ [backend done!]
- ~~clock/time~~ [done!]

[[asset pack](https://cupnooble.itch.io/)]


 <img src="https://cdn.discordapp.com/attachments/554140257441021972/1210663481410588692/image.png?ex=65eb613b&is=65d8ec3b&hm=f3297f3a8dfbd7b08ef514e7ee7326406ceea3fe10ed47e2a588033467489c2d&">
