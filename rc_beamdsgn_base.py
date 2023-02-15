import math
import numpy as np
from rc_recbeamcal_base import math2, cal_recbeam_Mn,cal_phi,cal_effectived_beta
from rc_tbeamcal_base import cal_effective_width,math2

def beam_dsgn_button_clicked(data):
    try :
        B=float(data.width.text())
        D=float(data.depth.text())
        hf=float(data.hf.text())
        length=float(data.length.text())
        Sn=float(data.Sn.text())
        BeamCondition=data.beam_condition.currentText()
        fy=float(data.fy.text())
        fc=float(data.fc.text())
        Mu_left_minus=float(data.Mu_left_minus.text())
        Mu_mid_minus=float(data.Mu_mid_minus.text())
        Mu_rght_minus=float(data.Mu_rght_minus.text())
        Mu_left_plus=float(data.Mu_left_plus.text())
        Mu_mid_plus=float(data.Mu_mid_plus.text())
        Mu_rght_plus=float(data.Mu_rght_plus.text())
        Mu=[Mu_left_minus,Mu_left_plus,
            Mu_mid_minus,Mu_mid_plus,
            Mu_rght_minus,Mu_rght_plus]
        Vu_left=float(data.Vg_left.text())
        Vu_mid=float(data.Vg_mid.text())
        Vu_rght=float(data.Vg_rght.text())
        Vg=[Vu_left,Vu_mid,Vu_rght]

        #initial設計參數
        d=D-7 #cm
        dd=7 #cm
        stirrup_num=2
        stirrup_d=1.27 #cm
        #計算有效翼寬
        be=cal_effective_width(BeamCondition,B,Sn,hf,length)

        #配筋設計
        As_dsgn=[]
        Ass_dsgn=[]
        #計算拉筋應變=0.005時所能提供的彎矩
        [phiMn_rec_tcs,rec_As1]=cal_rec_tensioncontrol_single_Mnmax(B,d,fc,fy)
        [phiMn_T_tcs,T_As1]=cal_t_tensioncontrol_single_Mnmax(B,d,hf,be,fc,fy)
        for i in range(6) :
            if i%2==0 :
                #負彎矩
                input=[rec_As1,phiMn_rec_tcs,'矩形']
            else :
                 #正彎矩
                if data.CTbeam=='no' :
                    input=[rec_As1,phiMn_rec_tcs,'矩形']
                else :
                    input=[T_As1,phiMn_T_tcs,'T形']
            [As_dsgn_sg,Ass_dsgn_sg]=dsgn_beam_As(B,d,dd,be,hf,fc,fy,input[0],Mu[i],input[1],input[2])
            As_dsgn.append(As_dsgn_sg)
            Ass_dsgn.append(Ass_dsgn_sg)
        As_final=[]
        #最小鋼筋量
        As_min=max(0.8*fc**0.5/fy*B*D,14/fy*B*D) #cm2
        #考慮耐震梁限制
        As_seismic1=max(As_dsgn[0],As_dsgn[4])/4
        for i in range(6) :
            if i%2==0 :
                As_final.append(max(As_dsgn[i],Ass_dsgn[i+1],As_min,As_seismic1))
            else :
                As_final.append(max(Ass_dsgn[i-1],As_dsgn[i],As_min,As_seismic1))
        #耐震梁規範
        As_final[1]=max(As_final[1],As_final[0]/2)
        As_final[5]=max(As_final[5],As_final[4]/2)

        #根據所需鋼筋量進行配筋
        ########Design Strategy###########
        [barchart,barinfo]=BarDsgn(data,max(As_final))
        if barinfo['#8'][3] <=1.4*barinfo['#8'][2] :
            choose_bar='#8'
        elif barinfo['#9'][3] <= 1.4*barinfo['#9'][2] :
            choose_bar='#9'
        else :
            choose_bar='#10'

        dsgn_barnum=[]
        arrange=[]
        for i in range(6) :
            dsgn_barnum.append(math.ceil(As_final[i]/barinfo[choose_bar][1]))
            arrange.append('雙排') if dsgn_barnum[i]>barinfo[choose_bar][2] else arrange.append('單排')
        
        #檢核彎矩強度與最外鋼筋拉應變限制
        [phiMn_all,et_all,bar_ratio]=CheckMratio(barinfo,choose_bar,dsgn_barnum,arrange,B,D,fc,fy)

        #剪力需求計算
        Mpr=cal_Mpr(barinfo,choose_bar,dsgn_barnum,arrange,B,D,fc,fy) #tf-m
        Vsway=[(Mpr[0]+Mpr[3])/(length/100),(Mpr[1]+Mpr[2])/((length-B)/100)] #tf 假設柱尺寸=梁寬
        Ve1=max(abs(Vg[0]+Vsway[0]),abs(Vg[0]-Vsway[1]))
        Ve2=max(abs(Vg[2]-Vsway[0]),abs(Vg[2]+Vsway[1]))
        Ve=max(Ve1,Ve2)

        #剪力鋼筋設計(已考慮耐震特別規範)
        s_dsgn_all=[0,0] #mm
        choose_stirrup=['#3','#3']
        stir_result=['none','none']
        choose_stirrup_num=[2,2]
        #塑鉸區
        if max(Vsway) > 0.5*Ve : #假設梁受軸力很小
            # Av=stirrup_num*math.pi*stirrup_d**2/4 #cm2
            # s_hinge_req=Av*(fy/1000)*d/(Ve/0.75)*10 #mm  
            Vc=0.53*fc**0.5*B*d/1000 #tf
            [choose_stirrup[0],choose_stirrup_num[0],s_hinge_req,stir_result[0]]=Stirrup_Dsgn(Ve+0.75*Vc,fc,fy,B,d,barinfo)
        else :
            [choose_stirrup[0],choose_stirrup_num[0],s_hinge_req,stir_result[0]]=Stirrup_Dsgn(Ve,fc,fy,B,d,barinfo)
        s_min=min(d/4,15,6*barinfo[choose_bar][0]) #cm
        s_hinge_dsgn=min(s_min*10,s_hinge_req) #mm
        s_hinge_dsgn=math.floor(s_hinge_dsgn/25)*25 #mm
        s_dsgn_all[0]=s_hinge_dsgn #mm
        #非塑鉸區
        Vu_nhinge=Vg[1]+max(Vsway)
        [choose_stirrup[1],choose_stirrup_num[1],s_dsgn_all[1],stir_result[1]]=Stirrup_Dsgn(Vu_nhinge,fc,fy,B,d,barinfo)


        #伸展長度計算   
        dvlpmnt_length=cal_development_length(fc,fy,barinfo,choose_bar)
        

        #結果輸出
        location=['左端負彎矩','左端正彎矩','中央負彎矩','中央正彎矩','右端負彎矩','右端正彎矩']
        location2=['左端剪力 :','中央剪力 :','右端剪力 :']
        result1=''
        result2='塑鉸區剪力需求　Vu= '+str(round(Ve,2))+' tonf\n'+'非塑鉸區剪力需求　Vu= '+str(round(Vu_nhinge,2))+' tonf\n'
        for i in range(6) :
            result1=(result1+str(i+1)+'. '+location[i]+':  撓曲鋼筋設計 '+str(dsgn_barnum[i])+'-'+str(choose_bar)+' ('
                    +str(arrange[i])+'),  '+'\u03d5 Mn= '+str(round(phiMn_all[i],2))+'  tf-m, '
                    +'\u03b5 t= '+str(round(et_all[i],5)) +', 鋼筋比 \u03c1= '+str(round(bar_ratio[i],3))+'\n')
        x=[0,1,0]
        for i in range(len(x)) :
            result2=(result2+location2[i]+stir_result[x[i]]+'\n')
        result=(result1+result2)

        data.textBrowser.setText(result)

        #畫圖
        data.rcbeamdsgnwidget.rcbeamdsgndraw_info(data,choose_bar,dsgn_barnum,s_dsgn_all,choose_stirrup,choose_stirrup_num,barinfo)
     

    except :
        data.textBrowser.setText('Please input the parameters')

