from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtCore import QThread, Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor,QFont


class rcbeamdsgnwidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.drawornot = 'no'
    

    def rcbeamdsgndraw_info(self,data,choose_bar,dsgn_barnum,s_dsgn_all,choose_stirrup,choose_stirrup_num,barinfo):
        self.wsize=500
        self.hsize=150
        w=float(data.length.text())+float(data.depth.text())
        h=2*float(data.depth.text())
        factor=min(self.wsize/w,self.hsize/h)
        self.factor=factor
        self.L=float(data.length.text())*factor
        self.D=float(data.depth.text())*factor
        self.colw=self.D
        self.colh=self.D/2
        self.B=float(data.width.text())*factor
        self.choose_bar=choose_bar
        self.dsgn_barnum=dsgn_barnum
        self.s_dsgn_all=s_dsgn_all
        self.choose_stirrup=choose_stirrup
        self.choose_stirrup_num=choose_stirrup_num
        self.barinfo=barinfo
        self.drawornot='yes'
        self.update()

    def paintEvent(self, event):
        self.qpainter = QPainter()
        self.qfont = QFont()
        self.qpainter.begin(self)
        palette = self.palette()
        palette.setColor(self.backgroundRole(),QColor(57,66,83))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        qpen = QPen(Qt.black, 2.5, Qt.SolidLine)
        self.qpainter.setPen(qpen)
        if self.drawornot=='yes' :
            #畫梁與柱
            p1x=self.wsize/2-self.L/2-self.colw/2
            p2x=self.wsize/2-self.L/2+self.colw/2
            p3x=self.wsize/2+self.L/2-self.colw/2
            p1y=self.hsize/2-self.colh-self.D/2
            p2y=self.hsize/2-self.D/2
            self.qpainter.setBrush(QColor(230,230,230))
            self.qpainter.drawRect(QRect(p2x,p2y, self.L-self.colw,self.D))
            self.qpainter.drawRect(QRect(p1x,p1y, self.colw,2*self.colh+self.D))
            self.qpainter.drawRect(QRect(p3x,p1y, self.colw,2*self.colh+self.D))
            qpen = QPen(QColor(230,230,230), 2, Qt.SolidLine)
            self.qpainter.setPen(qpen)
            self.qpainter.setBrush(QColor(57,66,83))
            self.qpainter.drawLine(p2x,p2y,p2x,p2y+self.D)
            self.qpainter.drawLine(p3x,p2y,p3x,p2y+self.D)

            #畫鋼筋
            qpen = QPen(Qt.black, 3, Qt.SolidLine)
            self.qpainter.setPen(qpen)
            self.qpainter.drawLine(p2x-self.colw/2,p2y+7*self.factor,p3x+self.colw/2,p2y+7*self.factor)
            self.qpainter.drawLine(p2x-self.colw/2,p2y+self.D-10*self.factor,p3x+self.colw/2,p2y+self.D-7*self.factor)
            #畫標線
            qpen = QPen(Qt.red, 1, Qt.SolidLine)
            self.qpainter.setPen(qpen)
            self.qpainter.drawLine(p2x+0.05*self.L,p2y+7*self.factor,p2x+0.05*self.L,p2y-self.colh/2)
            self.qpainter.drawLine(p2x+0.05*self.L,p2y+self.D-7*self.factor,p2x+0.05*self.L,p2y+self.D+self.colh/2)
            self.qpainter.drawLine(p3x-0.05*self.L,p2y+7*self.factor,p3x-0.05*self.L,p2y-self.colh/2)
            self.qpainter.drawLine(p3x-0.05*self.L,p2y+self.D-7*self.factor,p3x-0.05*self.L,p2y+self.D+self.colh/2)
            self.qpainter.drawLine(self.wsize/2,p2y+7*self.factor,self.wsize/2,p2y-self.colh/2)
            self.qpainter.drawLine(self.wsize/2,p2y+self.D-7*self.factor,self.wsize/2,p2y+self.D+self.colh/2)
        
            #標示鋼筋
            inputx=[p2x+0.05*self.L,self.wsize/2-50,p3x-0.05*self.L-100,]
            inputy=[p2y-self.colh,p2y+self.D+self.colh/2]
            xnum=[0,0,1,1,2,2]
            ynum=[0,1,0,1,0,1]
            Align=[Qt.AlignLeft,Qt.AlignCenter,Qt.AlignRight]
            content1=[0,1,2,3,4,5]
            adjusty=[-12,0]
            
            maxnumperrow=self.barinfo[self.choose_bar][2]
            for i in range(6) :
                if self.dsgn_barnum[i]<=maxnumperrow :
                    self.qpainter.drawText(inputx[xnum[i]],inputy[ynum[i]],100,20,Align[xnum[i]],str(self.dsgn_barnum[i])+' - '+self.choose_bar)
                else :
                    double_layer=[str(maxnumperrow),str(self.dsgn_barnum[i]-maxnumperrow)]
                    self.qpainter.drawText(inputx[xnum[i]],inputy[ynum[i]]+adjusty[ynum[i]],100,30,Align[xnum[i]],double_layer[ynum[i]]+' - '+self.choose_bar+'\n'
                                                                                         +double_layer[1-ynum[i]]+' - '+self.choose_bar)
            # self.qpainter.drawText(p2x+0.05*self.L,p2y-self.colh,100,50,Qt.AlignLeft,str(self.dsgn_barnum[0])+' - '+self.choose_bar)
            # self.qpainter.drawText(p2x+0.05*self.L,p2y+self.D+self.colh/2,100,50,Qt.AlignLeft,str(self.dsgn_barnum[1])+' - '+self.choose_bar )
            # self.qpainter.drawText(self.wsize/2-50,p2y-self.colh,100,20,Qt.AlignCenter,str(self.dsgn_barnum[2])+' - '+self.choose_bar )
            # self.qpainter.drawText(self.wsize/2-50,p2y+self.D+self.colh/2,100,20,Qt.AlignCenter,str(self.dsgn_barnum[3])+' - '+self.choose_bar )
            # self.qpainter.drawText(p3x-0.05*self.L-100,p2y-self.colh,100,50,Qt.AlignRight,str(self.dsgn_barnum[4])+' - '+self.choose_bar )
            # self.qpainter.drawText(p3x-0.05*self.L-100,p2y+self.D+self.colh/2,100,50,Qt.AlignRight,str(self.dsgn_barnum[5])+' - '+self.choose_bar )
            #標註剪力鋼筋
            self.qpainter.drawText(p2x+0.05*self.L,p2y+self.D/2-5,100,10,Qt.AlignLeft, str(self.choose_stirrup_num[0])+' - '+self.choose_stirrup[0]+' @'+str(self.s_dsgn_all[0]))
            self.qpainter.drawText(self.wsize/2-50,p2y+self.D/2-5,100,10,Qt.AlignCenter,str(self.choose_stirrup_num[1])+' - '+self.choose_stirrup[1]+' @'+str(self.s_dsgn_all[1]))
            self.qpainter.drawText(p3x-0.05*self.L-100,p2y+self.D/2-5,100,10,Qt.AlignRight,str(self.choose_stirrup_num[0])+' - '+self.choose_stirrup[0]+' @'+str(self.s_dsgn_all[0]))            

        self.qpainter.end()
        


            

        
