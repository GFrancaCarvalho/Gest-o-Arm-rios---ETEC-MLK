import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from Interface import Ui_MainWindow
import commands

# Conexão comandos + interface ->

class myMainWindow(QMainWindow):
    def __init__(self):
        super(myMainWindow, self).__init__()

        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)


        # Conexão dos botões com as funçõoes -> 

        self.main_ui.AddButton.clicked.connect(self.showAdd)
        self.main_ui.SearchButton.clicked.connect(self.showSearch)
        self.main_ui.DeleteButton.clicked.connect(self.showDelete)
        self.main_ui.InfoButton.clicked.connect(self.showInfo)
        self.main_ui.exitBttn.clicked.connect(self.closeApp)
        self.main_ui.VoltarButtonB.clicked.connect(self.buscar_todos)
        self.main_ui.RegistrarBttn.clicked.connect(self.adicionar_cadastro)
        self.main_ui.DelButtonDEL.clicked.connect(self.excluir_cadastro)
        self.main_ui.BuscarButtonB.clicked.connect(self.buscar_espec)
        self.main_ui.popupclosebtn.clicked.connect(self.fechar_pop)

    # Funções ->

    # Troca para a tela "Add"

    def showAdd(self):
        self.main_ui.pages.setCurrentWidget(self.main_ui.Add1)

    # Troca para a tela "Search" e preenche a tabela

    def showSearch(self):
        self.main_ui.pages.setCurrentWidget(self.main_ui.Search1)
        self.buscar_todos()

    # Troca para a tela "Delete"

    def showDelete(self):
        self.main_ui.pages.setCurrentWidget(self.main_ui.Delete1)

    # Troca para a tela "Infos"

    def showInfo(self):
        self.main_ui.pages.setCurrentWidget(self.main_ui.Infos1)

    # Função para preencher a tabela com todos os dados do Banco

    def buscar_todos(self):

        dados_tabela = commands.buscar_todos()
        self.main_ui.TabelaBuscar.setRowCount(len(dados_tabela))
        self.main_ui.InputBuscarB.clear()
        row = 0
        for i in dados_tabela:
            self.main_ui.TabelaBuscar.setItem(row, 0, QTableWidgetItem(i[1]))
            self.main_ui.TabelaBuscar.setItem(row, 1, QTableWidgetItem(i[2]))
            self.main_ui.TabelaBuscar.setItem(row, 2, QTableWidgetItem(i[3]))
            self.main_ui.TabelaBuscar.setItem(row, 3, QTableWidgetItem(i[4]))
            self.main_ui.TabelaBuscar.setItem(row, 4, QTableWidgetItem(i[5]))
            self.main_ui.TabelaBuscar.setItem(row, 5, QTableWidgetItem(i[6]))
            row += 1

    # Função para encerrar o aplicativo

    def closeApp(self):
        sys.exit(app.exec())

    # Função para adicionar um cadastro do Banco de Dados

    def adicionar_cadastro(self):
        if self.main_ui.InputNomeAlunoAD.text() == "" or self.main_ui.InputCursoAD.text() == "" or self.main_ui.InputArmarioAD.text() == "" or commands.registro(self.main_ui.InputNomeAlunoAD.text(), self.main_ui.InputCursoAD.text(), self.main_ui.InputArmarioAD.text()) == []:
            self.main_ui.InputNomeAlunoAD.clear()
            self.main_ui.InputCursoAD.clear()
            self.main_ui.InputArmarioAD.clear()
            self.main_ui.popup.hide()
            self.main_ui.error_popup()
            self.main_ui.textpopup.setText("| Erro: Campo vazio ou armário inválido.")
            self.main_ui.popup.show()

        else:
            commands.registro(self.main_ui.InputNomeAlunoAD.text(
            ), self.main_ui.InputCursoAD.text(), self.main_ui.InputArmarioAD.text())
            self.main_ui.InputNomeAlunoAD.clear()
            self.main_ui.InputCursoAD.clear()
            self.main_ui.InputArmarioAD.clear()
            self.main_ui.popup.hide()
            self.main_ui.sucess_popup()
            self.main_ui.textpopup.setText("| Cadastro realizado com sucesso.")
            self.main_ui.popup.show()

    # Função para excluir um cadastro do Banco de Dados

    def excluir_cadastro(self):
        if commands.excluir_cadastro(self.main_ui.InputButtonDEL.text()) == []:
            self.main_ui.InputButtonDEL.clear()
            self.main_ui.error_popup()
            self.main_ui.textpopup.setText("| Usuário não encontrado.")
            self.main_ui.popup.show()
            
        else:
            commands.excluir_cadastro(self.main_ui.InputButtonDEL.text())
            self.main_ui.popup.hide()
            self.main_ui.InputButtonDEL.clear()
            self.main_ui.sucess_popup()
            self.main_ui.textpopup.setText("| Usuário removido com sucesso.")
            self.main_ui.popup.show()

    # Na tela de busca, realiza pesquisas com termos inseridos pelo usuário

    def buscar_espec(self):
        resultado = (commands.buscar(self.main_ui.InputBuscarB.text()))
        self.main_ui.InputBuscarB.clear()
        if resultado != None:
            self.main_ui.popup.hide()
            self.main_ui.TabelaBuscar.setRowCount(1)
            self.main_ui.TabelaBuscar.setItem(0, 0, QTableWidgetItem(resultado[1]))
            self.main_ui.TabelaBuscar.setItem(0, 1, QTableWidgetItem(resultado[2]))
            self.main_ui.TabelaBuscar.setItem(0, 2, QTableWidgetItem(resultado[3]))
            self.main_ui.TabelaBuscar.setItem(0, 3, QTableWidgetItem(resultado[4]))
            self.main_ui.TabelaBuscar.setItem(0, 4, QTableWidgetItem(resultado[5]))
            self.main_ui.TabelaBuscar.setItem(0, 5, QTableWidgetItem(resultado[6]))
        else:
            self.main_ui.popup.hide()
            self.main_ui.InputButtonDEL.clear()
            self.main_ui.error_popup()
            self.main_ui.textpopup.setText("| Usuário ou armário não encontrado.")
            self.main_ui.popup.show()
            


    # Botão para fechar popup

    def fechar_pop(self):
        self.main_ui.popup.hide()

# Execução do aplicativo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = myMainWindow()
    window.show()

    sys.exit(app.exec())
