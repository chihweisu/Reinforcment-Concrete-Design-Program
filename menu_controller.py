from PyQt5 import QtCore, QtGui, QtWidgets
from menu import Ui_menu
from RC_RecbeamCal import Ui_RCRecbeamCal
from RC_RecbeamCal_base import RecBeamCalButtonClicked
from RC_TbeamCal import Ui_RCTbeamCal
from RC_TbeamCal_base import TBeamCalButtonClicked
from RC_BeamDsgn import Ui_RCBeamDsgn
from RC_BeamDsgn_base import BeamDsgnButtonClicked
from RC_ColumnCal import Ui_RCColumnCal
from RC_ColumnCal_base import ColumnCalButtonClicked
from beam_function import BarAllowabelNumClicked
from  DataFrameModel import  DataFrameModel

class menu_controller(QtWidgets.QMainWindow):
  # signal=QtCore.pyqtSignal(list)
  def __init__(self):
      super().__init__()  # in python3, super(Class, self).xxx = super().xxx
      self.setWindowIcon(QtGui.QIcon('cover.png'))
      # self.setWindowTitle("title")
      self.ui = Ui_menu()
      self.ui.setupUi(self)
      self.setup_control()

  def setup_control(self):
      # TODO
      # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
      # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
      self.ui.RC_RecbeamCal.clicked.connect(self.RC_RecbeamCalClicked)
      self.ui.RC_TbeamCal.clicked.connect(self.RC_TbeamCalClicked)
      self.ui.RC_BeamDsgn.clicked.connect(self.RC_BeamDsgnClicked)
      self.ui.RC_ColumnCal.clicked.connect(self.RC_ColumnCalClicked)

  def RC_RecbeamCalClicked(self):
    self.hide()
    self.ui=w2_controller()
    self.ui.show()

  def RC_TbeamCalClicked(self):
    self.hide()
    self.ui=w3_controller()
    self.ui.show()
  
  def RC_BeamDsgnClicked(self) :
    self.hide()
    self.ui=w4_controller()
    self.ui.show()

  def RC_ColumnCalClicked(self):
    self.hide()
    self.ui=w5_controller()
    self.ui.show()
  

class w2_controller(QtWidgets.QMainWindow,Ui_RCRecbeamCal):
  def __init__(self):
    super(w2_controller,self).__init__()
    self.setupUi(self)
    self.setup_control()


  def setup_control(self):
    self.cnstrctblty='no'
    self.fc.setText('280')
    self.fy.setText('4200')
    self.Mux.setText('0')
    self.Vuy.setText('0')
    self.Tu.setText('0')
    self.closeButton1.clicked.connect(self.closebutton1Clicked)    
    self.constructability.clicked.connect(self.constructabilityClicked)
    self.calbutton.clicked.connect(lambda:RecBeamCalButtonClicked(self))
    self.barallowbutton.clicked.connect(lambda:BarAllowabelNumClicked(self,'Beam'))

  def constructabilityClicked(self) :
    self.cnstrctblty='yes' if self.constructability.isChecked() else 'no'
    return self.cnstrctblty

  def closebutton1Clicked(self):
    self.hide()
    self.ui=menu_controller()
    self.ui.show()

class w3_controller(Ui_RCTbeamCal,w2_controller,QtWidgets.QMainWindow):
  def __init__(self):
    super(w3_controller,self).__init__()
    self.setupUi(self)
    self.setup_control()

  def setup_control(self):
    self.cnstrctblty='no'
    self.fc.setText('280')
    self.fy.setText('4200')
    self.Mux.setText('0')
    self.Vuy.setText('0')
    self.Tu.setText('0')
    self.closeButton1.clicked.connect(self.closebutton1Clicked)    
    self.constructability.clicked.connect(self.constructabilityClicked)
    self.calbutton.clicked.connect(lambda:TBeamCalButtonClicked(self))
    self.barallowbutton.clicked.connect(lambda:BarAllowabelNumClicked(self,'Beam'))

