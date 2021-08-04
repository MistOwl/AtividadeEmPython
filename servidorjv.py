#Jader Maciel dos Santos Cruz
import Pyro4
import os
from colorama import Fore,Back,Style

@Pyro4.expose #dar acesso ao cliente
class jogodavelha:
    NumeroDeTurnos = 0 #Para calcular o número de turnos até que atinja o máximo (VELHA)
    MaxDeTurnos = 9 #máximo de turnos para dar velha
    TurnoDoJogador = 1 #verifica de quem é turno
    Vitorioso = 0 #de 0 a 3, 0 = em andamento, 1 = jogador 1 vitorioso, 2 = jogador 2 vitorioso, 3 = Velha
    #jogador1online = False #verifica se jogador está conectado para partida
    #jogador2online = False #verifica se jogador está conectado para partida
    partidacriada = 1 #verifica se a partida está em andamento
    jogador1 = None #o proxy de cada jogador
    jogador2 = None
    Revanche1 = 1 #Checar se haverá revanche
    Revanche2 = 1 

    velha=[
        [" "," "," "],
        [" "," "," "],
        [" "," "," "]
    ]
    
    def registrarparapartida(self, nomedojogador):#é necessário usar self para ser instancia e partida criada = partida criada para ser um parametro default já que o cliente não passará parametros
        if self.jogador1 == None: #Se jogador 1 ainda não tiver registrado
            self.jogador1 = Pyro4.Proxy(ns.lookup(nomedojogador)) #registra o jogador
            print(self.jogador1)
            self.Revanche1 = 1
            if self.jogador2!= None:
                self.partidacriada = 0
            return "Registrado como jogador 1, solicite o ingresso do jogador 2 para ativar o jogo"
        
        elif self.jogador2 == None: #Se o jogador 2 já estiver registrado e depois a mesma coisa
            self.jogador2 = Pyro4.Proxy(ns.lookup(nomedojogador))
            self.Revanche2 = 1
            if self.jogador1!= None:
                self.partidacriada = 0
            return "Registrado como jogador 2, solicite o ingresso do jogador 1 para ativar o jogo"
            
        #Se ambos já foram registrados e alguem pediu para registrar novamente (cancela o jogo e pede para que ambos realizem o registro novamente)
       
        return "Ambos jogadores já foram registrados, partida já em andamento ou pronta para ser iniciada"

    def iniciarpartida(self):
        if self.jogador1 != None and self.jogador2 != None and self.partidacriada == False: #Se tiver jogador 1 e 2 e a partida não tiver sido criada ainda
            self.partidacriada = True #marque a criação dela
            self.NumeroDeTurnos = 0 #faça o número de turnos ser 0
            self.TurnoDoJogador = 1 #faça ser o turno do primeiro jogador
            self.zerarTabuleiro() #deixa o tabuleiro todo em branco
            self.Vitorioso == 0 #reseta o vencedor
            while self.Vitorioso == 0 and self.NumeroDeTurnos != self.MaxDeTurnos: #enquanto não houver vitorioso e o número de turnos não for estrapolado
                self.tabuleiro()
                self.verificarVitoria()
                self.NumeroDeTurnos += 1
                print(self.NumeroDeTurnos)
            if self.NumeroDeTurnos == self.MaxDeTurnos and self.Vitorioso == 0: #Se chegamos ao máximo de turnos 
                self.Vitorioso = 3
            if self.Vitorioso == 1: 
                self.Revanche1 = int(self.jogador1.resultado(1,self.velha,self.NumeroDeTurnos))    #resultados : 1 = Vitória | 2 = Derrota | 3 = Velha
                self.Revanche2 = int(self.jogador2.resultado(2,self.velha,self.NumeroDeTurnos))
            elif self.Vitorioso == 2:
                self.Revanche1 = int(self.jogador1.resultado(2,self.velha,self.NumeroDeTurnos))    #resultados : 1 = Vitória | 2 = Derrota | 3 = Velha
                self.Revanche2 = int(self.jogador2.resultado(1,self.velha,self.NumeroDeTurnos))
            else:
                self.Revanche1 = int(self.jogador1.resultado(3,self.velha,self.NumeroDeTurnos))    #resultados : 1 = Vitória | 2 = Derrota | 3 = Velha
                self.Revanche2 = int(self.jogador2.resultado(3,self.velha,self.NumeroDeTurnos))                         
            self.partidacriada = 1
            return self.velha
    
    def tabuleiro(self):
        if self.TurnoDoJogador == 1:
            print("Turno do jogador 1")
            self.velha = self.jogador1.realizarjogada(self.velha, self.NumeroDeTurnos,1)
            self.TurnoDoJogador = 2

        else: 
            print("turno do jogador2")
            self.velha = self.jogador2.realizarjogada(self.velha, self.NumeroDeTurnos,2)
            self.TurnoDoJogador = 1

    def zerarTabuleiro(self):
        for i in range(0, len(self.velha)):
            for j in range(0, len(self.velha[0])):
                self.velha[i][j] = " "           
    
    def verificarVitoria(self):
        self.Vitorioso = 0
        if ((self.velha[0][0] == self.velha[0][1] == self.velha[0][2] == "X") or (self.velha[1][0] == self.velha[1][1] == self.velha[1][2] == "X") or (self.velha[2][0] == self.velha[2][1] == self.velha[2][2] == "X") or (self.velha[0][0] == self.velha[1][0] == self.velha[2][0] == "X") or (self.velha[0][1] == self.velha[1][1] == self.velha[2][1] == "X") or (self.velha[0][2] == self.velha[1][2] == self.velha[2][2] == "X") or (self.velha[0][0] == self.velha[1][1] == self.velha[2][2] == "X") or (self.velha[0][2] == self.velha[1][1] == self.velha[2][0] == "X")):
            self.Vitorioso = 1   
        elif ((self.velha[0][0] == self.velha[0][1] == self.velha[0][2] == "O") or (self.velha[1][0] == self.velha[1][1] == self.velha[1][2] == "O") or (self.velha[2][0] == self.velha[2][1] == self.velha[2][2] == "O") or (self.velha[0][0] == self.velha[1][0] == self.velha[2][0] == "O") or (self.velha[0][1] == self.velha[1][1] == self.velha[2][1] == "O") or (self.velha[0][2] == self.velha[1][2] == self.velha[2][2] == "O") or (self.velha[0][0] == self.velha[1][1] == self.velha[2][2] == "O") or (self.velha[0][2] == self.velha[1][1] == self.velha[2][0] == "O")):
            self.Vitorioso = 2
        return self.Vitorioso

    def desconectarPartida(self,jogadorQueChamou):
        if jogadorQueChamou == 1:
            self.jogador1 = None
            self.jogador2.desconectar()
            self.jogador2 = None
        else:
            self.jogador2 = None
            self.jogador1.desconectar()
            self.jogador1 = None    
    def verificarpartida(self):
        return self.partidacriada

daemon = Pyro4.Daemon() #criando o Daemon
thisJogodavelha = jogodavelha()
uri = daemon.register(thisJogodavelha) #criando o identificador uniforme de recurso
ns = Pyro4.locateNS() #servidorDeNomes
ns.register('jogodavelha', uri) #registrando o recurso no servidor de nomes
print(uri)

daemon.requestLoop(thisJogodavelha.verificarpartida) #pedido de loop em background
print("funcionou")
while(thisJogodavelha.Revanche1 and thisJogodavelha.Revanche2):
    thisJogodavelha.iniciarpartida()
daemon.requestLoop(thisJogodavelha.verificarpartida)