from readXlsx.readData import readData
from pesosYUmbrales import matrizUmbrales,matrizPesos,guardarPesos,guardarUmbrales,readDataExcel,readDataExcel2
import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from interface import Ui_MainWindow as UI
import openpyxl

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
        self.ui.btn_simular.setEnabled(False)
        self.ui.btn_simular.style()
        
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
        self.iteraciones = self.ui.sBox_Iteraciones.value()
        self.rataAprendizaje = self.ui.dsBox_Rata.value()
        self.errorMaximo = self.ui.dsBox_EMP.value()
        self.entrenar()
        
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
        q = self.matrizUmbrales
        self.ui.tw_umb.setRowCount(1)
        self.ui.tw_umb.setColumnCount(q.shape[0])
        for i in range(q.shape[0]):
            item = QTableWidgetItem(str(q[i]))
            self.ui.tw_umb.setItem(0,i,item)
        self.ui.tw_umb.resizeColumnsToContents()
        self.ui.tw_umb.resizeRowsToContents()
        self.ui.tw_umb.viewport().update()
    
    def guardarPesos(matriz,nombre):
        matriz= matriz.tolist()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        for row in matriz:
            sheet.append(row)
            rutaPesos="archivosExcelGuardados/"+nombre+'.xlsx'
            workbook.save(rutaPesos)
        return rutaPesos
    
    def guardarUmbrales(matriz,nombre):
        matriz=matriz.tolist()
        workbook = openpyxl.Workbook()
        sheet = workbook.active 
        sheet.append(matriz)
        rutaUmbrales="archivosExcelGuardados/"+nombre+'.xlsx'
        workbook.save(rutaUmbrales)
        return rutaUmbrales
        
    def entrenar(self):
        self.Yr = np.zeros(self.salida)
        self.El = np.zeros(self.salida)
        self.EpTotal=np.zeros(self.patron)
        for itera in range(self.iteraciones):
            for patron in range(self.patron):
                a =self.matrizEntrada[patron]
                print(a)      
                
                Ep=0
                for i in range(self.salida): 
                    aux=0
                  
                    for j in range(self.entrada):
                      
                        aux+=(a[j])*(self.matrizPesos[i][j])
                   
                    self.Yr[i]=aux+self.matrizUmbrales[i]
                    if(self.ui.cBox_activacion.currentIndex()==0 ):
                        self.Yr[i] = self.Yr[i]
                    else:
                        if(self.Yr[i]>=0.5):
                            self.Yr[i] = 1
                        else:
                            self.Yr[i] = 0
                        print("si entra", self.Yr[i])
                    
                    self.El[i] = self.matrizSalida[i][i]-self.Yr[i]
                   
                    #!agregar el valor absoluto 
                    if(self.El[i])<0:
                        self.El[i] = self.El[i]*-1
                        Ep+=self.El[i]
                    print("error: por patron: ",Ep)

                Ep/=self.salida

                self.EpTotal[patron]=Ep
                print(self.Yr)
                print(self.El)
                print("error: por patron: ",Ep)
        
                #!Segunda parte del algoritmo
                #**Modificacion de PESOS Y UMBRALES

                for i in range(self.salida): 
                    aux = self.matrizPesos[i]
                    print("valor de i:" ,i)
                    for j in range(self.entrada):
                     
                        aux[j] = self.rataAprendizaje*self.El[i]*a[j]
                       
                    self.matrizPesos[i]= aux
                    self.matrizUmbrales[i]+=self.rataAprendizaje*self.El[i]*1
                        
        
    

            self.Erms = sum(self.EpTotal)/self.patron
            if(self.Erms <= self.errorMaximo):
                print("\nError maximo alcanzado\n")
                self.guardarPesos(self.matrizPesos,"Pesos")
                self.guardarUmbrales(self.matrizUmbrales,"Umbrales")
                self.ui.btn_simular.setEnabled(True)

                print("ERMS")
                print(self.Erms)
                break
           
            print("ERMS")
            print(self.Erms)
           
            
            
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

