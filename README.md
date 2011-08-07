Python implementation of the [Caylus](http://en.wikipedia.org/wiki/Caylus) board game. Includes web-based multiplayer using the Tornado server.

Installation
=============

All modules needed, including Tornado, are included in the repository.

To run the server, run `python server.py`. The default port is 8080, and can be changed in server.py.

Playing
========

Open `localhost:8080` and wait for the Connect dialog to open. To create a new game, check the "Create" box, enter an arbitrary game ID, and enter the number of players (2-5; 1 is supported for testing purposes but there are no special "solo play" rules) in the "Player" box. To join leave the create box unchecked, enter the same game ID, and enter the player number to connect as in the "Player" box (zero-indexed, so player 1 = "0", player 2 = "1", etc).

Rules
------
See the official [Caylus rules](http://www.ystari.com/caylus/Caylus72E.pdf).

Notation
----------

The game identifies buildings and actions using a consistent notation. Here are some examples:

Resources:

* `<number>`: a certain number of deniers
* `F, W, S, C, G`: food, wood, stone, cloth, gold respectively
* `R`: any resource
* `P`: points
* `RF`: royal favor

Actions:

* `<resources>`: Produce all of the specified resources
* `<resources>-><resources>`: Convert one set of resources to another
* `<action>/<action>`: Allows selection of one of the actions
* `<resources>->[<actions>]`: Construct a building allowing the specified action with the specified resources
