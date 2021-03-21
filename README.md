# cd-history  
  
extends cd by user-wide permanent history stack + let user cd into recently visited dirs  
  
works by aliasing cd with bashfunction (in /etc/bash.bashrc), that implements those features  
to make the history system-wide
  
## features  
* display recent history with indexes:  
* cd -- 	
* display recent history results containing word foo:  
* cd -- foo	 
* cd into dir from histoty at index 3:  
* cd - 3 	
* display whole history:  
* cd --- 	 
  
## install  
./install.sh   
