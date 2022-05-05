__author__ = 'lv'

from math import *

class DSMIMT_SIMON_Dist():
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

    def genObjective(self,round):
        V=[]
        for i in range(round):
            DGL=self.genVars_DGL(i)
            V+=DGL
        v=' + '.join(V)
        Objective=v
        return Objective

    def genConstraints_additional(self,round,InputA,keysize):
        C=[]
        L0=self.genVars_L(0)
        R0=self.genVars_R(0)
        DL=self.genVars_DL(round)
        DR=self.genVars_DR(round)

        if InputA<=Num_ActiveInput:
            C+=[' + '.join(L0)+' + '+' + '.join(R0)+' = '+str(InputA)]
            Constraint=''
            Constraint+=self.genObjective(round)
            for i in range(self.n):
                Constraint+=' - '+str(int(pow(2,In)-1))+' '+str(DL[i])
                Constraint+=' - '+str(int(pow(2,In)-1))+' '+str(DR[i])
            Constraint+=' < 0'
            C+=[Constraint]
        else:
            C+=[' + '.join(L0)+' + '+' + '.join(R0)+' >= '+str(InputA)]
        #活跃输入位数不超过密钥位数，不少于1
        C+=[self.genObjective(round)+' <= '+str(keysize-1)]
        C+=[self.genObjective(round)+' >= '+str(1)]

        return C

    def genModel(self,lpFile,round,OutputA,keysize):
        r=round
        V=set([])
        C=list([])
        C+=self.genConstraints_additional(r,OutputA,keysize)

        for i in range(r):
            C+=self.genConstraints_Encrypt(i)
            C+=self.genConstraints_Decrypt(i)
            C+=self.genConstraints_en_de_gue(i)

        V=self.getVariables_From_Constraints(C)

        fw=open(lpFile,'w')
        fw.write('Minimize'+'\n')
        fw.write(self.genObjective(r)+'\n')
        fw.write('Subject To'+'\n')

        for c in C:
            fw.write(c+'\n')

        fw.write('\n'+'\n')
        fw.write('Binary'+'\n')
        for v in V:
            fw.write(v+'\n')
        fw.close()

if __name__ == '__main__':
    blocksize=128
    keysize=256
    round=15
    Num_ActiveInput=ceil(log(keysize,2))
    fw = open('D://SIMON_solution//SIMON'+str(blocksize)+'_'+str(keysize)+'//R'+str(round)+'//cmd.txt','a')
    a=DSMIMT_SIMON_Dist(blocksize)
    for In in range(1, Num_ActiveInput + 2):
        b= a.genModel('D://SIMON_solution//SIMON'+str(blocksize)+'_'+str(keysize)+'//R'+str(round)+'//Simon_R'+str(round)+'_In'+str(In)+'.lp',round, In, keysize)
        fw.write('r = read("D://SIMON_solution//SIMON'+str(blocksize)+'_'+str(keysize)+'//R'+str(round)+'//Simon_R'+str(round)+'_In'+str(In)+'.lp'+'")'+'\n')
        fw.write('r.optimize()'+'\n')
        fw.write('r.write("D://SIMON_solution//SIMON'+str(blocksize)+'_'+str(keysize)+'//R'+str(round)+'//Simon_R'+str(round)+'_In'+str(In)+'.sol'+'")'+'\n')

