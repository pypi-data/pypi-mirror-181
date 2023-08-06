# win-basic-tools

## Before installing...
This is a some kind of fancy and pythonic way of listing a directory and some aliases.  
Try another compiled program if all you seek is speed (although it is really fast).  
  
Description:  
This repository intends to give some simple commands to Windows cmd.exe (or any other shell).  
(Basically I will put those quick shell programs here)

## Installation

It is intended for the global Python Env.  
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install win-basic-tools

~~~bash
> pip install win-basic-tools
~~~

## Usage

~~~bash
$ win-basic-tools setup
~~~

Run for setting the macros file for your cmd.exe.  
It will create the `.macros.doskey` at your home directory and point it in Registry.  
Alias gives more source control than entry-points, however maybe it will be the choice in the future.  
  
After refreshing your prompt, you can use `ls`, `ll`, `touch`. See `%USERPROFILE%\.macros.doskey` for the list of aliases.  
  
Uninstall: run `win-basic-tools uninstall` before `pip uninstall` for reseting Registry

#### Image

![Aplication exmaple](./example/ll_example.png "Example")


## License

[MIT](https://choosealicense.com/licenses/mit/)
