# HonorsProjectCSE231
Plays Two Bots against themselves one random and one with a strategy in the game Dots and Boxes.
It plays with one random player and one strategic player. I did this project for honors credit in CSE231, a introductory 
python course at Michigan State University. The developement of this program happened in two parts. The first part consisted of creating the games logistics, 
setting up the board, the random player, score keeping and such. The second part was all about creating the strategic player, the player plays using the chain 
method a common strategy in this dots and boxes. What this does is it uses boxes that can moved to in succession and leverages those to score many points all 
at once.

More Info On Dots and Boxes, and the chain method: https://en.wikipedia.org/wiki/Dots_and_Boxes

This project was created after gaining about a month and half of coding experience. That said it is not perfect and is quite inefficient at points. It served
as a nice introduction into computer science and garnered a healthy respect on my part for the power of the computer.

IMPORTANT NOTICE FOR TESTING THIS PROJECT:
The project states this when run but remember player B is the strategic player throughout. In multiple play you need to be aware of your board size selection and number of games to play. Be sure to not choose any board length that is exceedingly high as it may result in weird displays of the game and the time to play becoming exceedingly high. I reccomend 4 <= Board Size <= 8 for a good game. In multiple play board size and number of games can greatly effect run time. At a board size of 5, running 10,000 games takes roughly 16 seconds for me, scale accordingly. 
