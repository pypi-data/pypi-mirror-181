class trStr:
    """
    Solves the problem of string methods to uppercase/lowercase the turkish character 'İ,i' and 'I,ı' for upper, lower, capitalize, title methods
    For example strings are converted as: "insan".capitalize() -> "Insan" but in Turkish language it should be converted as "İnsan", this class solves this problem.
    
    Usage: trStr("Bu Benim Cümlem").upper() -> "BU BENİM CÜMLEM"
    
    """
    
    def __init__(self,thestring):
        self.thestring = thestring
        
    def upper(self):
        thestring = self.thestring.replace("i", "İ")
        thestring = thestring.upper()
        return thestring
    
    def lower(self):
        thestring = self.thestring.replace("İ", "i")
        thestring = self.thestring.replace("I", "ı")
        thestring = thestring.lower()
        return thestring
    
    def capitalize(self):
        
        thestring = self.thestring
        
        if thestring[0] == 'i':
            thestring = thestring.replace('i','İ',1)
            
        if thestring[0] == 'ı':
            thestring = thestring.replace('ı','I',1)
            
        thestring = thestring.capitalize()
            
        return thestring
    
    def title(self):
        
        thewords = self.thestring.split()
        emptystring = []
        
        for word in thewords:
            
            if word[0] == 'i':
                word = word.replace('i','İ',1)
                
            emptystring.append(word)
            
        emptystring = " ".join(emptystring)
            
        thenewstring = emptystring.title()
        
        return thenewstring