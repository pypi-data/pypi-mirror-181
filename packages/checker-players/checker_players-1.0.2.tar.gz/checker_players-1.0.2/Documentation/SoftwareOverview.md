# Software Overview

This document presents an overview of the software in hopes that it will improve code maintainability and improve the developer on-ramping experience.

## File Tree
In the root directory we find some common files such as [.gitignore](https://git-scm.com/docs/gitignore), [LICENSE](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository), [README](https://www.mygreatlearning.com/blog/readme-file/), [requirements](https://learnpython.com/blog/python-requirements-file/), [pyproject](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/). An important note is that we also have a distribution folder (called `dist`) because this code will be made availbile via `pip`. For all intents and purposes, the majority of our work will be found within the `src` folder. In the root directory we also have the folder `Documentation` where we can document our software and general work. This is a good place to include example code, links to educative material, and citations from papers whose ideas we implement.

## src
This is our source folder and should be the only folder in the repository to contain any and all code.

## src/checker_players
This folder is what will be uploaded to pip and will hence carry the majority of our code. In particular you can think of `checker_players` as our packagae or, put differently, all the classes and functions that we would need to train/test/run/instantiate our checkers game with AI checker players.

## src/checker_players/Checker_Environment
This folder contains python files related to our reinforcement learning environment. As it currently stands, this folder should only include the files related to our checker board environment. In the future, we could implement additional games.

## src/checker_players/Interpretters
This folder contains python files which extend `class Interpretter`. Intuitively, the `Interpretter` class is suppose to "re-interpret" a game's state. In the case of checkers, an interpretter would take in an 8 by 8 matrix representing the locations of various pieces on the board, and outputs a the same information under a different structure. This class can largely be thought of as a helper class as different models and reward functions will assume different structures for our game state. As an example, `DoubleColumnInterpretter` maps the 8 by 8 matrix board representation to two lists, where the first contains the positions of all the pieces belonging to player 1, and the second representing the positions of all the pieces belonging to player 2.

## src/checker_players/Players
This folder contains files which extend `class Player`. Intuitively, the `Player` class is suppose to be our AI checker players and hence all they have to implement is a `play` and `learn` function.

## src/checker_players/Runners
TODO: not done writing documentation. However in the meantime, these files should "run" our games. We should be able to run our games, collect metrics, and train our  models.

## src/scripts
This folder is where we include the scripts which do not add to the core functionalities of the library. More specifically, I expect this to mainly be populated with python notebooks which will then be loaded in to google collab when we eventually begin to train our models.

## src/test
This folder is to mirror the structure of `src/checker_players` and is used to test the functionalities implemented in `src/checker_players`. In general, if there is some functionality we have implemented, for example the AI player who plays randomly as implemented in `src/checker_players/Players/RandomPlayer.py` then we can expect to find a file `src/test/Players/RandomPlayer.py` which tests it's functionality. This insures that our code is always being properly tested, allows us to re-test code after a refactoring or a new feature addition, and allows us to always have example code ready as documentation.