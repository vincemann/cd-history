# cd-history  
Keeps track of all visited dirs in bash.    
You can display recently visited dirs and cd into them.  
Works in gui and terminal environments and can be installed system wide or locally just for one user.   

![demo](demo.gif)

## usage  
* display recent dirs and cd into selected dir:   
* ```cd -- ```  
* display recent dirs with path containing 'foo' and cd into selected dir:   
* ```cd -- foo```	  
* traverse dir history:
* ```cd -|+```  
  
## installation  
```bash
git clone https://github.com/vincemann/cd-history
cd cd-history
./install.sh gui|terminal local|system
```  
## how it works  
The install script modifies your bashrc (either ```~/.bashrc``` or ```/etc/bash.bashrc```) and inserts an alias for cd to a bash function.  
This bash function is executed when typing ```cd```. This bash function executes a python script, that will save all dirs you visited in 
```~/.cd_history``` or ```/opt/.cd_history``` depending on installation scope.  
