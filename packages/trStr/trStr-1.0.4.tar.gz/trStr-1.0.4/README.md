Solves the problem of string methods to uppercase/lowercase of 'i, I' characters in Turkish; for upper, lower, capitalize, title methods.

Normal string methods is problematic for Turkish strings as follows:

"Islak".lower() -> "islak" 
"aliler bize geldi".upper() -> "ALILER BIZE GELDI" 

This class solves the problem above

Usage: 

trStr(your_str).lower() 
trStr(your_str).upper() 
trStr(your_str).capitalize() 
trStr(your_str).title()