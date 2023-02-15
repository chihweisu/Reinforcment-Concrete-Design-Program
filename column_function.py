from cmath import atan
import numpy as np
import pandas as pd
import math
from beam_function import get_beta, get_EandG_vaule,rebar_info,cal_d_eff

def get_column_section_info(B,D,fc,fy,bar1,bar2,stirrup_size):
    beta=get_beta(fc)
    Ec,ShearM=get_EandG_vaule(fc)
    [db_rebar1,Ab_rebar1]=rebar_info(bar1)
    [db_rebar2,Ab_rebar2]=rebar_info(bar2)
    [db_stirrup,Ab_stirrup]=rebar_info(stirrup_size)
    return beta,Ec,db_rebar1,Ab_rebar1,db_rebar2,Ab_rebar2,db_stirrup,Ab_stirrup


def get_rebar_df(B,D,cover,Nx,Ny,Ab_rebar1,Ab_rebar2):
    layers=[ i+1 for i in range((Nx+Ny)*2-4)]
    df=pd.DataFrame(columns=["x0","y0","Ab","x0^2Ab","y0^2Ab","y_alpha","yy_alpha","epsilon","fs","FsandT"],index=layers)
    span_x=(B-2*cover)/(Nx-1)
    span_y=(D-2*cover)/(Ny-1)
    x_ord=[cover-B/2+span_x*i for i in range(Nx)]
    y_ord=[cover-D/2+span_y*(i+1) for i in range(Ny-2)]
    ord=[]
    Ab=[]
    for i in [cover-D/2,D/2-cover]:
        for j in x_ord :
            ord.append([j,i])
            Ab.append(Ab_rebar1)
    for i in [cover-B/2,B/2-cover]:
        for j in y_ord:
            ord.append([i,j])
            Ab.append(Ab_rebar2)
    for i in range(len(ord)) :
        df.loc[i+1,'x0']=ord[i][0]
        df.loc[i+1,'y0']=ord[i][1]
        df.loc[i+1,'Ab']=Ab[i]
    df["x0^2Ab"]=df["x0"]**2*df["Ab"]
    df["y0^2Ab"]=df["y0"]**2*df["Ab"]
    return df
    
def get_theta(Mux,Muy):
    theta=np.degrees(math.atan2(Muy,Mux))
    return theta

def get_alpha(B,D,df,theta,Es,Ec):
    Ix=B*D**3/12+sum(df['y0^2Ab'])*Es/Ec
    Iy=D*B**3/12+sum(df['x0^2Ab'])*Es/Ec
    # print('Ix=',Ix,'Iy',Iy)
    alpha=math.degrees(math.atan2(Ix/Iy*math.tan(math.radians(theta)),1))
    return alpha

def build_column_ord(B,D):
    layers=['p1','p2','p3','p4','np1','np2']
    df=pd.DataFrame([[-B/2,D/2],[-B/2,-D/2],[B/2,-D/2],[B/2,D/2],[None,None],[None,None]],columns=["x0","y0"],index=layers)
    return df

def find_intersection(B,D,alpha,n):
    m=math.tan(math.radians(alpha))
    if math.radians(alpha)==0:
        point=[[B,D],[B,D],[-B/2,-m*B/2+n],[B/2,m*B/2+n]]
    elif math.radians(alpha)==90:
        point=[[(-D/2-n)/m,-D/2],[(D/2-n)/m,D/2],[B,D],[B,D]]
    else :
        point=[[(-D/2-n)/m,-D/2],[(D/2-n)/m,D/2],[-B/2,-m*B/2+n],[B/2,m*B/2+n]]
    intersection=[]
    record=[]
    j=1
    # print("point=",point)
    for i in point:
        if i[0]>=-B/2 and i[0]<=B/2 and i[1]>=-D/2 and i[1]<=D/2:
            intersection.append(i)
            record.append(j)
        j+=1
    # print('intersection=',intersection)
    intersection.sort()
    # print("record=",record)
    if {1,2}.issubset(record) :
        stress_block_shape=['np1','np2','p1','p2']
    elif {2,3}.issubset(record) :
        stress_block_shape=['np1','np2','p1']
    elif {3,4}.issubset(record) :
        stress_block_shape=['np1','np2','p4','p1']       
    elif {1,4}.issubset(record) :
        stress_block_shape=['np1','np2','p4','p1','p2']  
    else :
        stress_block_shape=['p1','p2','p3','p4']
    return intersection,  stress_block_shape

