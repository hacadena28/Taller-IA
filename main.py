from readXlsx.readData import readData
from pesosYUmbrales import matrizUmbrales,matrizPesos,guardarPesos,guardarUmbrales,readDataExcel,readDataExcel2
import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from interface import Ui_MainWindow as UI

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.InicializarGUI()

    def InicializarGUI(self):
        #---------------------declaracion de variables-----------------------
        self.ui = UI()
        self.ui.setupUi(self)
        self.iteraciones=.0
        self.rataAprendizaje=.0
        self.errorMaximo=.0
        self.ui.rbtn_per.clicked.connect(self.toggle)
        self.ui.rbtn_ada.clicked.connect(self.toggle)
        self.ui.cBox_activacion.currentTextChanged.connect(self.toggle2)
        self.ui.btn_datos.clicked.connect(self.fileOpen)
        self.ui.btn_entrenar.clicked.connect(self.setiar)
        
        self.show()

    def configuraLCD(self):
        self.ui.lcdNumber_e.setDigitCount(self.digitos(self.entrada))
        self.ui.lcdNumber_s.setDigitCount(self.digitos(self.salida))
        self.ui.lcdNumber_p.setDigitCount(self.digitos(self.patron))
        self.ui.lcdNumber_e.display(self.entrada)
        self.ui.lcdNumber_s.display(self.salida)
        self.ui.lcdNumber_p.display(self.patron)
    
    def digitos(self,n):
        digits = len(str(n))
        return digits

    def fileOpen(self):
        ruta, _ = QFileDialog.getOpenFileName(self,'Elegir Archivo','C:\\Users\\Jpalacio\\Desktop')
        if ruta =='':
            print("Seleccione un archivo")
        else:
            self.entrada, self.salida, self.patron, self.matrizEntrada, self.matrizSalida = readData(ruta)
            self.configuraLCD()
            
            self.matrizPesos()
            self.matrizUmbrales()
            
    def setiar(self):
        self.iteraciones = self.ui.sBox_Iteraciones.value
        self.rataAprendizaje = self.ui.dsBox_Rata.value
        self.errorMaximo = self.ui.dsBox_EMP.value
        print("prueba 1")
        
    def toggle(self):
        if(self.ui.rbtn_per.isChecked()):
            self.ui.rbtn_per.setChecked(True)
            self.ui.rbtn_ada.setChecked(False)
            self.ui.cBox_activacion.setCurrentIndex(0)
        else:
            self.ui.rbtn_ada.setChecked(True)
            self.ui.rbtn_per.setChecked(False)
            self.ui.cBox_activacion.setCurrentIndex(1)
            
    def toggle2(self):
        if(self.ui.cBox_activacion.currentIndex()==0 ):
            self.ui.rbtn_per.setChecked(True)
            self.ui.rbtn_ada.setChecked(False)
            
        if(self.ui.cBox_activacion.currentIndex()==1 ):
            self.ui.rbtn_ada.setChecked(True)
            self.ui.rbtn_per.setChecked(False)
    
    def matrizPesos(self):
        
        self.matrizPesos = np.random.uniform(low=-1, high=1, size=(self.salida, self.entrada))
        self.matrizPesos = np.round(self.matrizPesos, decimals=2)
        print(self.matrizPesos)
        p = self.matrizPesos
        self.ui.tw_w.setRowCount(p.shape[0])
        self.ui.tw_w.setColumnCount(p.shape[1])
        for i in range(p.shape[1]):
            for j in range(p.shape[0]):
                item = QTableWidgetItem(str(p[j][i]))
                self.ui.tw_w.setItem(j,i,item)
        self.ui.tw_w.resizeColumnsToContents()
        self.ui.tw_w.resizeRowsToContents()
        self.ui.tw_w.viewport().update()

    def matrizUmbrales(self):
        self.matrizUmbrales = np.random.uniform(low=-1, high=1, size=(self.salida))
        self.matrizUmbrales = np.round(self.matrizUmbrales, decimals=2)
        print(self.matrizUmbrales)

    
def main():
    windows = QApplication(sys.argv)
    ventana= Aplicacion()
    ventana.show()

    sys.exit(windows.exec_())

if __name__ == "__main__":
    main()



























# red =0
# funcionDeActivacion=""
# algoritmoDeEntrenamiento="Regla Delta"
# while(red==0):
#     red = int(input("Digite 1 para Percetron 2 para Adaline: \n"))
    
# if(red == 1):
#     red = "PERCETRON"
#     funcionDeActivacion="Escalon"
# else:
#     red = "ADALINE"
#     funcionDeActivacion="Lineal"
        
# print(red)
# print(funcionDeActivacion)

# #**Carga los pesos y umbrales funciones de llamado
# # w = readDataExcel2(AbrirDocumento())
# # print(w)
# # u = readDataExcel(AbrirDocumento())
# # print(u)



# #**Se genera la matriz de peso aleatoriamente
# w= matrizPesos(entrada,salida)
# guardarPesos(w,"Pesos")
# # print(w)
# #**Se genera el vector de umbrales aleatoriamente
# u= matrizUmbrales(salida)
# # print(u)
# guardarUmbrales(u,"Umbrales")

