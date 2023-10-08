#Utility.py

class MyUtil():
    def SimpEncrypt(self,text,s):
        result = ""

        # 遍历文本
        for i in range(len(text)):
           char = text[i]

           # 加密大写字符
           if (char.isupper()):
              result += chr((ord(char) + s-65) % 26 + 65)

           # 加密小写字符
           else:
              result += chr((ord(char) + s - 97) % 26 + 97)

        return result

    
    def SimpDecrypt(self,text,s):
        result = ""

        # 遍历文本
        for i in range(len(text)):
           char = text[i]
        
           # 解密大写字符
           if (char.isupper()):
              result += chr((ord(char) - s-65) % 26 + 65)
        
           # 解密小写字符
           else:
              result += chr((ord(char) - s - 97) % 26 + 97)
        
        return result
    
    def get_timestamp(self):
       return
    
    def verify_timestamp(self, timestamp, expire):
       return
    
    def get_client_name(self):
       return "clientA"
    
    def get_ip(self):
       return "127.0.0.1"
       