#迭代 C畫出互制曲線
def find_interaction_point(B,D,concrete_df,alpha,beta,c,d_max,fc,rebar_df,Es,fy):
    d_max=2*cal_distance_from_point_to_line(concrete_df.loc['p1','x0'],concrete_df.loc['p1','y0'],math.tan(math.radians(alpha)),-1,0)
    delta=((d_max/2-c)+(1-beta)*c)/math.cos(math.radians(alpha))
    intersection,  stress_block_shape=find_intersection(B,D,alpha,delta)
    try:
        concrete_df.loc['np1']=intersection[0]
        concrete_df.loc['np2']=intersection[1]
    except:
        pass
    # print( stress_block_shape)
    points_ord=[[concrete_df.loc[i,'x0'],concrete_df.loc[i,'y0']] for i in  stress_block_shape]
    # print(points_ord)
    [Cc,Mnx_rc,Mny_rc]=cal_Cc(points_ord,fc,c)
    [rebar_df,Fs,Mnx_s,Mny_s]=cal_Fs_T(rebar_df,alpha,d_max,c,beta,Es,fc,fy)
    Pn=Cc+Fs
    Mnx=Mnx_rc+Mnx_s
    Mny=Mny_rc+Mny_s
    phi=get_phi(abs(rebar_df["epsilon"].min()))
    # print(rebar_df)
    # print(np.degrees(math.atan2(Mny,Mnx)))
    return round(Pn,2), round(Mnx,2), round(Mny,2), round(phi,2)

def cal_Cc(points_ord,fc,c):
    if c<=0 :
        Cc=0
        Mnx_rc=0
        Mny_rc=0
    else :
        Area_comp= cal_area(np.array(points_ord))
        xc,yc=cal_centroid(np.array(points_ord))
        Cc=0.85*fc*Area_comp/1000 #tf
        Mnx_rc=Cc*yc/100 #tf-m
        Mny_rc=Cc*xc/100 #tf-m

    return Cc,Mnx_rc,Mny_rc

def cal_Fs_T(df,alpha,d_max,c,beta,Es,fc,fy):
    df["y_alpha"]=df["y0"]*math.cos(math.radians(alpha))-df["x0"]*math.sin(math.radians(alpha))
    df["yy_alpha"]=d_max/2-df["y_alpha"]
    df["epsilon"]=0.003*(1-df["yy_alpha"]/c)
    #///計算鋼筋拉壓力(Fs&T) 並扣除重複計算混凝土壓力
    for i in range(df.shape[0]):
        fs=min(fy,Es*abs(df.loc[i+1,"epsilon"]))*np.sign(df.loc[i+1,"epsilon"]) #kgf/cm2
        df.loc[i+1,"fs"]=round(fs,0)
        Fs=df.loc[i+1,"Ab"]*fs/1000 #tf
        if df.loc[i+1,"yy_alpha"]<beta*c :
            df.loc[i+1,"FsandT"]=round(Fs-0.85*fc*df.loc[i+1,"Ab"]/1000,2)
        else :
            df.loc[i+1,"FsandT"]=round(Fs,2)
    df["Mnx_s"]=df["FsandT"]*df["y0"]/100 #tf-m
    df["Mny_s"]=df["FsandT"]*df["x0"]/100 #tf-m
    Fs=df["FsandT"].sum()
    Mnx_s=df["Mnx_s"].sum()
    Mny_s=df["Mny_s"].sum()

    return df,Fs,Mnx_s,Mny_s

def modify_interaction_diagram(interaction_diagram,Pno,phi_Pnmax) :
    interaction_diagram.loc[interaction_diagram.shape[0]]=[None,0.65,Pno,0,0,0]
    interaction_diagram["Mn"]=round((interaction_diagram["Mnx"]**2+interaction_diagram["Mny"]**2)**0.5,2)
    get_phiPn=lambda x: round(min(x,phi_Pnmax),1)
    interaction_diagram["phiPn"]=interaction_diagram["phi"]*interaction_diagram["Pn"]
    interaction_diagram["phiPn"]=interaction_diagram["phiPn"].apply(get_phiPn)
    interaction_diagram["phiMn"]=round(interaction_diagram["phi"]*interaction_diagram["Mn"],2)
    return interaction_diagram

