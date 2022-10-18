#import sqlite3
from os import system

class console_mode():
    #define valores base da classe
    def __init__(self):
        self.target = "NONE"
        self.mode = "SELECT"
        self.auto_clear = True
            
        #dicionario contendo as funcoes e suas chamadas
        self.mode_list = {"SELECT":self.test()}
        self.base_commands = {"test":self.test}
            
    #inicia o método de console
    def start(self):
        while True:
            #limpa o console
            if self.auto_clear == True: system("cls")
            
            print("Starting console in {} mode for target {}".format(self.mode, self.target))
            
            try:
                #se o texto inseriod pelo usuario for igual ao nome de uma função listade em base_commands, executa-a
                self.base_commands[input("Command:").lower()]()
            except Exception as e:
                print("{} is not a valid command".format(e))
            #para previnir a limpeza indesejada do console
            input("Press enter to continue")
                    
    def test(self):
        print("Console is Working...")

#cria a instancia do console
main_console = console_mode()

main_console.start()