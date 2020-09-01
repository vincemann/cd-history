# cd-history  
  
extends cd by systemwide history stack + let user cd into recently visited dirs  
works by aliasing cd with bashfunction, that implements those features  

## features  
  
* display recent history with indexes with:  
* cd -- 	
* cd into dir from histoty at index 3 with:  
* cd -3 	
* display whole history with:  
* cd --- 	 
  
## install  
run install.sh   
this will append the alias config + bash function to your system wide /etc/bash.bashrc  
changes will take place after restarting of terminal  
