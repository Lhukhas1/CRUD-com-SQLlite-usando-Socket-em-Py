import socket
import Banco

banco = Banco.Banco()
conector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conector.bind(('127.0.0.1', 50000))
conector.listen(1)

#DEFINE
TRUE = 'T'
FALSE = 'F'


while True:
    try:
        [sock_dados, _] = conector.accept()
        
        while True:
            try:
                opcode = sock_dados.recv(1) # Ver qual opcode
                opcode = opcode.decode("utf-8") # Decodificar a açao
                
                match(opcode):
                    case 'C': 
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

                        if(banco.buscar(codigo)):
                            sock_dados.send(FALSE.encode("utf-8")) 
                        else:
                            # Adicionar no banco
                            resultado = banco.adicionar(codigo, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma)


                        
                        # Confirmar se foi adicionado
                            if resultado is not None:
                                sock_dados.send(TRUE.encode("utf-8"))  

                            else:
                                sock_dados.send(FALSE.encode("utf-8")) 
                    

                    case 'R':   
                        # Codigo
                        tam_codigo = int.from_bytes(sock_dados.recv(1), "big")
                        codigo = sock_dados.recv(tam_codigo).decode("utf-8")
                        
                        # Buscar no banco
                        resultado = banco.buscar(codigo)
                        
                        if resultado:
                            sock_dados.send(TRUE.encode("utf-8"))  

                            # cod, nomeDisc, nomeProf, QuantAlu, CargaHoraria, mediaTurma
                            # Agilizar a codificaçao
                            parteConvertida = {}
                            parteConvertida[0] = resultado[0].encode("utf-8") # codigo
                            parteConvertida[1] = resultado[1].encode("utf-8") # nome disciplina
                            parteConvertida[2] = resultado[2].encode("utf-8") # nome professor
                            
                            # Codificar mensagem
                            mensagem = b""
                            mensagem += len(parteConvertida[0]).to_bytes(1, "big") + parteConvertida[0]  # codigo
                            mensagem += len(parteConvertida[1]).to_bytes(1, "big") + parteConvertida[1]  # nome disciplina
                            mensagem += len(parteConvertida[2]).to_bytes(1, "big") + parteConvertida[2]  # nome professor
                            mensagem += resultado[3].to_bytes(1, "big")      # quant alunos
                            mensagem += resultado[4].to_bytes(1, "big")      # carga horaria
                            mediaTurma = int(resultado[5] * 100)
                            mensagem += mediaTurma.to_bytes(3, "big")        # media turma
                            
                            sock_dados.send(mensagem)

                        else:
                            sock_dados.send(FALSE.encode("utf-8"))   
                    
                    case 'U':  
                        # Codigo antigo
                        tam_codigo = int.from_bytes(sock_dados.recv(1), "big")
                        codigo = sock_dados.recv(tam_codigo).decode("utf-8")
                        
                        # Codigo novo
                        tam_codigo_novo = int.from_bytes(sock_dados.recv(1), "big")
                        codigoNovo = sock_dados.recv(tam_codigo_novo).decode("utf-8")

                        # Nome disciplina
                        tam_disciplina = int.from_bytes(sock_dados.recv(1), "big")
                        nomeDisciplina = sock_dados.recv(tam_disciplina).decode("utf-8")
                        
                        # Nome professor
                        tam_professor = int.from_bytes(sock_dados.recv(1), "big")
                        nomeProfessor = sock_dados.recv(tam_professor).decode("utf-8")
                        
                        # Quant alunos
                        quantidadeAlunos = int.from_bytes(sock_dados.recv(1), "big")

                        # Carga horaria
                        cargaHoraria = int.from_bytes(sock_dados.recv(1), "big")

                        # Media da turma ja feito cast pra float
                        mediaTurma = int.from_bytes(sock_dados.recv(3), "big") / 100.0
                        
                        # Atualizar no banco
                        modificou = banco.update(codigo, codigoNovo, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma)

                        
                        if modificou:
                            sock_dados.send(TRUE.encode("utf-8"))  
                        else:
                            sock_dados.send(FALSE.encode("utf-8"))  
                            
                    
                    case 'D':  
                        # codigo
                        tam_codigo = int.from_bytes(sock_dados.recv(1), "big")
                        codigo = sock_dados.recv(tam_codigo).decode("utf-8")
                        
                        modificou = banco.remover(codigo)
                        
                        if modificou:
                            sock_dados.send(TRUE.encode("utf-8"))  
                        else:
                            sock_dados.send(FALSE.encode("utf-8"))  
                    


                    case 'L':  
                        resultados = banco.listarTodas()
                        
                        if resultados:
                            sock_dados.send(TRUE.encode("utf-8"))  

                            sock_dados.send(len(resultados).to_bytes(2, "big"))

                            for registro in resultados:
                                parteConvertida = {}
                                parteConvertida[0] = registro[0].encode("utf-8") # codigo
                                parteConvertida[1] = registro[1].encode("utf-8") # nome disciplina
                                parteConvertida[2] = registro[2].encode("utf-8") # nome professor
                                

                                mensagem = b""
                                mensagem += len(parteConvertida[0]).to_bytes(1, "big") + parteConvertida[0]  # codigo
                                mensagem += len(parteConvertida[1]).to_bytes(1, "big") + parteConvertida[1]  # nome disciplina
                                mensagem += len(parteConvertida[2]).to_bytes(1, "big") + parteConvertida[2]  # nome professor
                                mensagem += registro[3].to_bytes(1, "big")      # quant alunos
                                mensagem += registro[4].to_bytes(1, "big")      # carga horaria

                                mediaTurma = int(registro[5] * 100)
                                mensagem += mediaTurma.to_bytes(3, "big")       # media turma
                                
                                sock_dados.send(mensagem)
                            
                        else:
                            sock_dados.send(FALSE.encode("utf-8"))

                opcode = None
                        
            except Exception as e:
                print(f"Erro no servidor: {e}")
                break
          
    except Exception as e:
        print(f"Erro na conexão: {e}")
        sock_dados.close()
        banco.fecharConexao()
        continue


