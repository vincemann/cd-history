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
./install.sh (gui|terminal) (local|system)
```  