def get_phi(et):
    phi=min(0.9,0.65+0.25/0.003*(et-0.002)) if et>=0.002 else 0.65
    return phi

def get_section_info(B,D,fc,fy,bar1,bar2,stirrup_size,PrtctT,cnstrctblty):
    beta=get_beta(fc)
    Ec,ShearM=get_EandG_vaule(fc)
    [db_rebar1,Ab_rebar1]=rebar_info(bar1)
    [db_rebar2,Ab_rebar2]=rebar_info(bar2)
    [db_stirrup,Ab_stirrup]=rebar_info(stirrup_size)
    return beta,Ec,db_rebar1,Ab_rebar1,db_rebar2,Ab_rebar2,db_stirrup,Ab_stirrup


def cal_centroid(points):
    A = cal_area(points)
    c_x, c_y = 0.0, 0.0
    point_p = points[-1] # point_p 表示前一节点
    for point in points:
        c_x +=((point[0] + point_p[0]) * (point[1]*point_p[0] - point_p[1]*point[0]))
        c_y +=((point[1] + point_p[1]) * (point[1]*point_p[0] - point_p[1]*point[0]))
        point_p = point
    return c_x / (6*A), c_y / (6*A)


def cal_area(vertices): #Gauss's area formula 高斯面积计算
    A = 0.0
    point_p = vertices[-1]
    for point in vertices:
        A += (point[1]*point_p[0] - point[0]*point_p[1])
        point_p = point
    return abs(A)/2


def cal_distance_from_point_to_line(x0,y0,a,b,c):
    #ax+by+c=o
    distance=abs(a*x0+b*y0+c)/math.sqrt(a**2+b**2)
    return distance

def get_pmmratio(interaction_diagram,Pu,Mu):
    demand=math.sqrt(Pu**2+Mu**2)
    angle=get_theta(Mu,Pu)
    for i in range(interaction_diagram.shape[0]) :
        angle2=get_theta(interaction_diagram.loc[i,'phiMn'],interaction_diagram.loc[i,'phiPn'])
        if angle2>=angle :
            points=[interaction_diagram.loc[i-1,['phiMn','phiPn']],interaction_diagram.loc[i,['phiMn','phiPn']]]
            break
    x=np.linspace(points[0][0],points[1][0],20)
    y=np.linspace(points[0][1],points[1][1],20)
    # m_total=[ get_theta(x[i],y[i])-angle for i in range(len(x))]
    n=90
    for i in range(len(x)) :
        m=abs(get_theta(x[i],y[i])-angle)
        if m<n:
            n=m
            answer=[x[i],y[i]]
    capacity=math.sqrt(answer[0]**2+answer[1]**2)
    pmm_ratio=round(demand/capacity,3)
    return answer,pmm_ratio


def get_mm_diagram(Pu,Pno,Pnt,B,D,fc,fy,Es,beta,concrete_df,rebar_df):
    mm_diagram=pd.DataFrame(columns=["alpha","c","phi","Pn","Mnx","Mny","iter"])
    alpha=np.linspace(0,90,21)
    for i in range(len(alpha)):
        d_max=2*cal_distance_from_point_to_line(concrete_df.loc['p1','x0'],concrete_df.loc['p1','y0'],math.tan(math.radians(alpha[i])),-1,0)
        left_pointer=0
        right_pointer=2*max(B,D)
        error=1
        num=0
        while error > 0.05 :
            mid=(left_pointer+right_pointer)/2
            [Pn,Mnx,Mny,phi]=find_interaction_point(B,D,concrete_df,alpha[i],beta,mid,d_max,fc,rebar_df,Es,fy)
            # print(left_pointer,right_pointer,'mid=',mid,'Pn=',Pn)
            if abs(Pu)<=100:
                error=abs((Pn-Pu)/100)
            else :
                error=abs((Pn-Pu)/Pu)
            if Pn<Pu :
                left_pointer=mid
            elif  Pn>Pu :
                right_pointer=mid
            num+=1
            if num>15:
                break
        mm_diagram.loc[i]=[alpha[i],mid,phi,Pn,Mnx,Mny,num]
    return mm_diagram
