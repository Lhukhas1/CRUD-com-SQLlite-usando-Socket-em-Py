import socket


class Cliente:
    def __init__(self, host = "127.0.0.1", porta = 50000):
        self.socket_dados = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_dados.connect((host, porta))
        self.fechar = False
    
    def enviarMensagem(self, mensagem):  
        self.socket_dados.send(mensagem)
    

    def desconectar(self):
        if self.socket_dados:
            self.socket_dados.close()
            print("Desconectando")
    

    def executar(self):
        while not self.fechar:  
            try:
                self.CRUD()

                if self.fechar:
                    break

                continuar = input("Nova operação(S/N): ").upper()
                if continuar not in ["SIM", 'S']:
                    break
                    
            except KeyboardInterrupt:
                self.desconectar()
                break
        
        self.desconectar()


    
    def CRUD(self):
        opcao = None
        print("\tSistema CRUD\nDigite: \nC - Criar\nR - Buscar\nU - Update\nD - Deletar\nE - Encerrar")
        while True: 
            opcao = input("opcao: ").upper()
            if opcao not in ['C', 'R', 'U', 'D','E']:
                print("Caracter invalido!")
            elif(opcao == 'E'):
                self.fechar = True
                break
            else:
                break
        
        
        match opcao:
            case 'C':
                mensagem = self.escolhaC()

                self.enviarMensagem(mensagem)

                resposta = self.socket_dados.recv(1).decode("utf-8")

                if resposta == 'T':
                    print("Disciplina adicionada com sucesso!")
                else:
                    print("Erro ao adicionar disciplina!")
                        
            case 'R':
                while True:
                    escolha = input("\t1 - Listar todas\n\t2 - Buscar uma\nOpcao: ")
                    if escolha not in ['1', '2']:
                        print("Escolha invalida!\nNova opcao: ")
                    else:
                        break

                if escolha == '1':
                    # Listar todas
                    mensagem = b'L'
                    self.enviarMensagem(mensagem)
                    resposta = self.socket_dados.recv(1).decode("utf-8")
                    
                    if resposta == 'T':
                        # Receber quantidade
                        quantidade = int.from_bytes(self.socket_dados.recv(2), "big")
                        print(f"{quantidade} disciplinas encontradas:")
                        for i in range(quantidade):
                            resultado = self.processaR(self.socket_dados)
                            print(f"{i + 1}. Codigo: {resultado[0]}")
                            print(f"   Nome: {resultado[1]}")
                            print(f"   Professor: {resultado[2]}")
                            print(f"   Quant Alunos: {resultado[3]}")
                            print(f"   Carga Horaria: {resultado[4]}")
                            print(f"   Media turma: {resultado[5]}\n")
                    else:
                        print("Nenhuma disciplina encontrada!")
                        
                else:
                    # Buscar uma especifica
                    mensagem = self.escolhaR()
                    self.enviarMensagem(mensagem)

                    resposta = self.socket_dados.recv(1).decode("utf-8")
                    
                    if resposta == 'T':
                        resultado = self.processaR(self.socket_dados)
                        print("Disciplina encontrada\n")
                        print(f"Codigo: {resultado[0]}\nNome: {resultado[1]}\nProfessor: {resultado[2]}\nQuant Alunos: {resultado[3]}\nCarga Horaria: {resultado[4]}\nMedia turma: {resultado[5]}\n")
                    else:
                        print("Disciplina nao encontrada!\n")
                        
            case 'U':
                mensagem = self.escolhaU()
                self.enviarMensagem(mensagem)

                resposta = self.socket_dados.recv(1).decode("utf-8")

                if resposta == 'T':
                    print("Disciplina atualizada")
                else:
                    print("Disciplina nao encontrada!")
                        
            case 'D':
                mensagem = self.escolhaD()
                self.enviarMensagem(mensagem)

                resposta = self.socket_dados.recv(1).decode("utf-8")

                if resposta == 'T':
                    print("Disciplina removida com sucesso!")
                else:
                    print("Disciplina nao encontrada!")          
   
    def escolhaC(self):  # Faz o cadastro

        print("\nInforme as informações abaixo:")
        codigo = input("Codigo da disciplina: ").upper()
        nomeDisciplina = input("Nome da Disciplina: ")
        nomeProfessor = input("Nome do Professor: ")
        quantidadeAlunos = int(input("Quant de alunos matriculados: "))
        cargaHoraria = int(input("Carga Horaria: "))
        mediaTurma = float(input("Media de notas da disciplina: "))
        mediaTurma = int(mediaTurma * 100)
    
        # Para fazer menos conversões
        parteConvertida = {}
        parteConvertida[0] = codigo.encode("utf-8")
        parteConvertida[1] = nomeDisciplina.encode("utf-8")
        parteConvertida[2] = nomeProfessor.encode("utf-8")
        
        # Codificar mensagem
        mensagem = b""
        mensagem += 'C'.encode("utf-8")  # opcode
        mensagem += len(parteConvertida[0]).to_bytes(1, "big") + parteConvertida[0]  # codigo
        mensagem += len(parteConvertida[1]).to_bytes(1, "big") + parteConvertida[1]  # nome disciplina
        mensagem += len(parteConvertida[2]).to_bytes(1, "big") + parteConvertida[2]  # nome professor
        mensagem += quantidadeAlunos.to_bytes(1, "big")  # quant alunos
        mensagem += cargaHoraria.to_bytes(1, "big")      # carga horaria
        mensagem += mediaTurma.to_bytes(3, "big")        # media turma

        return mensagem

    def escolhaR(self):  # Buscar disciplina
     
        codigo = input("Qual Codigo da disciplina buscar: ").upper()
        
        codigoBytes = codigo.encode("utf-8")
        mensagem = b""
        mensagem += 'R'.encode("utf-8")  # opcode
        mensagem += len(codigoBytes).to_bytes(1, "big") + codigoBytes  # codigo

        return mensagem
    
    def processaR(self, sock_dados):
        # Codigo
        tam_codigo = int.from_bytes(sock_dados.recv(1), "big")
        codigo = sock_dados.recv(tam_codigo).decode("utf-8")
                        
        # Nome disciplina
        tam_disciplina = int.from_bytes(sock_dados.recv(1), "big")
        nomeDisciplina = sock_dados.recv(tam_disciplina).decode("utf-8")
                        
        # Nome professor
        tam_professor = int.from_bytes(sock_dados.recv(1), "big")
        nomeProfessor = sock_dados.recv(tam_professor).decode("utf-8")
                        
        # Quant de alunos
        quantidadeAlunos = int.from_bytes(sock_dados.recv(1), "big")
                        
        # Carga horaria
        cargaHoraria = int.from_bytes(sock_dados.recv(1), "big")
                        
        # Media da turma
        mediaTurma = float(int.from_bytes(sock_dados.recv(3), "big" )) / 100

        resultado = {}
        resultado[0] = codigo
        resultado[1] = nomeDisciplina
        resultado[2] = nomeProfessor
        resultado[3] = quantidadeAlunos
        resultado[4] = cargaHoraria
        resultado[5] = mediaTurma

        return resultado  

    
    def escolhaU(self):  # Atualizar disciplina
        codigo = input("Qual codigo atualizar: ").upper()

        print("Informe as novas informacoes da disciplina:\n")

        novoCodigo = input("Novo Codigo da disciplina: ").upper()
        nomeDisciplina = input("Nome da Disciplina: ")
        nomeProfessor = input("Nome do Professor: ")
        quantidadeAlunos = int(input("Quant de alunos: "))
        cargaHoraria = int(input("Carga Horaria: "))
        mediaTurma = float(input("Media de notas: "))
        mediaTurma = int(mediaTurma * 100)
        
        # Para fazer menos conversões
        parteConvertida = {}
        parteConvertida[0] = codigo.encode("utf-8")
        parteConvertida[1] = nomeDisciplina.encode("utf-8")
        parteConvertida[2] = nomeProfessor.encode("utf-8")
        parteConvertida[3] = novoCodigo.encode("utf-8")
        
        # Codificar mensagem
        mensagem = b""
        mensagem += 'U'.encode("utf-8")  # opcode
        mensagem += len(parteConvertida[0]).to_bytes(1, "big") + parteConvertida[0]  # codigo antigo
        mensagem += len(parteConvertida[3]).to_bytes(1, "big") + parteConvertida[3]  # novo codigo
        mensagem += len(parteConvertida[1]).to_bytes(1, "big") + parteConvertida[1]  # nome disciplina
        mensagem += len(parteConvertida[2]).to_bytes(1, "big") + parteConvertida[2]  # nome professor
        mensagem += quantidadeAlunos.to_bytes(1, "big")  # quant alunos
        mensagem += cargaHoraria.to_bytes(1, "big")      # carga horaria
        mensagem += mediaTurma.to_bytes(3, "big")        # media turma
        return mensagem
    
    def escolhaD(self):  # Deletar disciplina
        codigo = input("Codigo da disciplina: ").upper()
        
        codigoBytes = codigo.encode("utf-8")
        mensagem = b""
        mensagem += 'D'.encode("utf-8")  # opcode
        mensagem += len(codigoBytes).to_bytes(1, "big") + codigoBytes  # codigo

        return mensagem

if __name__ == "__main__":
    cliente = Cliente()
    
    cliente.executar()  
    
    