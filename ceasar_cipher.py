def encode(text,shift):
    string = []
    for i in text:
        if(i == " "):
            string.append(" ")
        elif(i.isupper()):                
            code = ((ord(i)-65)-int(shift))%26
            char = chr(code+65)
            string.append(char)
        else:
            code = ((ord(i)-97)+int(shift))%26
            char = chr(code+97)
            string.append(char)
    return string

def decode(text,shift):
    string = []
    for i in text:
        if(i == " "):
            string.append(" ")
        elif(i.isupper()):
            code = ((ord(i)-65)+int(shift))%26
            char = chr(code+65)
            string.append(char)
        else:
            code = ((ord(i)-97)-int(shift))%26
            char = chr(code+97)
            string.append(char)
    return string