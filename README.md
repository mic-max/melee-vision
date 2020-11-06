# Melee Vision

Analyzes Melee gameplay and extracts game information from video

## Resources

# http://tournament-tabler.com/images/char-spritesheet.png
# https://www.spriters-resource.com/gamecube/ssbm/sheet/1593/
# https://www.spriters-resource.com/gamecube/ssbm/sheet/46039/
# https://www.spriters-resource.com/gamecube/ssbm/sheet/1602/

## Moves

Guess what moves a player has done by storing a collection of moves with their damage ranges, including their ability to stale.

## Audio

Can some information be learned from the games sound and music. Stage selected, moves being used, type of KO.

## Game Boundaries

Find "Go!" and "Game!" splashes, or assume start of game is 08:00 00 and that the end is when several frames have passed and the timer stayed the same value.

## Improve Guessing Accuracy

Make sure the crops are good, damages with 1 need to be fixed for sure

1. Run program and get all guesses in a folder
1. Move incorrect guesses to their proper folder
1. Now we have folders that correctly identify their contents.
1. Run each file through the similarity function to determine how closely it matches the options.


## Load Computed Hashed from Database

[sqlite python](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)
Have the program load all precomputed data from the database. This should improve startup time, and reduce disk requirements.
All programs can load from the same database as well to stay in sync.
