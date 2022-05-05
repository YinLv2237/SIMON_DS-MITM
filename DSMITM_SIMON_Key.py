__author__ = 'lv'

from math import *

class DSMIMT_SIMON_Key():
    def __init__(self,blocksize):
        self.blocksize=blocksize
        self.n=blocksize//2
        self.s1=1
        self.s2=8
        self.s3=2

    #生成加密阶段变量
    def genVars_L(self,r):
        return ['L_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_R(self,r):
        return ['R_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_In1_AND(self,r):
        return ['IA1_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_In2_AND(self,r):
        return ['IA2_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_Out_AND(self,r):
        return ['OA_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_Out_S3(self,r):
        return ['S3_'+str(i)+'_r'+str(r) for i in range(self.n)]

    #生成解密阶段变量
    def genVars_DL(self,r):
        return ['DL_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_DR(self,r):
        return ['DR_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_DIn1_AND(self,r):
        return ['DIA1_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_DIn2_AND(self,r):
        return ['DIA2_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_DOut_AND(self,r):
        return ['DOA_'+str(i)+'_r'+str(r) for i in range(self.n)]
    def genVars_DOut_S3(self,r):
        return ['DS3'+str(i)+'_r'+str(r) for i in range(self.n)]

    #生成猜测变量
    def genVars_DGL(self,r):
        return ['DGL_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_In1_AND_Guess(self,r):
        return ['GIA1_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_In2_AND_Guess(self,r):
        return ['GIA2_'+str(j)+'_r'+str(r) for j in range(self.n)]

    #输入轮既存在差分又需要猜测：猜测个数减少
    def genVars_CL(self,r):
        return ['CL_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_CR(self,r):
        return ['CR_'+str(j)+'_r'+str(r) for j in range(self.n)]

    #密钥恢复阶段
    #后向差分
    def genVars_Key_ML(self,r):
        return ['ML_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_MR(self,r):
        return ['MR_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_MS1(self,r):
        return ['MS1_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_MS2(self,r):
        return ['MS2_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_MS3(self,r):
        return ['MS3_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_MA(self,r):
        return ['MA_'+str(j)+'_r'+str(r) for j in range(self.n)]

    #前向决定关系
    def genVars_Key_WL(self,r):
        return ['WL_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_WR(self,r):
        return ['WR_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_WS1(self,r):
        return ['WS1_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_WS2(self,r):
        return ['WS2_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_WS3(self,r):
        return ['WS3_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_WA(self,r):
        return ['WA_'+str(j)+'_r'+str(r) for j in range(self.n)]

    #转化为猜测值
    def genVars_Key_GL(self,r):
        return ['GL_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_GR(self,r):
        return ['GR_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_GS1(self,r):
        return ['GS1_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_GS2(self,r):
        return ['GS2_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_GS3(self,r):
        return ['GS3_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_GA(self,r):
        return ['GA_'+str(j)+'_r'+str(r) for j in range(self.n)]
    def genVars_Key_GK(self,r):
        return ['GK_'+str(j)+'_r'+str(r) for j in range(self.n)]

    def getVariables_From_Constraints(self,C):
        V = set([])
        for s in C:
            temp = s.strip()
            temp = temp.replace('+', ' ')
            temp = temp.replace('-', ' ')
            temp = temp.replace('<', ' ')
            temp = temp.replace('>', ' ')
            temp = temp.replace('>=', ' ')
            temp = temp.replace('<=', ' ')
            temp = temp.replace('=', ' ')
            temp = temp.split()
            for v in temp:
                if not v.isdecimal():
                    V.add(v)

        return V

    #用于生成与和异或操作的约束，若a活跃，则b活跃；否则b不活跃
    def genConstraints_AND_XOR(self,a,b):
        l=len(a)
        C=[]
        C+=[' + '.join(a)+' - '+b+' >= 0']
        C+=[str(l)+' '+b+' - '+' - '.join(a)+' >= 0']
        return C

    #生成加密阶段约束
    def genConstraints_Encrypt(self,r):
        C=[]
        Lr=self.genVars_L(r)
        Rr=self.genVars_R(r)
        Lr1=self.genVars_L(r+1)
        Rr1=self.genVars_R(r+1)
        IA1=self.genVars_In1_AND(r)
        IA2=self.genVars_In2_AND(r)
        OA=self.genVars_Out_AND(r)
        S3=self.genVars_Out_S3(r)

        for i in range(self.n):
            #L0和移位间的约束
            C += [Lr[i]+ ' - ' + IA1[(i-self.s1)%self.n] + ' = 0']
            C += [Lr[i]+ ' - ' + IA2[(i-self.s2)%self.n] + ' = 0']
            C += [Lr[i]+ ' - ' + S3[(i-self.s3)%self.n] + ' = 0']
            C += [Lr[i] + ' - ' + Rr1[i] + ' = 0']
            #AND操作的约束
            C += self.genConstraints_AND_XOR([IA1[i],IA2[i]],OA[i])
            #异或操作的约束
            C += self.genConstraints_AND_XOR([OA[i],S3[i],Rr[i]],Lr1[i])
        return C

    #生成解密阶段约束
    def genConstraints_Decrypt(self,r):
        C=[]
        DLr=self.genVars_DL(r)
        DRr=self.genVars_DR(r)
        DLr1=self.genVars_DL(r+1)
        DRr1=self.genVars_DR(r+1)
        DIA1=self.genVars_DIn1_AND(r)
        DIA2=self.genVars_DIn2_AND(r)
        DOA=self.genVars_DOut_AND(r)
        DS3=self.genVars_DOut_S3(r)

        for i in range(self.n):
            #R1和移位间的约束
            C += self.genConstraints_AND_XOR([DRr1[i],DIA1[(i- self.s1)%self.n],DIA2[(i-self.s2)%self.n],DS3[(i-self.s3)%self.n]],DLr[i])
            #AND操作的约束
            C += [DOA[i] + ' - ' + DIA1[i] + ' = 0']
            C += [DOA[i] + ' - ' + DIA2[i] + ' = 0']
            #异或操作的约束
            C += [DLr1[i] + ' - ' + DS3[i] + ' = 0']
            C += [DLr1[i] + ' - ' + DOA[i] + ' = 0']
            C += [DLr1[i] + ' - ' + DRr[i] + ' = 0']
        return C

    def subfunc_AND(self,Input1,Input2,Doutput,GInput1,GInput2):
        C = []
        C += [GInput1+' - '+Doutput+' <= 0']
        C += [GInput1 + ' - '+ Input2 + ' <= 0']
        C += [Input2+' + '+Doutput+' - '+ GInput1 + ' <= 1']
        C += [GInput2+' - '+Doutput+' <= 0']
        C += [GInput2 + ' - '+ Input1 + ' <= 0']
        C += [Input1+' + '+Doutput+' - '+ GInput2 + ' <= 1']
        return C

    def genConstraints_en_de_gue(self,r):
        C = []
        DGL = self.genVars_DGL(r)
        GIA1 = self.genVars_In1_AND_Guess(r)
        GIA2 = self.genVars_In2_AND_Guess(r)
        IA1 = self.genVars_In1_AND(r)
        IA2 = self.genVars_In2_AND(r)
        DOA=self.genVars_DOut_AND(r)

        for j in range(self.n):
            C += self.subfunc_AND(IA1[j],IA2[j],DOA[j],GIA1[j],GIA2[j])
        for j in range(self.n):
            C += self.genConstraints_AND_XOR([GIA1[(j-self.s1)%self.n],GIA2[(j-self.s2)%self.n]],DGL[j])
        return C

    def genConstraints_additional(self,Dis_Round,InputA,keysize):
        C=[]
        L0=self.genVars_L(0)
        R0=self.genVars_R(0)
        DL=self.genVars_DL(Dis_Round)
        DR=self.genVars_DR(Dis_Round)
        CL0=self.genVars_CL(0)
        DGL0=self.genVars_DGL(0)

        for j in range(self.n):
            C+=self.genConstraints_AND_XOR([L0[j],DGL0[j]],CL0[j])

        for j in range(self.n):
            C += [CL0[j]+' - '+L0[j]+' <= 0']
            C += [CL0[j] + ' - '+ DGL0[j] + ' <= 0']
            C += [DGL0[j]+' + '+L0[j]+' - '+ CL0[j] + ' <= 1']

        if InputA<=ceil(log(keysize,2)):
            C+=[' + '.join(L0)+' + '+' + '.join(R0)+' = '+str(InputA)]
            Constraint=''

            for i in range(self.n):
                Constraint+=str(int(pow(2,In)-1))+' '+str(DL[i])+' + '
                Constraint+=str(int(pow(2,In)-1))+' '+str(DR[i])+' + '
            Constraint += ' + '.join(CL0)
            Constraint+= ' - '+ self._genObjective_(Dis_Round)
            Constraint+=' >= 1'
            C+=[Constraint]
        else:
            C+=[' + '.join(L0)+' + '+' + '.join(R0)+' >= '+str(InputA)]
        #活跃输入位数不超过密钥位数，不少于1
        C+=[self.genObjective(Dis_Round)+' <= '+str(keysize-1)]
        C += [self.genObjective(Dis_Round) +' + ' + ' + '.join(L0)+ ' - '+' - '.join(CL0)+' <= '+str(keysize+2)]
        C+=[self.genObjective(Dis_Round)+' >= '+str(1)]

        return C

    #这两个目标函数只用于调用，真正的目标函数为后面的密钥恢复的目标函数
    def genObjective(self,Dis_Round):
        V=[]
        for i in range(Dis_Round):
            DGL=self.genVars_DGL(i)
            V+=DGL
        v=' + '.join(V)
        Objective=v
        return Objective

    def _genObjective_(self,Dis_Round):
        V=[]
        for i in range(Dis_Round):
            DGL=self.genVars_DGL(i)
            V+=DGL
        v=' - '.join(V)
        Objective=v
        return Objective

    #生成密钥恢复的目标函数
    def genObjective_Key(self,Dis_Round,En_Round,De_Round):
        GK=[]
        CK=[]
        '''for i in range(En_Round):
            CK+=self.genVars_cutting_guessed_subkey(i)
            GK+=self.genVars_Key_GK(i)
        for i in range(Dis_Round+En_Round,Dis_Round+En_Round+De_Round):
            CK+=self.genVars_cutting_guessed_subkey(i)
            GK+=self.genVars_Key_GK(i)
        Objective=' + '.join(GK)+' - '+' - '.join(CK)'''
        for i in range(En_Round):
            GK+=self.genVars_Key_GK(i)
        for i in range(Dis_Round+En_Round,Dis_Round+En_Round+De_Round):
            GK+=self.genVars_Key_GK(i)
        Objective=' + '.join(GK)

        return Objective

    #前r0轮：向前差分约束
    def genConstraints_Key_M(self,r):
        C=[]
        ML=self.genVars_Key_ML(r-1)
        MR=self.genVars_Key_MR(r-1)
        MLr=self.genVars_Key_ML(r)
        MRr=self.genVars_Key_MR(r)
        MS1=self.genVars_Key_MS1(r-1)
        MS2=self.genVars_Key_MS2(r-1)
        MS3=self.genVars_Key_MS3(r-1)
        MA=self.genVars_Key_MA(r-1)

        for j in range(self.n):
            C+=[MRr[j]+' - '+ML[j]+' = 0']
            C+=[MRr[(j+self.s1)%self.n]+' - '+MS1[j]+' = 0']
            C+=[MRr[(j+self.s2)%self.n]+' - '+MS2[j]+' = 0']
            C+=[MRr[(j+self.s3)%self.n]+' - '+MS3[j]+' = 0']

        for j in range(self.n):
            C+=self.genConstraints_AND_XOR([MS1[j],MS2[j]],MA[j])
            C+=self.genConstraints_AND_XOR([MS3[j],MA[j],MLr[j]],MR[j])
        return C

    #后r2轮：向下确定关系
    def genConstraints_Key_W(self,r):
        C=[]
        WL=self.genVars_Key_WL(r-1)
        WR=self.genVars_Key_WR(r-1)
        WLr=self.genVars_Key_WL(r)
        WRr=self.genVars_Key_WR(r)
        WS1=self.genVars_Key_WS1(r-1)
        WS2=self.genVars_Key_WS2(r-1)
        WS3=self.genVars_Key_WS3(r-1)
        WA=self.genVars_Key_WA(r-1)

        for j in range(self.n):
            C+=[WLr[j]+' - '+WR[j]+' = 0']
            C+=[WLr[j]+' - '+WA[j]+' = 0']
            C+=[WS1[j]+' - '+WA[j]+' = 0']
            C+=[WS2[j]+' - '+WA[j]+' = 0']
            C+=[WLr[j]+' - '+WS3[j]+' = 0']

        for j in range(self.n):
            C+=self.genConstraints_AND_XOR([WL[j],WS1[(j-self.s1)%self.n],WS2[(j-self.s2)%self.n],WS3[(j-self.s3)%self.n]],WRr[j])

        return C

    def genConstraints_Key_G1(self,r):
        C=[]
        GR=self.genVars_Key_GR(r-1)
        GL=self.genVars_Key_GL(r-1)
        GRr=self.genVars_Key_GR(r)
        GLr=self.genVars_Key_GL(r)
        GS1=self.genVars_Key_GS1(r-1)
        GS2=self.genVars_Key_GS2(r-1)
        GS3=self.genVars_Key_GS3(r-1)
        GA=self.genVars_Key_GA(r-1)
        MS1=self.genVars_Key_MS1(r-1)
        MS2=self.genVars_Key_MS2(r-1)
        GK=self.genVars_Key_GK(r-1)
        for j in range(self.n):
            C+=[GLr[j]+' - '+GR[j]+' = 0']
            C+=[GLr[j]+' - '+GA[j]+' = 0']
            C+=[GLr[j]+' - '+GK[j]+' = 0']
            C+=[GLr[j]+' - '+GS3[j]+' = 0']

        for j in range(self.n):
            C+=self.genConstraints_AND_XOR([GA[j],MS2[j]],GS1[j])
            C+=self.genConstraints_AND_XOR([GA[j],MS1[j]],GS2[j])

        for j in range(self.n):
            C+=self.genConstraints_AND_XOR([GRr[j],GS1[(j-self.s1)%self.n],GS2[(j-self.s2)%self.n],GS3[(j-self.s3)%self.n]],GL[j])

        return C

    def genConstraints_Key_G2(self,r):
        C=[]
        GR=self.genVars_Key_GR(r-1)
        GL=self.genVars_Key_GL(r-1)
        GRr=self.genVars_Key_GR(r)
        GLr=self.genVars_Key_GL(r)
        GS1=self.genVars_Key_GS1(r-1)
        GS2=self.genVars_Key_GS2(r-1)
        GS3=self.genVars_Key_GS3(r-1)
        GA=self.genVars_Key_GA(r-1)
        WA=self.genVars_Key_WA(r-1)
        GK = self.genVars_Key_GK(r-1)
        for j in range(self.n):
            C+=self.genConstraints_AND_XOR([GL[j],GS1[(j-self.s1)%self.n],GS2[(j-self.s2)%self.n],GS3[(j-self.s3)%self.n]],GRr[j])

        for j in range(self.n):
            C+=[GR[j]+' - '+ GA[j] + ' = 0']
            C+=[GR[j]+' - '+ GS3[j] + ' = 0']
            C+=[GR[j]+' - '+ GLr[j] + ' = 0']
            C+=[GR[j]+' - '+ GK[j] + ' = 0']

        for j in range(self.n):
            C+=[WA[j]+' - '+ GS1[j] + ' = 0']
            C+=[WA[j]+' - '+ GS2[j] + ' = 0']


        return C

    #key bridging technique
    def genVars_cutting_guessed_subkey(self, r):
        return ['CSK_'+ str(j) + '_r' + str(r) for j in range(self.n)]

    #sk = [k1,k2,k3,k4],ck, any three elements of sk can deduce the other one.
    #Thus if k1 = k2 = k3 = k4 = 1, we let ck = 1, reducing one guess.

    def genConstraints_cutting_guessed_subkey(self, Dis_Round,En_Round, De_Round):
        C=[]

        if keysize//self.n==2:
            for i in range(0,De_Round-1):
                CK = self.genVars_cutting_guessed_subkey(Dis_Round+En_Round+i)
                GK0=self.genVars_Key_GK(Dis_Round+En_Round+i)
                GK1=self.genVars_Key_GK(Dis_Round+En_Round+i+1)
                GK2=self.genVars_Key_GK(Dis_Round+En_Round+i+2)
                if i%3==0 and De_Round>=i+3:
                    for j in range(0,self.n):
                        C+=[GK0[j]+' + '+GK1[(j-3)%self.n]+' + '+GK1[(j-4)%self.n]+' + '+GK2[j]+' - 4 '+CK[j]+' >= 0']
                        C+=[GK0[j]+' + '+GK1[(j-3)%self.n]+' + '+GK1[(j-4)%self.n]+' + '+GK2[j]+' - '+CK[j]+' <= 3']
                else:
                    for j in range(0,self.n):
                        C +=[CK[j] + ' = 0']
            for i in range(De_Round-1,De_Round):
                CK = self.genVars_cutting_guessed_subkey(Dis_Round+En_Round+i)
                for j in range(0,self.n):
                    C +=[CK[j] + ' = 0']

            for i in range(0,En_Round-1):
                CK = self.genVars_cutting_guessed_subkey(i)
                GK0=self.genVars_Key_GK(i)
                GK1=self.genVars_Key_GK(i+1)
                GK2=self.genVars_Key_GK(i+2)
                if i%3==0 and En_Round>=i+3:
                    for j in range(0,self.n):
                        C+=[GK0[j]+' + '+GK1[(j-3)%self.n]+' + '+GK1[(j-4)%self.n]+' + '+GK2[j]+' - 4 '+CK[j]+' >= 0']
                        C+=[GK0[j]+' + '+GK1[(j-3)%self.n]+' + '+GK1[(j-4)%self.n]+' + '+GK2[j]+' - '+CK[j]+' <= 3']
                else:
                    for j in range(0,self.n):
                        C +=[CK[j] + ' = 0']
            for i in range(En_Round-1,En_Round):
                CK = self.genVars_cutting_guessed_subkey(i)
                for j in range(0,self.n):
                    C +=[CK[j] + ' = 0']

        elif keysize//self.n==3:
            for i in range(0,De_Round-2):
                CK = self.genVars_cutting_guessed_subkey(Dis_Round+En_Round+i)
                GK0=self.genVars_Key_GK(Dis_Round+En_Round+i)
                GK2=self.genVars_Key_GK(Dis_Round+En_Round+i+2)
                GK3=self.genVars_Key_GK(Dis_Round+En_Round+i+3)
                if i%4==2 and De_Round>=i+4:
                    for j in range(0,self.n):
                        C+=[GK0[j]+' + '+GK2[(j-3)%self.n]+' + '+GK2[(j-4)%self.n]+' + '+GK3[j]+' - 4 '+CK[j]+' >= 0']
                        C+=[GK0[j]+' + '+GK2[(j-3)%self.n]+' + '+GK2[(j-4)%self.n]+' + '+GK3[j]+' - '+CK[j]+' <= 3']
                else:
                    for j in range(0,self.n):
                        C +=[CK[j] + ' = 0']
            for i in range(max(0,De_Round-2),De_Round):
                CK = self.genVars_cutting_guessed_subkey(Dis_Round+En_Round+i)
                for j in range(0,self.n):
                    C +=[CK[j] + ' = 0']

            for i in range(0,En_Round-2):
                CK = self.genVars_cutting_guessed_subkey(i)
                GK0=self.genVars_Key_GK(i)
                GK2=self.genVars_Key_GK(i+2)
                GK3=self.genVars_Key_GK(i+3)
                if i%4==0 and En_Round>=i+4:
                    for j in range(0,self.n):
                        C+=[GK0[j]+' + '+GK2[(j-3)%self.n]+' + '+GK2[(j-4)%self.n]+' + '+GK3[j]+' - 4 '+CK[j]+' >= 0']
                        C+=[GK0[j]+' + '+GK2[(j-3)%self.n]+' + '+GK2[(j-4)%self.n]+' + '+GK3[j]+' - '+CK[j]+' <= 3']
                else:
                    for j in range(0,self.n):
                        C +=[CK[j] + ' = 0']
            for i in range(max(0,En_Round-2),En_Round):
                CK = self.genVars_cutting_guessed_subkey(i)
                for j in range(0,self.n):
                    C +=[CK[j] + ' = 0']

        else:
            for i in range(0,De_Round-3):
                CK =self.genVars_cutting_guessed_subkey(Dis_Round+En_Round+i)
                GK0=self.genVars_Key_GK(Dis_Round+En_Round+i)
                GK1=self.genVars_Key_GK(Dis_Round+En_Round+i+1)
                GK3=self.genVars_Key_GK(Dis_Round+En_Round+i+3)
                GK4=self.genVars_Key_GK(Dis_Round+En_Round+i+4)
                if i%5==1 and De_Round>=i+5:
                    for j in range(0,self.n):
                        C+=[GK0[j]+' + '+GK1[j]+' + '+GK1[(j-1)%self.n]+' + '+GK3[(j-3)%self.n]+' + '+GK3[(j-4)%self.n]+' + '+GK4[j]+' - 6 '+CK[j]+' >= 0']
                        C+=[GK0[j]+' + '+GK1[j]+' + '+GK1[(j-1)%self.n]+' + '+GK3[(j-3)%self.n]+' + '+GK3[(j-4)%self.n]+' + '+GK4[j]+' - '+CK[j]+' <= 5']
                else:
                    for j in range(0,self.n):
                        C +=[CK[j] + ' = 0']
            for i in range(max(0,De_Round-3),De_Round):
                CK = self.genVars_cutting_guessed_subkey(Dis_Round+En_Round+i)
                for j in range(0,self.n):
                    C +=[CK[j] + ' = 0']

            for i in range(0,En_Round-3):
                CK = self.genVars_cutting_guessed_subkey(i)
                GK0=self.genVars_Key_GK(i)
                GK1=self.genVars_Key_GK(i+1)
                GK3=self.genVars_Key_GK(i+3)
                GK4=self.genVars_Key_GK(i+4)
                if i%5==0 and En_Round>=i+5:
                    for j in range(0,self.n):
                        C+=[GK0[j]+' + '+GK1[j]+' + '+GK1[(j-1)%self.n]+' + '+GK3[(j-3)%self.n]+' + '+GK3[(j-4)%self.n]+' + '+GK4[j]+' - 6 '+CK[j]+' >= 0']
                        C+=[GK0[j]+' + '+GK1[j]+' + '+GK1[(j-1)%self.n]+' + '+GK3[(j-3)%self.n]+' + '+GK3[(j-4)%self.n]+' + '+GK4[j]+' - '+CK[j]+' <= 5']
                else:
                    for j in range(0,self.n):
                        C +=[CK[j] + ' = 0']
            for i in range(max(0,En_Round-3),En_Round):
                CK = self.genVars_cutting_guessed_subkey(i)
                for j in range(0,self.n):
                    C +=[CK[j] + ' = 0']
                    
        return C

    def genConstraints_Key_additional(self,Dis_Round,En_Round,De_Round):
        C=[]
        L0=self.genVars_L(0)
        R0=self.genVars_R(0)
        ML0=self.genVars_Key_ML(0)
        MR0=self.genVars_Key_MR(0)
        ML=self.genVars_Key_ML(En_Round)
        MR=self.genVars_Key_MR(En_Round)
        DL=self.genVars_DL(Dis_Round)
        DR=self.genVars_DR(Dis_Round)
        WL=self.genVars_Key_WL(Dis_Round+En_Round)
        WR=self.genVars_Key_WR(Dis_Round+En_Round)
        GL0 = self.genVars_Key_GL(En_Round)
        GR0 = self.genVars_Key_GR(En_Round)
        GL1 = self.genVars_Key_GL(Dis_Round+En_Round)
        GR1 = self.genVars_Key_GR(Dis_Round+En_Round)

        for j in range(self.n):
            C += [L0[j]+' - '+ ML[j] + ' = 0']
            C += [R0[j]+' - '+ MR[j] + ' = 0']

        for j in range(self.n):
            C += [DL[j]+' - '+ WL[j] + ' = 0']
            C += [DR[j]+' - '+ WR[j] + ' = 0']

        C += [' + '.join(ML0) +' + ' +' + '.join(MR0) + ' <= '+ str(blocksize-1)]
        #C += [self.genObjective_Key(Dis_Round, En_Round, De_Round) + ' <= '+ str(keysize-1)]

        for j in range(self.n):
            C += [GL0[j]+ ' = 0']
            C += [GR0[j]+ ' = 0']
            C += [GL1[j]+ ' = 0']
            C += [GR1[j]+ ' = 0']

        return C

    def genModel_keyrecovery(self,lpFile,InputA,Dis_Round,En_Round,De_Round):
        V=set([])
        C=list([])

        C+=self.genConstraints_cutting_guessed_subkey(Dis_Round,En_Round,De_Round)
        C+=self.genConstraints_Key_additional(Dis_Round,En_Round,De_Round)
        C+=self.genConstraints_additional(Dis_Round,InputA,keysize)

        for i in range(Dis_Round):
            C+=self.genConstraints_Encrypt(i)
            C+=self.genConstraints_Decrypt(i)
            C+=self.genConstraints_en_de_gue(i)

        for i in range(1,En_Round+1):
            C+=self.genConstraints_Key_M(i)

        for i in range(1,De_Round+1):
            C+=self.genConstraints_Key_W(Dis_Round+En_Round+i)

        for i in range(1,En_Round+1):
            C+=self.genConstraints_Key_G1(i)

        for i in range(1,De_Round+1):
            C+=self.genConstraints_Key_G2(Dis_Round+En_Round+i)


        V=self.getVariables_From_Constraints(C)

        fw=open(lpFile,'w')
        fw.write('Minimize'+'\n')
        fw.write(self.genObjective_Key(Dis_Round,En_Round,De_Round)+'\n')
        fw.write('\n')
        fw.write('Subject To'+'\n')

        for c in C:
            fw.write(c+'\n')

        fw.write('\n')
        fw.write('Binary'+'\n')
        for v in V:
            fw.write(v+'\n')
        fw.close()

if __name__ == '__main__':
    Dis_Round=11
    Addition_Round=10
    Num_ActiveInput=[8]
    blocksize=96
    keysize=144
    fw = open('D://SIMON_solution//SIMON'+str(blocksize)+'_'+str(keysize)+'//T'+str(Dis_Round)+'//A'+str(Addition_Round)+'//cmd.txt','w')
    m = DSMIMT_SIMON_Key(blocksize)
    for In in Num_ActiveInput:
        #fw.write('cd D:/gurobi/win64/bin/')
        #fw.write('\n')
        #fw.write('gurobi.bat')
        #fw.write('\n')
        for i in range(1, Addition_Round):
            m.genModel_keyrecovery('D://SIMON_solution//SIMON'+str(blocksize)+'_'+str(keysize)+'//T'+str(Dis_Round)+'//A'+str(Addition_Round)+'//T'+str(Dis_Round)+'_'+str(Addition_Round)+'_E'+str(i)+'_D'+str(Addition_Round-i)+'_In'+str(In)+'.lp', In, Dis_Round, i, Addition_Round-i)
            fw.write('r = read("D://SIMON_solution//SIMON'+str(blocksize)+'_'+str(keysize)+'//T'+str(Dis_Round)+'//A'+str(Addition_Round)+'//T'+str(Dis_Round)+'_'+str(Addition_Round)+'_E'+str(i)+'_D'+str(Addition_Round-i)+'_In'+str(In)+'.lp'+'")'+'\n')
            fw.write('r.optimize()'+'\n')
            fw.write('r.write("D://SIMON_solution//SIMON'+str(blocksize)+'_'+str(keysize)+'//T'+str(Dis_Round)+'//A'+str(Addition_Round)+'//T'+str(Dis_Round)+'_'+str(Addition_Round)+'_E'+str(i)+'_D'+str(Addition_Round-i)+'_In'+str(In)+'.sol'+'")'+'\n')
            fw.write('\n')
            fw.write('\n')
    fw.close()