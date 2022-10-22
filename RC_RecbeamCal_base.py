import math
from beam_function import *

def RecBeamCalButtonClicked(data):
    try :
        B=float(data.width.text()) #cm
        D=float(data.depth.text()) #cm
        fy=float(data.fy.text()) #kgf/cm2
        fc=float(data.fc.text()) #kgf/cm2
        rebar_size1=data.bar1.currentText()
        rebar_size2=data.bar2.currentText()
        tensilebar_num=int(data.barnum1.text())
        compressionbar_num=int(data.barnum2.text())
        stirrup_size=data.stirrup_size.currentText()
        stirrup_span=float(data.stirrup_span.text()) #cm
        stirrup_num=stirrup_info(data.stirrup_num.currentText())
        cnstrctblty=data.cnstrctblty
        Mux=float(data.Mux.text()) #tf-m
        Vuy=float(data.Vuy.text()) #tf
        
        PrtctT=get_clear_cover('Beam') #cm
        BarAllowabelNumClicked(data,'Beam')

        
        [beta,Ec,bard1,Ab_rebar1,bard2,Ab_rebar2,As,Ass,d,dt,dd,db_stirrup,Ab_stirrup,\
            RebarAllowabelNumPerRow1,RebarAllowabelNumPerRow2]=get_section_info(B,D,fc,fy,\
            rebar_size1,rebar_size2,tensilebar_num,compressionbar_num,stirrup_size,PrtctT,cnstrctblty,"Beam")

        #檢核壓筋是否降伏
        [Asy,result0,c,Cc,Cs,Mn]=Cal_Recbeam_Mn(dd,fc,beta,B,d,fy,Ass,As)
        [es,et,result1,result2,phi]=cal_phi(c,d,dt)

        #剪力強度計算
        [Av,Vc,phiVn]=cal_shear_strngth(db_stirrup,stirrup_num,stirrup_span,fc,fy,B,d)
        [s_max]=check_stirrup_span_limit(Vuy,Vc,fc,fy,B,d,Av)

        #結果輸出
        info1='d= '+str(round(d,2))+'  cm'
        info2='d\'= '+str(round(dd,2))+'  cm'
        info3='dt= '+str(round(dt,2))+'  cm'
        info4='As= '+str(round(As,2))+'  cm^2'
        info5='As\'= '+str(round(Ass,2))+'  cm^2'
        info6='Asy= '+str(round(Asy,2))+'  cm^2'
        info7='c= '+str(round(c,2))+'  cm'
        info8='\u03b5 s= '+str(round(es,5))
        info9='\u03b5 t= '+str(round(et,5))
        info10='Cc= '+str(round(Cc/1000,2))+'  tonf'
        info11='Cs= '+str(round(Cs/1000,2))+'  tonf'
        result3='\u03d5 Mn= '+str(round(phi,3))+'x'+str(round(Mn,2))+'= '+str(round(phi*Mn,2))+'  tf-m'
        result4='M ratio= '+str(round(Mux/phi/Mn,3))
        result5='\u03d5 Vn= '+str(round(phiVn,2)) +'  tf'
        result6='V ratio= '+str(round(Vuy/phiVn,3))
        result7='最大剪力筋間距= '+str(s_max) +'  mm'
        data.textBrowser.setText((result0+'\n'+result1+'\n'+info1+'\n'+info2+'\n'+info3+'\n'+info4+'\n'+info5+'\n'+info6+'\n'+
                                    info7+'\n'+info8+'\n'+info9+'\n'+result2+'\n'+info10+'\n'+info11+'\n'+result3+'\n'+result4+'\n'
                                    +result5+'\n'+result6+'\n'+result7+'\n' ))
        #畫圖
        BarAllowabelNumPerRow=[RebarAllowabelNumPerRow1,RebarAllowabelNumPerRow1]
        BarNum=[tensilebar_num,compressionbar_num]
        data.rcrecbeamwidget.rcrecbeamdraw_info(data,BarNum,BarAllowabelNumPerRow,db_stirrup,bard1,bard2)
    except :
        data.textBrowser.setText('Please input the parameters')






