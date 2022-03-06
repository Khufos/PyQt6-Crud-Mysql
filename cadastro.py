
from reportlab.pdfgen import canvas
from PyQt6 import  uic,QtWidgets
import mysql.connector
#from mysql.connector import (connection)
numero_id = 0
banco = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd = "",
    database='cadastro_produtos'
);

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()


    if formulario.radioButton.isChecked():
        categoria = 'Informatica'
    elif formulario.radioButton_2.isChecked():
        categoria = 'Alimentos'
    elif formulario.radioButton_3.isChecked():
        categoria = 'Eletronicos'
    
    cursor = banco.cursor()
    comando_sql = "INSERT INTO produtos values (default,%s,%s,%s,%s)"
    dados =(str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_sql,dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def chamatela():
    tela_lista.show()

    lista_banc = banco.cursor()
    command_sql = "SELECT * FROM produtos"
    lista_banc.execute(command_sql)
    dados_lidos = lista_banc.fetchall() 

    #--------------mostrando na tabela ---------------#
    #tamanhotabela = len(dados_lidos)
    tela_lista.tableWidget.setRowCount(len(dados_lidos))
    tela_lista.tableWidget.setColumnCount(5)
    for i in range(0, len(dados_lidos)):
        for j in range(0 , 5):
            tela_lista.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def pdf():
    pdf = banco.cursor()
    comando_sql = "SELECT * FROM produtos"
    pdf.execute(comando_sql)
    dados_lidos = pdf.fetchall()
    y = 0
    pdf_show = canvas.Canvas("Cadastro_produto.pdf")
    pdf_show.setFont("Times-Bold", 25)
    pdf_show.drawString(200,800,"Produtos cadastrados")
    pdf_show.setFont("Times-Bold", 12)
    #------------------------------------------#
    pdf_show.drawString(10,690,"ID")
    pdf_show.drawString(110,690,"CODIGO")
    pdf_show.drawString(210,690,"PRODUTO")
    pdf_show.drawString(310,690, "PREÇO")
    pdf_show.drawString(410,690,"CATEGORIA")
    for  i in range(0, len(dados_lidos)):
        y = y + 60
        pdf_show.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf_show.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf_show.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf_show.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf_show.drawString(410,750 - y, str(dados_lidos[i][4]))
    pdf_show.save()
    print("PDF FOI GERADO COM SUCESSO!")

def excluir_dados():
    linha = tela_lista.tableWidget.currentRow()
    tela_lista.tableWidget.removeRow(linha)
    excluir = banco.cursor()
    excluir.execute("SELECT id from  produtos")
    dados_lidos = excluir.fetchall()
    valor_id = dados_lidos[linha][0]
    excluir.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
    banco.commit()

def editar():
    global numero_id
    linha = tela_lista.tableWidget.currentRow() # -> retorna qual linha clico na tabela 
    editar = banco.cursor() # -> declaro o curso do banco onde eu vou da query no banco 
    editar.execute("SELECT id from  produtos") # -> pesquisa dentro do tabela do banco 
    dados_lidos = editar.fetchall()
    valor_id = dados_lidos[linha][0]
    editar.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = editar.fetchall()
    telaedit.show()

    numero_id = valor_id


    telaedit.lineEdit.setText(str(produto[0][0]))
    telaedit.lineEdit_2.setText(str(produto[0][1]))
    telaedit.lineEdit_3.setText(str(produto[0][2]))
    telaedit.lineEdit_4.setText(str(produto[0][3]))
    telaedit.lineEdit_5.setText(str(produto[0][4]))
  

def salvar():
   #print(numero_id)
   codigo = telaedit.lineEdit_2.text()
   descricao = telaedit.lineEdit_3.text()
   preco = telaedit.lineEdit_4.text()
   categoria = telaedit.lineEdit_5.text()
   salvar = banco.cursor()
   salvar.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}'  WHERE id = {} ".format(codigo,descricao,preco,categoria,numero_id))
   banco.commit()
   telaedit.close()
   tela_lista.close()
   chamatela()
   


app=QtWidgets.QApplication([])
#------------------------------------------
formulario=uic.loadUi("telacd.ui")
#----------------------------------------------
tela_lista=uic.loadUi("telalista.ui")
#=-------------------------------------------------
telaedit = uic.loadUi("telaedit.ui")
#--------------------------------------------
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chamatela)
tela_lista.pushButton_2.clicked.connect(excluir_dados)
tela_lista.pushButton.clicked.connect(pdf)
tela_lista.pushButton_3.clicked.connect(editar)
telaedit.pushButton_3.clicked.connect(salvar)


formulario.show()
app.exec()