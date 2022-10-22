from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtCore import QThread, Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor


class rccolumnwidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.drawornot = 'no'
    

    def rccolumndraw_info(self,data,Nx,Ny,stirrup_d,db_rebar1,db_rebar2,PrtctT):

        factor=200/max(float(data.depth.text()),float(data.width.text()))
        self.factor=factor
        self.D=float(data.depth.text())*factor
        self.B=float(data.width.text())*factor
        self.bard=[db_rebar1*factor,db_rebar2*factor]
        self.stirrup_d=stirrup_d*factor
        self.Nx=Nx
        self.Ny=Ny
        self.xstart=[(PrtctT+stirrup_d)*factor,self.B-(PrtctT+stirrup_d+db_rebar1)*factor]    #[左,右]
        self.ystart=[self.D-(PrtctT+stirrup_d+db_rebar2)*factor,(PrtctT+stirrup_d)*factor]    #[下,上]
        self.db_h=[(self.B/factor-2*PrtctT-2*stirrup_d-db_rebar1)*factor/(Nx-1),
                     (self.D/factor-2*PrtctT-2*stirrup_d-db_rebar2)*factor/(Ny-1)]
        self.drawornot='yes'
        self.str_start=(PrtctT+stirrup_d/2)*factor

        self.arcd=max(self.bard[0],self.bard[1])+self.stirrup_d
        self.str_width=self.D-(2*PrtctT+stirrup_d)*factor
        self.str_height=self.B-(2*PrtctT+stirrup_d)*factor
        self.cuvre_start=[self.str_start+(0.5+2**0.5/4)*self.arcd,self.str_start+(0.5-2**0.5/4)*self.arcd]
        self.cuvre_length=max(6*stirrup_d,7.5)*factor
        self.update()

    def paintEvent(self, event):
        self.qpainter = QPainter()
        self.qpainter.begin(self)
        palette = self.palette()
        palette.setColor(self.backgroundRole(),QColor(57,66,83))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        qpen = QPen(Qt.black, 2, Qt.SolidLine)
        self.qpainter.setPen(qpen)


        if self.drawornot =='yes' :
            #Draw 斷面
            self.qpainter.setBrush(QColor(230,230,230))
            self.qpainter.drawRect(QRect(0, 0, self.B,self.D))

            # Draw 剪力筋
            qpen = QPen(Qt.red, 1.5, Qt.SolidLine)
            self.qpainter.setPen(qpen)
            self.qpainter.drawRoundedRect(self.str_start,self.str_start,self.str_height,self.str_width,self.arcd/2,self.arcd/2) 
            self.qpainter.drawArc(self.str_start,self.str_start,self.arcd,self.arcd,45*16,180*16)
            self.qpainter.drawLine(self.cuvre_start[0],self.cuvre_start[1],self.cuvre_start[0]+self.cuvre_length/2**0.5
                                  ,self.cuvre_start[0]+self.cuvre_length/2**0.5) 
            self.qpainter.drawLine(self.cuvre_start[0]-self.arcd/2**0.5,self.cuvre_start[1]+self.arcd/2**0.5,
                                   self.cuvre_start[0]+self.cuvre_length/2**0.5-self.arcd/2**0.5,self.cuvre_start[0]+self.cuvre_length/2**0.5+self.arcd/2**0.5) 
            # Draw 鋼筋
            qpen = QPen(Qt.black, 1.5, Qt.SolidLine)
            self.qpainter.setPen(qpen)
            self.qpainter.setBrush(Qt.black)
            for i in range(2) :
                for j in range(self.Nx) :
                     self.qpainter.drawEllipse(self.xstart[0]+j*self.db_h[0],self.ystart[i],self.bard[0],self.bard[0])
                for j in range(self.Ny) :
                     self.qpainter.drawEllipse(self.xstart[i],self.ystart[1]+j*self.db_h[1],self.bard[1],self.bard[1])

            

        self.qpainter.end()
        


            

        