class w4_controller(Ui_RCBeamDsgn,w2_controller,QtWidgets.QMainWindow):
  def __init__(self):
    super(w4_controller,self).__init__()
    self.setupUi(self)
    self.setup_control()

  def setup_control(self):        
    self.cnstrctblty='no'
    self.CCompBar='no'
    self.CTbeam='no'
    self.fc.setText('280')
    self.fy.setText('4200')
    self.Mu_left_minus.setText('0')
    self.Mu_left_plus.setText('0')
    self.Vg_left.setText('0')
    self.Tu_left.setText('0')
    self.Mu_mid_minus.setText('0')
    self.Mu_mid_plus.setText('0')
    self.Vg_mid.setText('0')
    self.Tu_mid.setText('0')
    self.Mu_rght_minus.setText('0')
    self.Mu_rght_plus.setText('0')
    self.Vg_rght.setText('0')
    self.Tu_rght.setText('0')
    self.constructability.clicked.connect(self.constructabilityClicked)
    self.ConsiderCompressionBar.clicked.connect(self.ConsiderCompressionBarClicked)
    self.ConsiderTbeam.clicked.connect(self.ConsiderTbeamClicked)
    self.dsgnbutton.clicked.connect(lambda:BeamDsgnButtonClicked(self))
    self.closeButton1.clicked.connect(self.closebutton1Clicked)  

  def ConsiderCompressionBarClicked(self) :
    self.CCompBar='yes' if self.ConsiderCompressionBar.isChecked() else 'no'
    return self.CCompBar
  def ConsiderTbeamClicked(self) :
    self.CTbeam='yes' if self.ConsiderTbeam.isChecked() else 'no'
    return self.CTbeam

class w5_controller(Ui_RCColumnCal,w2_controller,QtWidgets.QMainWindow):
  signal=QtCore.pyqtSignal(list)
  def __init__(self):
    super(w5_controller,self).__init__()
    self.setupUi(self)
    self.setup_control()

  def setup_control(self):
    self.cnstrctblty='no'
    self.fc.setText('280')
    self.fy.setText('4200')
    self.Mux.setText('0')
    self.Muy.setText('0')
    self.Pu.setText('0')
    self.closeButton1.clicked.connect(self.closebutton1Clicked)    
    self.constructability.clicked.connect(self.constructabilityClicked)
    self.calbutton.clicked.connect(self.calbuttonClicked)
    self.barallowbutton.clicked.connect(lambda:BarAllowabelNumClicked(self,'Column'))
    self.PicChangeButton.clicked.connect(self.picchangeclicked)
    self.signal.connect(self.aa)

  def calbuttonClicked(self):
    self.textBrowser.setText('running.......')
    QtWidgets.QApplication.processEvents()
    ColumnCalButtonClicked(self)

  def aa(self,result):
    self.result=result
    self.picchangeclicked()

  def picchangeclicked(self) :
    try :
      if self.PicChangeButton.isChecked():
        self.draw_mm(self.result)
      else :
        self.draw_pmm(self.result)
    except :
        self.textBrowser.setText('Please run the column analysis first')
        
  def output_df(self,table):
    df = table
    model = DataFrameModel(df)
    self.tableView.setModel(model)

  def draw_pmm(self,result):
      [interaction_diagram, mm_diagram, capacity_point,Mux,Muy,Mu,Pu]=result
      self.rcpmmwidget.canvas.axes.clear()
      self.rcpmmwidget.canvas.axes.plot(interaction_diagram['Mn'],interaction_diagram['Pn'], linestyle='--',color='orange')
      self.rcpmmwidget.canvas.axes.plot(interaction_diagram['phiMn'],interaction_diagram['phiPn'])
      self.rcpmmwidget.canvas.axes.plot(Mu,Pu,color='red',marker='o')
      self.rcpmmwidget.canvas.axes.plot([0,Mu,capacity_point[0]],[0,Pu,capacity_point[1]],color='gray', linestyle='--')
      self.rcpmmwidget.canvas.axes.set_xlabel('\u03c6 Mn(tf-m)', fontsize=8, color='white')
      self.rcpmmwidget.canvas.axes.set_ylabel('\u03c6 Pn(tf)', fontsize=8, color='white')
      self.rcpmmwidget.canvas.axes.grid(True,linestyle='--', color='black')
      self.rcpmmwidget.canvas.axes.axis([0,None,None,None])
      self.rcpmmwidget.canvas.draw()
      #顯示表格
      self.output_df(interaction_diagram)

  def draw_mm(self,result) :
      [interaction_diagram, mm_diagram, capacity_point,Mux,Muy,Mu,Pu]=result
      self.rcpmmwidget.canvas.axes.clear()
      self.rcpmmwidget.canvas.axes.plot(mm_diagram['phi']*mm_diagram['Mnx'],mm_diagram['phi']*abs(mm_diagram['Mny']))
      self.rcpmmwidget.canvas.axes.plot(Mux,Muy,color='red',marker='o')
      self.rcpmmwidget.canvas.axes.set_xlabel('\u03c6 Mnx(tf-m)', fontsize=8, color='white')
      self.rcpmmwidget.canvas.axes.set_ylabel('\u03c6 Mny(tf)', fontsize=8, color='white')
      self.rcpmmwidget.canvas.axes.grid(True,linestyle='--', color='black')
      self.rcpmmwidget.canvas.axes.axis([0,None,0,None])
      self.rcpmmwidget.canvas.draw()
      #顯示表格
      self.output_df(mm_diagram)



