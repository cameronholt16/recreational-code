# recreational-code
Code I've written for its own sake

In decreasing order of time investment.

'Code' is a folder containing a chess bot (chess.py) I built from scratch and the images needed to show the board. It has a GUI that shows games and allows users to play moves by tapping squares. The bot's hyperparameters can easily be modified to change its playstyle. It seems to be better than between 5-10% of the active players on chess.com. It would easily beat an absoloute beginner. If the program is run as it is, you will play white against my cpu. Press the square of the piece you would like to move, then the square you would like to move it to, them 'submit move'. Press 'next move' to see the cpu's response, then repeat. Here is the PGN of a game it played against a human. My bot was playing with the white pieces.

1. d4 d5 2. e3 Nc6 3. Bb5 f6 4. Qh5+ g6 5. Qd1 e5 6. Nc3 Be6 7. Nf3 a6 8. Bxc6+
bxc6 9. dxe5 Be7 10. Nd4 Qd7 11. O-O fxe5 12. Bd2 Bf6 13. Nxe6 Qxe6 14. e4 Rb8
15. Qe2 Nh6 16. Bxh6 a5 17. b3 g5 18. Qd3 Rg8 19. Rae1 Kf7 20. Re3 Ra8 21. Rfe1
Rg6 22. exd5 cxd5 23. Qxd5 Qxd5 24. Nxd5 Re8 25. Nxc7 Re7 26. Nd5 Re6 27. Rh3 g4
28. Rh5 Bg7 29. Be3 Rh6 30. Rf5+ Kg6 31. Rg5+ Kf7 32. Rf5+ Bf6 33. Bxh6 a4 34.
bxa4 Rc6 35. Nb4 Rb6 36. Nd5 Rd6 37. Nc7 Rc6 38. Nd5 Rxc2 39. Rxf6+ Ke8 40. Re6+
Kd7 41. R6xe5 Rxa2 42. Nf6+ Kd6 43. Bf8+ Kc7 44. Nd5+ Kc6 45. Rc1+ Kd7 46. Nf6+
Kd8 47. Rd5# 1-0

naughts_and_crosses_ai is a genetic algorithm that learns to play naughts and crosses significantly better than bots playing at random. With the example hyperparameters, its win:loss ratio against a blind bot settles around 2.5:1. It simulates a population playing against itself and reproducing acording to individual success in the game. It is not intended to be the most efficient way to code a naughts and crosses bot.

nnbackprop implements the backpropogation algorithm on an arbitrary neural network.

animation.py simulates and animates charged particles' interractions due to Coulomb's law. It was my 'Hello World' animation.

bombmanual is a tool to play 'Keep Talking and Nobody Explodes', which I play with my younger sister. She reads out letters six at a time and I determine the unique word that can be built from them.
