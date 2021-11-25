# cd-history  
  
extends cd by system-wide permanent dir-history stack + let user cd into recently visited dirs and more  
works by aliasing cd with bashfunction that implements features  
  
## features  
* supports gui and terminal based dir selection  
* traverse last dirs:  
* cd -  
* display recent history (always in terminal):  
* cd show 	
* display recent dirs and cd into selected dir:  
* cd --  
* display recent dirs containing word foo and cd into selected dir:   
* cd -- foo	 
  
## install  
./install.sh gui|terminal local|system  
  
## requirements  
* bash  
* python3  