def dsgn_beam_As(B,d,dd,be,hf,fc,fy,As1,Mu,phiMn_tcs,shape) :
    #拉控斷面配筋法
    if Mu>phiMn_tcs :
        #雙筋
        Mn2_req=(Mu-phiMn_tcs)/0.9
        Ass_dsgn=Mn2_req*1000*100/(d-dd)/(fy-0.85*fc) #cm2
        As2=Mn2_req*1000*100/(d-dd)/fy
        As_dsgn=As1+As2
    else :
        #單筋
        Mn_req=Mu/0.9

        if shape=='矩形' :
            As_dsgn=dsgn_recbeam_single_As(B,d,fc,fy,Mn_req)
        elif shape=='T形' :
            As_dsgn=dsgn_tbeam_single_As(B,d,be,hf,fc,fy,Mn_req)
        Ass_dsgn=0
    return As_dsgn, Ass_dsgn
    

def dsgn_recbeam_single_As(B,d,fc,fy,Mn_req) :
    #前提拉筋要降伏
    m=fy/(0.85*fc)
    Rn=Mn_req*1000*100/(B*d**2)
    rho_req=1/m*(1-(1-2*m*Rn/fy)**0.5)
    As_req=rho_req*B*d
    return As_req

def dsgn_tbeam_single_As(B,d,be,hf,fc,fy,Mn_req) :
    Mn_dot=0.85*fc*be*hf*(d-hf/2)/1000/100 #tf-m
    if Mn_req>Mn_dot :
        Mn1=0.85*fc*(be-B)*hf*(d-hf/2)/1000/100
        Mn2=Mn_req-Mn1
        matha=0.85*fc*B/2
        mathb=-0.85*fc*B*d
        mathc=Mn2*1000*100
        a=min(math2(matha,mathb,mathc))
        As_req=0.85*fc*((be-B)*hf+B*a)/fy
    else :
        As_req=dsgn_recbeam_single_As(be,d,fc,fy,Mn_req)
    return As_req
    

