# cd-history  
Saves history of visited dirs in bash.    
Lets you display and cd into recently visited dirs.  
Works in gui and terminal environments (either gui- or terminal- prompt ).  
Can be installed system wide or just for one user.   

## usage  
* display recent dirs and cd into selected dir:   
* ```cd -- ```  
* display recent dirs with path containing foo and cd into selected dir:   
* ```cd -- foo```	  
* move to last dir:
* ```cd -```  
* only show recent history (terminal only):  
* ```cd show```  

  
## installation  
```bash
git clone https://github.com/vincemann/cd-history
cd cd-history
./install.sh (gui|terminal) (local|system)
```  
