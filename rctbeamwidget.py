from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtCore import QThread, Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor


class rctbeamwidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.drawornot = 'no'
    

    def rctbeamdraw_info(self,data,BarNum,BarAllowabelNumPerRow,stirrup_d,bard1,bard2,be,BeamCondition):

        factor=min(300/be,200/float(data.depth.text()))
        self.BeamCondition=BeamCondition
        self.factor=factor
        self.D=float(data.depth.text())*factor
        self.B=float(data.width.text())*factor
        self.hf=float(data.hf.text())
        self.be=be*factor
        self.bard=[bard1*factor,bard2*factor]
        self.stirrup_d=stirrup_d*factor
        self.BarNum=BarNum
        if self.BeamCondition=='內梁' :
            self.x_offset=(self.be-self.B)/2
        else :
            self.x_offset=self.be-self.B
        self.BarAllowabelNumPerRow=BarAllowabelNumPerRow
        self.xstart=(4+stirrup_d)*factor+self.x_offset
        self.ystart=[self.D-(4+stirrup_d+bard1)*factor,(4+stirrup_d)*factor]
        self.db_h=[(self.B/factor-8-2*stirrup_d-bard1)*factor/(min(BarNum[0],BarAllowabelNumPerRow[0])-1),
                     (self.B/factor-8-2*stirrup_d-bard2)*factor/(min(BarNum[1],BarAllowabelNumPerRow[1])-1)]
        self.cleardb_v=[(-2.5-bard1)*factor,(2.5+bard2)*factor]
        self.drawornot='yes'
        self.str_start=[(4+stirrup_d/2)*factor+self.x_offset,(4+stirrup_d/2)*factor]
        self.arcd=max(self.bard[0],self.bard[1])+self.stirrup_d
        self.str_width=self.D-(8+stirrup_d)*factor
        self.str_height=self.B-(8+stirrup_d)*factor
        self.cuvre_start=[self.str_start[0]+(0.5+2**0.5/4)*self.arcd,self.str_start[1]+(0.5-2**0.5/4)*self.arcd]
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
            self.qpainter.drawRect(QRect(0+self.x_offset, 0, self.B,self.D))
            self.qpainter.drawRect(QRect(0, 0, self.x_offset,self.hf))
            if self.BeamCondition=='內梁' :
                self.qpainter.drawRect(QRect(self.B+self.x_offset, 0, self.x_offset,self.hf))
            # Draw 剪力筋
            qpen = QPen(Qt.red, 1.5, Qt.SolidLine)
            self.qpainter.setPen(qpen)
            self.qpainter.drawRoundedRect(self.str_start[0],self.str_start[1],self.str_height,self.str_width,self.arcd/2,self.arcd/2) 
            self.qpainter.drawArc(self.str_start[0],self.str_start[1],self.arcd,self.arcd,45*16,180*16)
            self.qpainter.drawLine(self.cuvre_start[0],self.cuvre_start[1],self.cuvre_start[0]+self.cuvre_length/2**0.5
                                  ,self.cuvre_start[1]+self.cuvre_length/2**0.5) 
            self.qpainter.drawLine(self.cuvre_start[0]-self.arcd/2**0.5,self.cuvre_start[1]+self.arcd/2**0.5,
                                   self.cuvre_start[0]+self.cuvre_length/2**0.5-self.arcd/2**0.5,self.cuvre_start[1]+self.cuvre_length/2**0.5+self.arcd/2**0.5) 
            # Draw 鋼筋
            qpen = QPen(Qt.black, 1.5, Qt.SolidLine)
            self.qpainter.setPen(qpen)
            self.qpainter.setBrush(Qt.black)
            for i in range(2) :
                for j in range(self.BarNum[i]) :
                    if j< self.BarAllowabelNumPerRow[i] :
                        self.qpainter.drawEllipse(self.xstart+j*self.db_h[i],self.ystart[i],self.bard[i],self.bard[i])
                    else :
                        if (j-self.BarAllowabelNumPerRow[i])%2 == 0 :
                            self.qpainter.drawEllipse(self.xstart+0.5*(j-self.BarAllowabelNumPerRow[i])*self.db_h[i]
                                                      ,self.ystart[i]+self.cleardb_v[i],self.bard[i],self.bard[i])
                        else  :
                            self.qpainter.drawEllipse(self.B+2*self.x_offset-self.xstart-self.bard[i]-0.5*(j-self.BarAllowabelNumPerRow[i]-1)*self.db_h[i]
                                                      ,self.ystart[i]+self.cleardb_v[i],self.bard[i],self.bard[i])
            
            


        self.qpainter.end()
        


            

        
