# cd-history  
Keeps track of all visited dirs in bash.    
You can display recently visited dirs and cd into them.  
Works in gui and terminal environments and can be installed system wide or locally just for one user.   

![demo](demo.gif)

## usage  
* display recent dirs and cd into selected dir:   
 ```cd -- ```  
* display recent dirs with path containing 'foo' and cd into selected dir:   
 ```cd -- foo```	  
* traverse dir history:  
 ```cd -|+```  

***env vars with examples***  
Note that some of these are set by the install script in your bashrc  
- gui or terminal mode    
 ```CD_HIST_MODE=gui```  
- how many results to display  
 ```CD_HIST_RESULTS=25```  
- how many dirs to scan at most  
 ```CD_HIST_MAX_SCANNED=-1```  
- where to store the history  
 ```CD_HIST_FILE=/home/user/.cd_history```  

## installation  
```bash
git clone https://github.com/vincemann/cd-history
cd cd-history
./install.sh gui|terminal local|system
```
## uninstall  
```bash
./uninstall.sh local|system
```
  
## how it works  
The install script modifies your bashrc (either ```~/.bashrc``` or ```/etc/bash.bashrc```) and inserts an alias for cd to a bash function.  
This bash function is executed when typing ```cd```. This bash function executes a python script, that will save all dirs you visited in 
```~/.cd_history``` or ```/opt/.cd_history``` depending on installation scope.  
A backup of your bashrc is stored at ```~/.cd-history-backup```.  

## tip  
install fuzzy finder and add this in your bashrc  
```alias c='cd $(cd-history --action=show --mode=terminal --results=1000 | fzf --tiebreak=index)'```  
press c in terminal and navigate fast with fuzzy search function  
