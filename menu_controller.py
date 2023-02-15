from PyQt5 import QtCore, QtGui, QtWidgets
from ui_menu import Ui_Menu
from ui_rc_recbeamcal import Ui_RcRecBeamCal
from rc_recbeamcal_base import recbeam_cal_button_clicked
from ui_rc_tbeamcal import Ui_RcTBeamCal
from rc_tbeamcal_base import tbeam_cal_button_clicked
from ui_rc_beamdsgn import Ui_RcBeamDsgn
from rc_beamdsgn_base import beam_dsgn_button_clicked
from ui_rc_columncal import Ui_RcColumnCal
from rc_columncal_base import column_cal_button_clicked
from beam_function import bar_allowable_num_clicked
from  dataframe_model import  DataFrameModel

class MenuController(QtWidgets.QMainWindow):
  # signal=QtCore.pyqtSignal(list)
  def __init__(self):
      super().__init__()  # in python3, super(Class, self).xxx = super().xxx
      self.setWindowIcon(QtGui.QIcon('cover.png'))
      # self.setWindowTitle("title")
      self.ui = Ui_Menu()
      self.ui.setupUi(self)
      self.setup_control()

  def setup_control(self):
      # TODO
      # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
      # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
      self.ui.RC_RecbeamCal.clicked.connect(self.rc_recbeam_cal_clicked)
      self.ui.RC_TbeamCal.clicked.connect(self.rc_tbeam_cal_clicked)
      self.ui.RC_BeamDsgn.clicked.connect(self.rc_beam_dsgn_clicked)
      self.ui.RC_ColumnCal.clicked.connect(self.rc_column_cal_clicked)

  def rc_recbeam_cal_clicked(self):
    self.hide()
    self.ui=W2Controller()
    self.ui.show()

  def rc_tbeam_cal_clicked(self):
    self.hide()
    self.ui=W3Controller()
    self.ui.show()
  
  def rc_beam_dsgn_clicked(self) :
    self.hide()
    self.ui=W4Controller()
    self.ui.show()

  def rc_column_cal_clicked(self):
    self.hide()
    self.ui=W5Controller()
    self.ui.show()
  

class W2Controller(QtWidgets.QMainWindow,Ui_RcRecBeamCal):
  def __init__(self):
    super(W2Controller,self).__init__()
    self.setupUi(self)
    self.setup_control()


  def setup_control(self):
    self.cnstrctblty='no'
    self.fc.setText('280')
    self.fy.setText('4200')
    self.Mux.setText('0')
    self.Vuy.setText('0')
    self.Tu.setText('0')
    self.closeButton1.clicked.connect(self.closebutton1_clicked)    
    self.constructability.clicked.connect(self.constructability_clicked)
    self.calbutton.clicked.connect(lambda:recbeam_cal_button_clicked(self))
    self.barallowbutton.clicked.connect(lambda:bar_allowable_num_clicked(self,'Beam'))

  def constructability_clicked(self) :
    self.cnstrctblty='yes' if self.constructability.isChecked() else 'no'
    return self.cnstrctblty

  def closebutton1_clicked(self):
    self.hide()
    self.ui=MenuController()
    self.ui.show()

class W3Controller(Ui_RcTBeamCal,W2Controller,QtWidgets.QMainWindow):
  def __init__(self):
    super(W3Controller,self).__init__()
    self.setupUi(self)
    self.setup_control()

  def setup_control(self):
    self.cnstrctblty='no'
    self.fc.setText('280')
    self.fy.setText('4200')
    self.Mux.setText('0')
    self.Vuy.setText('0')
    self.Tu.setText('0')
    self.closeButton1.clicked.connect(self.closebutton1_clicked)    
    self.constructability.clicked.connect(self.constructability_clicked)
    self.calbutton.clicked.connect(lambda:tbeam_cal_button_clicked(self))
    self.barallowbutton.clicked.connect(lambda:bar_allowable_num_clicked(self,'Beam'))

class W4Controller(Ui_RcBeamDsgn,W2Controller,QtWidgets.QMainWindow):
  def __init__(self):
    super(W4Controller,self).__init__()
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
    self.constructability.clicked.connect(self.constructability_clicked)
    self.ConsiderCompressionBar.clicked.connect(self.consider_compression_bar_clicked)
    self.ConsiderTbeam.clicked.connect(self.consider_tbeam_clicked)
    self.dsgnbutton.clicked.connect(lambda:beam_dsgn_button_clicked(self))
    self.closeButton1.clicked.connect(self.closebutton1_clicked)  

  def consider_compression_bar_clicked(self) :
    self.CCompBar='yes' if self.ConsiderCompressionBar.isChecked() else 'no'
    return self.CCompBar
  def consider_tbeam_clicked(self) :
    self.CTbeam='yes' if self.ConsiderTbeam.isChecked() else 'no'
    return self.CTbeam

class W5Controller(Ui_RcColumnCal,W2Controller,QtWidgets.QMainWindow):
  signal=QtCore.pyqtSignal(list)
  def __init__(self):
    super(W5Controller,self).__init__()
    self.setupUi(self)
    self.setup_control()

  def setup_control(self):
    self.cnstrctblty='no'
    self.fc.setText('280')
    self.fy.setText('4200')
    self.Mux.setText('0')
    self.Muy.setText('0')
    self.Pu.setText('0')
    self.closeButton1.clicked.connect(self.closebutton1_clicked)    
    self.constructability.clicked.connect(self.constructability_clicked)
    self.calbutton.clicked.connect(self.calbutton_clicked)
    self.barallowbutton.clicked.connect(lambda:bar_allowable_num_clicked(self,'Column'))
    self.PicChangeButton.clicked.connect(self.picchangeclicked)
    self.signal.connect(self.aa)

  def calbutton_clicked(self):
    self.textBrowser.setText('running.......')
    QtWidgets.QApplication.processEvents()
    column_cal_button_clicked(self)

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