def cal_rec_tensioncontrol_single_Mnmax(B,d,fc,fy) :
    c=3/8*d #cm
    #計算beta1值
    beta=0.85 if fc <= 280  else max(0.65,0.85-0.05/70*(fc-280))
    a=beta*c #cm
    phiMn=0.9*0.85*fc*B*a*(d-a/2)/1000/100 #tf-m
    As=0.85*fc*B*a/fy #cm2
    return phiMn,As

def cal_t_tensioncontrol_single_Mnmax(B,d,hf,be,fc,fy):
    c=3/8*d #cm
    #計算beta1值
    beta=0.85 if fc <= 280  else max(0.65,0.85-0.05/70*(fc-280))
    a=beta*c #cm
    if a<=hf :
        phiMn=0.9*0.85*fc*be*a*(d-a/2)/1000/100 #tf-m
        As=0.85*fc*be*a/fy #cm2
    else :
        Mn1=0.85*fc*B*a*(d-a/2)/1000/100 #tf-m
        Mn2=0.85*fc*(be-B)*hf*(d-hf/2)/1000/100 #tf-m
        phiMn=0.9*(Mn1+Mn2)
        As=0.85*fc*(B*a+(be-B)*hf)/fy #cm2
    return phiMn,As


def BarDsgn(data,As):
    B=float(data.width.text())
    #1st:直徑 2nd:面積 3rd:單排最大容許 4th:需要幾根 
    barinfo={'#3':[0.953,0.7133,0,0], '#4':[1.27,1.267,0,0], '#5':[1.588,1.986,0,0],
              '#6':[1.905,2.865,0,0], '#7':[2.223,3.871,0,0],'#8':[2.54,5.067,0,0],
              '#9':[2.865,6.469,0,0],'#10':[3.226,8.143,0,0],'#11':[3.581,10.07,0,0]}
    barchart=['#3', '#4','#5','#6','#7', '#8','#9','#10','#11']
    for i in range(len(barchart)) :
        cleardb_h=1.5*max(2.5,barinfo[barchart[i]][0]) if data.cnstrctblty=='yes'  else max(2.5,barinfo[barchart[i]][0])
        barinfo[barchart[i]][2]=max(0,math.floor((B-8-2.54+cleardb_h)/(barinfo[barchart[i]][0]+cleardb_h)))
        barinfo[barchart[i]][3]=math.ceil(As/ barinfo[barchart[i]][1])
    return barchart,barinfo

