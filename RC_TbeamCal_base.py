import math
import numpy as np
from beam_function import *

def tbeam_cal_button_clicked(data):
    try :
        B=float(data.width.text())
        D=float(data.depth.text())
        hf=float(data.hf.text())
        length=float(data.length.text())
        Sn=float(data.Sn.text())
        BeamCondition=data.beam_condition.currentText()
        fy=float(data.fy.text())
        fc=float(data.fc.text())
        rebar_size1=data.bar1.currentText()
        rebar_size2=data.bar2.currentText()
        tensilebar_num=int(data.barnum1.text())
        compressionbar_num=int(data.barnum2.text())
        stirrup_size=data.stirrup_size.currentText()
        stirrup_num=stirrup_info(data.stirrup_num.currentText())
        stirrup_span=float(data.stirrup_span.text()) #cm
        cnstrctblty=data.cnstrctblty
        Mux=float(data.Mux.text()) #tf-m
        Vuy=float(data.Vuy.text()) #tf

        PrtctT=get_clear_cover('Beam') #cm
        bar_allowable_num_clicked(data,'Beam')
        #計算有效翼寬
        be=cal_effective_width(BeamCondition,B,Sn,hf,length)

        [beta,Ec,bard1,Ab_rebar1,bard2,Ab_rebar2,As,Ass,d,dt,dd,db_stirrup,Ab_stirrup,\
            RebarAllowabelNumPerRow1,RebarAllowabelNumPerRow2]=get_section_info(B,D,fc,fy,\
            rebar_size1,rebar_size2,tensilebar_num,compressionbar_num,stirrup_size,PrtctT,cnstrctblty,"Beam")
        
        #計算彎矩強度
        [Asy,result0,c,Cc,Cs,Mn]=cal_tbeam_Mn(dd,beta,hf,fc,fy,B,d,be,Ass,As)
        [es,et,result1,result2,phi]=cal_phi(c,d,dt)

        #剪力強度計算
        [Av,Vc,phiVn]=cal_shear_strngth(db_stirrup,stirrup_num,stirrup_span,fc,fy,B,d)
        [s_max]=check_stirrup_span_limit(Vuy,Vc,fc,fy,B,d,Av)

        #結果輸出
        info1='d= '+str(round(d,2))+'  cm'
        info2='d\'= '+str(round(dd,2))+'  cm'
        info3='dt= '+str(round(dt,2))+'  cm'
        info4='be= '+str(round(be,2))+'  cm'
        info5='As= '+str(round(As,2))+'  cm^2'
        info6='As\'= '+str(round(Ass,2))+'  cm^2'
        info7='Asy= '+str(round(Asy,2))+'  cm^2'
        info8='c= '+str(round(c,2))+'  cm'
        info9='\u03b5 s= '+str(round(es,5))
        info10='\u03b5 t= '+str(round(et,5))
        info11='Cc= '+str(round(Cc/1000,2))+'  tonf'
        info12='Cs= '+str(round(Cs/1000,2))+'  tonf'
        result1='\u03d5 Mn= '+str(round(phi,3))+'x'+str(round(Mn,2))+'='+str(round(phi*Mn,2))+'  tf-m'
        result2='M ratio= '+str(round(Mux/phi/Mn,3))
        result3='\u03d5 Vn= '+str(round(phiVn,2)) +'  tf'
        result4='V ratio= '+str(round(Vuy/phiVn,3))
        result5='最大剪力筋間距= '+str(s_max) +'  mm'
        
        data.textBrowser.setText((result0+'\n'+info1+'\n'+info2+'\n'+info3+'\n'+info4+'\n'+info5+'\n'+info6+'\n'+
                                     info7+'\n'+info8+'\n'+info9+'\n'+info10+'\n'+result2+'\n'+info11+'\n'+info12+'\n'
                                     +result1+'\n'+result2+'\n'+result3+'\n'+result4+'\n'+result5 ))

        #畫圖
        BarAllowabelNumPerRow=[RebarAllowabelNumPerRow1,RebarAllowabelNumPerRow1]
        BarNum=[tensilebar_num,compressionbar_num]
        data.rctbeamwidget.rctbeamdraw_info(data,BarNum,BarAllowabelNumPerRow,db_stirrup,bard1,bard2,be,BeamCondition)
    except :
        data.textBrowser.setText('Please input the parameters')




