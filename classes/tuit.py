class Tuit:
    #usario,texto,idt,num_rt,peso,fecha
    def __init__(self, user, text, idt,numRT,weight,date_created):
        self.user = user
        self.text = text
        self.idt = idt
        self.num_RT=numRT
        self.weight=weight
        self.date_created=date_created
        

        

    def toString(self):
        return str("Usuario: " + self.user + " Text: " + self.text)

    def getText(self):
        return str(self.text)

    def getIdt(self):
        return self.idt
    
    def getAuthor(self):
        return self.user
    
    def getNumRT(self):
        return self.num_RT
        
    def getWeight(self):
        return self.weight
        
    def getDateCreated(self):
        return self.date_created
        