def CheckMratio(barinfo,choose_bar,dsgn_barnum,arrange,B,D,fc,fy) :
    phiMn_all=[]
    et_all=[]
    bar_ratio=[]
    for i in range(6) :
        bard=barinfo[choose_bar][0]
        barA=barinfo[choose_bar][1]
        BarNumCal=dsgn_barnum[i//2*2:i//2*2+2]
        arrange_use=arrange[i//2*2:i//2*2+2]
        BarNumMax_PerRow=[barinfo[choose_bar][2],barinfo[choose_bar][2]]
        if i%2==1 :
            BarNumCal=list(reversed(BarNumCal)) 
            arrange_use=list(reversed(arrange_use))
        [d,dt,dd,beta]=cal_effectived_beta(arrange_use,D,4,bard,bard,fc,barinfo['#4'][0],
                                            BarNumCal,BarNumMax_PerRow)                                 
        [Asy,result0,c,Cc,Cs,Mn]=cal_recbeam_Mn(dd,fc,beta,B,d,fy,BarNumCal[1]*barA,BarNumCal[0]*barA)
        [es,et,result1,result2,phi]=cal_phi(c,d,dt)
        phiMn_all.append(phi*Mn)
        et_all.append(et)
        bar_ratio.append(dsgn_barnum[i]*barinfo[choose_bar][1]/B/d)
    return  phiMn_all,et_all,bar_ratio

def Stirrup_Dsgn(Vu,fc,fy,B,d,barinfo) :
    #無軸壓
    Vc=0.53*fc**0.5*B*d/1000 #tf
    Vs_req=max(0,Vu/0.75-Vc)
    Av_s_req=Vs_req*1000/(fy*d) #cm
    Av_s_max=4*Vc*1000/(fy*d) #cm
    if Av_s_req>Av_s_max :
        Av_s_req=Av_s_max
        stir_result='剪力筋強度需求超過4Vc，請放大梁寬'
    else :
        stir_result='剪力筋強度需求滿足限制，無須調整梁寬'
    ########Design Strategy############
    stirrup_num=2
    if Av_s_req<=0.071 : # #3@200mm 單箍
        choose_stirrup='#3'
    elif Av_s_req<=0.254 : # #4@100m　單箍
        choose_stirrup='#4'
    elif Av_s_req<=0.398 : #5@100m　單箍
        choose_stirrup='#5'
    else :
        choose_stirrup='#5'
        stirrup_num=4
    Av=stirrup_num*barinfo[choose_stirrup][1] #cm2

    if Av_s_req==0 :
        s_req=600 #mm
    else :
        s_req=Av/Av_s_req*10 #mm
 
    if Vs_req<=2*Vc :
        s_max=min(d/2,60)
    else :
        s_max=min(d/4,30)
    s_dsgn=min(s_req,s_max*10) #mm
    s_dsgn=math.floor(s_dsgn/25)*25 #mm
    return choose_stirrup,stirrup_num,int(s_dsgn),stir_result

def cal_Mpr(barinfo,choose_bar,dsgn_barnum,arrange,B,D,fc,fy) :
    #以單筋矩形梁計算Mpr
    Mpr=[]
    for i in [0,1,4,5] :
        bard=barinfo[choose_bar][0]
        barA=barinfo[choose_bar][1]
        As=dsgn_barnum[i]*barA
        BarNumCal=[dsgn_barnum[i],0]
        arrange_use=[arrange[i],'單排']
        BarNumMax_PerRow=[barinfo[choose_bar][2],barinfo[choose_bar][2]]
        [d,dt,dd,beta]=cal_effectived_beta(arrange_use,D,4,bard,bard,fc,barinfo['#4'][0],
                                            BarNumCal,BarNumMax_PerRow)   
        a=1.25*fy*As/(0.85*fc*B) #cm
        Mpr.append(1.25*fy*As*(d-a/2)/100/1000) #tf-m
    return Mpr

def cal_development_length(fc,fy,barinfo,choose_bar) :
    Psi_e=1.3 #頂層鋼筋修正
    Psi_t=1 #鋼筋塗佈修正
    lumbda=1.0 #輕質骨材混凝土修正
    dvlpmnt_length=max(0.19*barinfo[choose_bar][0]*fy*Psi_e*Psi_t*lumbda/(fc**0.5),30)
    return dvlpmnt_length

