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
- **G:** switches inventory item [will update]
- **B:** eat!! [will update]
- **X:** closes notification
- **SHIFT:** turns you into forest gump
- **ENTER:** (near bed) sleep
  
[shop]
- **ENTER:** (near merchant) go into shop
- **arrows:** move up and down
- **X:** purchase
- **S:** sell
- **ESC:** exit shop

[pause menu]
- **ENTER:** to execute the options listed
- **arrows:** move up and down
  
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
- **3.15** notifications!!!
- **3.21** updated pause menu UI
- **3.22** pause menu: save works!
- **3.22** pause menu: load works!
- **3.22** updated shop UI + added seperate buy/sell options for all items

 ## bugs
- tree apples on empty trees displaying when day resets
- hoe should not be able to make a tile on tiles that are already created
- ~~hoe sounds anytime it is used - needs to be only when tile is placed~~ [fixed!]
- ~~seeds plant anywhere [not visably] and deduct from inventory~~ [fixed!]
- remove buy/sell text next to items in shop

## future updates:
- UI
  - inventory bar - this will allow user to go through the bar to select tool, seed, item
  - day/clock/season area
  - needs bars + add more needs
  - character ui - maybe similiar to sims style
  - ~~pause menu~~ [done!]
- map!!
- NPCs
- enemies
- moodlets??
- mailbox/phones/computer - jobs
- user settings [sounds, screen size, more]
- save/load game
- pause menu
  - ~~pauses game~~ [done!]
  - save game
    - work on which data is being saved
    - seperate pause and game manager data
  - load game
  - new game
  - settings
      - settings front+backend
- ~~clock/time~~ [done!]

[[asset pack](https://cupnooble.itch.io/)]


 <img src="https://cdn.discordapp.com/attachments/580110807367418010/1218248233390702633/image.png?ex=6606f914&is=65f48414&hm=ac2446bed55098e37f61fdb7f1dba4cf81e8307a55b693f36c504916856def91&">
