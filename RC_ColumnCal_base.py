import math
from beam_function import stirrup_info,get_clear_cover,BarAllowabelNumClicked,cal_shear_strngth,check_stirrup_span_limit
from column_function import get_column_section_info,get_rebar_df,get_theta,get_alpha, \
                            build_column_ord,cal_distance_from_point_to_line,find_interaction_point,modify_interaction_diagram,get_pmmratio,\
                            get_mm_diagram
import numpy as np
import pandas as pd
from  DataFrameModel import  DataFrameModel

def ColumnCalButtonClicked(data):
    try :
        # data=self
        B=float(data.width.text()) #cm
        D=float(data.depth.text()) #cm
        fy=float(data.fy.text()) #kgf/cm2
        fc=float(data.fc.text()) #kgf/cm2
        rebar_size1=data.bar1.currentText()
        rebar_size2=data.bar2.currentText()
        Nx=int(data.barnum1.text())
        Ny=int(data.barnum2.text())
        stirrup_size=data.stirrup_size.currentText()
        stirrup_span=float(data.stirrup_span.text()) #cm
        stirrup_num=stirrup_info(data.stirrup_num.currentText())
        cnstrctblty=data.cnstrctblty
        Mux=float(data.Mux.text()) #tf-m
        Muy=float(data.Muy.text()) #tf-m
        Pu=float(data.Pu.text()) #tf

        [beta,Ec,db_rebar1,Ab_rebar1,db_rebar2,Ab_rebar2,db_stirrup,Ab_stirrup]=get_column_section_info(B,D,fc,fy,rebar_size1,rebar_size2,stirrup_size)
        PrtctT=get_clear_cover('Column') #cm
        cover=PrtctT+db_stirrup+db_rebar1
        rebar_df=get_rebar_df(B,D,cover,Nx,Ny,Ab_rebar1,Ab_rebar2)
        Ast=rebar_df["Ab"].sum()
        Es=2040000 #kgf/cm2
        BarAllowabelNumClicked(data,'Column')
        theta=get_theta(Mux,Muy)
        Mu=math.sqrt((Mux)**2+(Muy)**2)
        Pno=round((0.85*fc*(B*D-Ast)+Ast*fy)/1000,1) #tf
        Pnmax=0.8*Pno
        phi_Pnmax=round(0.65*Pnmax,1)
        Pnt=round(-Ast*fy/1000,2) #tf

        #///////////////////////////////畫PMM互制曲線///////////////////////////////
        #假設中性軸角度
        alpha=get_alpha(B,D,rebar_df,theta,Es,Ec)
        concrete_df=build_column_ord(B,D)
        d_max=2*cal_distance_from_point_to_line(concrete_df.loc['p1','x0'],concrete_df.loc['p1','y0'],math.tan(math.radians(alpha)),-1,0)
        #find interaction diagram
        c_trial_1=np.linspace(0.05*min(B,D),3/5*max(B,D),15)
        c_trial_2=np.linspace(3/5*max(B,D),2*max(B,D),15)
        c_trial=np.concatenate([c_trial_1,c_trial_2])
        interaction_diagram=pd.DataFrame(columns=["c","phi","Pn","Mnx","Mny","theta"])
        interaction_diagram.loc[0]=[None,0.9,Pnt,0,0,0]
        for i in range(c_trial.shape[0]) :
            [Pn, Mnx, Mny,phi]=find_interaction_point(B,D,concrete_df,alpha,beta,c_trial[i],d_max,fc,rebar_df,Es,fy)
            theta_trial=round(get_theta(abs(Mnx),abs(Mny)),1)
            interaction_diagram.loc[i+1]=[round(c_trial[i],2),phi,Pn,Mnx,Mny,theta_trial]
        interaction_diagram=modify_interaction_diagram(interaction_diagram,Pno,phi_Pnmax)
        capacity_point,pmm_ratio=get_pmmratio(interaction_diagram,Pu,Mu)

        mm_diagram=get_mm_diagram(Pu,Pno,Pnt,B,D,fc,fy,Es,beta,concrete_df,rebar_df)
        # print(mm_diagram)
        #剪力強度計算
        eff_d1=D-PrtctT-db_stirrup-db_rebar1/2
        eff_d2=B-PrtctT-db_stirrup-db_rebar2/2
        [Av,Vc,phiVny]=cal_shear_strngth(db_stirrup,stirrup_num,stirrup_span,fc,fy,B,eff_d1)
        [Av,Vc,phiVnx]=cal_shear_strngth(db_stirrup,stirrup_num,stirrup_span,fc,fy,D,eff_d2)


        # #結果輸出
        info1='Ast= '+str(round(Ast,2))+'  cm^2'
        info2='鋼筋比= '+str(round(Ast/(B*D)*100,3))+' %'
        info3='Pno= '+str(round(Pno,1))+'  tonf'
        info4='Pnmax= '+str(round(Pnmax,1))+'  tonf'
        info5='\u03d5 Pno= '+str(round(0.65*Pno,1))+'  tonf'
        info6='\u03d5 Pnmax= '+str(round(0.65*Pnmax,1))+'  tonf'
        info7='理論 \u03B8 = '+str(round(theta,1))+'  °'
        info8='假設 \u03B1 = '+str(round(alpha,1))+'  °'
        result4='PMM ratio= '+str(pmm_ratio)
        result5='\u03d5 Vn= '+str(round(phiVny,2)) +'  tf'
        result6='\u03d5 Vn= '+str(round(phiVnx,2)) +'  tf'
        data.textBrowser.setText((info1+'\n'+info2+'\n'+info3+'\n'+info4+'\n'+info5+'\n'+info6+'\n'
                                +info7+'\n'+info8+'\n'+result4+'\n'+result5+'\n'+result6+'\n'))

        #畫圖
        data.rccolumnwidget.rccolumndraw_info(data,Nx,Ny,db_stirrup,db_rebar1,db_rebar2,PrtctT)
        data.signal.emit([interaction_diagram, mm_diagram, capacity_point,Mux,Muy,Mu,Pu])

    except :
        data.textBrowser.setText('Please input the parameters')

