# MaeStar
A new Interpreter called "MaeStar".

# Getting Started
This repo contains all related files of a new "interpreter" called *MaeStar*.
Just `git clone` and run. Codefiles and testfiles can be found inside their respective folder.


## Prerequisites
* [Pickle](https://docs.python.org/3/library/pickle.html)
* [PLY](https://www.dabeaz.com/ply/) Library


## Running the tests
Run Main program for quadruples creation.
`python maeStarMain.py`
It will let you choose wich codefile you want to run, codefiles can be found in _codefiles/_
After that, a pickle object will be created with the _*quadruples*_ of the code, the _*variable tables*_ and the _*procedure directory*_.

Run MaeStar for interpreting the code.
`python runMaeStar.py`
This will create the _*virtual machine*_ and process the previous quadruples.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

Thanks to Mariana (Mae), for being an inspiration to me during this project.
