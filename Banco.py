import sqlite3

class Banco:
    def __init__(self):
        self.conexao = sqlite3.connect("teste.db")
        cursor = self.conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS teste(codigo PRIMARY KEY, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma)")
        self.conexao.commit()
        cursor.close()
    
    # cod, nomeDisc, nomeProf, QuantAlu, CargaHoraria, mediaTurma
    def adicionar(self, codigo, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO teste(codigo, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma) VALUES(?, ?, ?, ?, ?, ?)',
                      (codigo, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma))
        if cursor.rowcount > 0:
            id = cursor.lastrowid
        else:
            id = None
        self.conexao.commit()
        cursor.close()
        return id
    
    # retorna uma tupla contendo todos os campos, na mesma ordem de criação do banco
    def buscar(self, codigo):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM teste WHERE codigo = ?', (codigo,))
        retorno = cursor.fetchone()
        cursor.close()
        return retorno
    


    def listarTodas(self):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM teste')
        retorno = cursor.fetchall()
        cursor.close()
        return retorno
    
  
    def update(self, codigoAntigo, codigoNovo, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma):
        cursor = self.conexao.cursor()
        
        cursor.execute("UPDATE teste SET codigo = ?, nomeDisciplina = ?, nomeProfessor = ?, quantidadeAlunos = ?, cargaHoraria = ?, mediaTurma = ? WHERE codigo = ?",
                      (codigoNovo, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma, codigoAntigo))
        sucesso = cursor.rowcount > 0
        self.conexao.commit()
        cursor.close()
        return sucesso  
    
    
    def remover(self, codigo):
        cursor = self.conexao.cursor()
        cursor.execute('DELETE FROM teste WHERE codigo = ?', (codigo,))
        sucesso = cursor.rowcount > 0
        self.conexao.commit()
        cursor.close()
        return sucesso  
    

    def fecharConexao(self):
        if self.conexao:
            self.conexao.close()