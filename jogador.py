#Jader Maciel dos Santos Cruz
import Pyro4
import os
from colorama import Fore,Back,Style
@Pyro4.expose
class player:
    nome = None
    def registrar(self, identificador_uri,ns):
        try: #tente registrar o nome do jogador
            while True:
                self.nome = input("coloque um nome de usuario: ") #insira o nome do jogador
                try:
                    ns.lookup(self.nome) #procure se já existe registro no servidor de nomes
                    print("jogador ja existente")
                except:
                    ns.register(self.nome,identificador_uri) #se não tiver, registre
                    return self.nome 
        except:
            return "Falha ao registrar"  #se não conseguir registrar, retorne falha ao registrar  
    
    def pedirnome(self): #metodo para que o servidor do tabuleiro solicite o nome para o jogador para que ele possa pedir jogadas
        try:
            return self.nome
        except:
            return "Erro de solicitacao"           
    
    def registarparapartida(self, jogodavelha):
        print(jogodavelha.registrarparapartida(self.nome))

    def imprimirvelha(self, velha,NumeroDeTurnos):
        os.system("cls")
        print("    0   1   2")
        print("0:  "+ velha[0][0] + " | " + velha[0][1] + " | " + velha[0][2])
        print("   -----------")
        print("1:  "+ velha[1][0] + " | " + velha[1][1] + " | " + velha[1][2])
        print("   -----------")
        print("2:  "+ velha[2][0] + " | " + velha[2][1] + " | " + velha[2][2])
        print("   -----------")
        print("Turnos: " + Fore.BLUE + str(NumeroDeTurnos) + Fore.RESET)

    def realizarjogada(self, velha,NumeroDeTurnos, jogador):
        self.imprimirvelha(velha,NumeroDeTurnos) #Chama função de imprimir a velha
        if jogador == 1:
            print(Fore.GREEN + "Você joga com X" + Fore.RESET)
        else:
            print(Fore.GREEN + "Você joga com O" + Fore.RESET)    
        linha = int(input("Escolha a linha a qual deseja jogar: "))
        coluna = int(input("Escolha a coluna a qual deseja jogar: "))
        while velha[linha][coluna]!= " " : #Enquanto não selecionar um espaço em branco
             os.system("cls")
             self.imprimirvelha(velha,NumeroDeTurnos)
             linha = int(input("Escolha a linha a qual deseja jogar: "))
             coluna = int(input("Escolha a coluna a qual deseja jogar: "))
        try:
            if jogador == 1:
                velha[linha][coluna] = "X"
            else:
                velha[linha][coluna] = "O"    
        except:
            print("A casa selecionada foi invalida, seu turno foi pulado")    
        self.imprimirvelha(velha,NumeroDeTurnos)
        print("Outro jogador já está realizando a jogada dele, isso pode levar um tempo")
        return velha            
    
    def resultado(self, resultadodapartida, velha,NumeroDeTurnos):
        if resultadodapartida == 1:
            self.imprimirvelha(velha,NumeroDeTurnos)
            print("Parabens, você venceu")
        elif resultadodapartida == 2:
            self.imprimirvelha(velha,NumeroDeTurnos)
            print("Vai precisar tentar um pouco melhor que isso")
        elif resultadodapartida == 3:
            self.imprimirvelha(velha,NumeroDeTurnos)
            print("Empatou! Finalmente, um oponente digno!")
        return input("insira [1] se deseja uma revanche e [2] deseja sair do servidor: ")         

    def desconectar():
        print("Optaram por não haver revanche. Obrigado por jogar")

thisPlayer = player()
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()  #localizar servidor de nomes
identificador_uri = daemon.register(thisPlayer) #cria identificador para o jogador
thisPlayer.registrar(identificador_uri,ns)



try: 
    
    uri = ns.lookup('jogodavelha') #localiza o identificador do servidor do jogo da velha
    jogodavelha = Pyro4.Proxy(uri) #cria proxy para o servidor do jogo da velha, baseado no identificador
    opt = 1 
    print(jogodavelha.registrarparapartida(thisPlayer.pedirnome()))
    daemon.requestLoop() 

except:
    print("Servidor não conectado")
