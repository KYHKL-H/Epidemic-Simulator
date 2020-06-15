import numpy as np
import json
import os
from step import node

if __name__=='__main__':
    #====================================settings and initialization======================================#
    os.makedirs('/temp')
    os.makedirs('/results')
    #---------------------------------loading popultaion mobility pattern---------------------------------#
    print('Loading popultaion mobility pattern...')
    with open('/od_prob.json','r') as f:
        od_prob=json.load(f)
        od_prob=np.array(od_prob)
    print('Down!')
    #-----------------------------------------------------------------------------------------------------#

    #----------------------------------------simulation settings------------------------------------------#
    LIST=[0]
    #LIST = [para1,para2,...] can be used to automatically simulate over a set of parameters
    times=1 #times of simulation
    N0=50 #number of cases at start
    LAST=100 #simulation lasting time(day)
    #-----------------------------------------------------------------------------------------------------#

    for I in LIST:
    #--------------------------------------dynamic mobility control---------------------------------------#
        clever_strategy=True
        control_threshold=2
        strategy_freq=48
    #-----------------------------------------------------------------------------------------------------#

    #----------------------------simple ratio mobility control between blocks-----------------------------#
        traffic_restrict=1 #restriction rate
        print('Setting traffic restriction...')
        od_prob1=od_prob*traffic_restrict
        print('Down!')
    #-----------------------------------------------------------------------------------------------------#

    #----------------------------------mobility control within blocks-------------------------------------#
        #reduction factor 𝛾0 needed to be applied to 'beta' in node.py
    #-----------------------------------------------------------------------------------------------------#

        for ti in range(times):
    #----------------------------------loading population distribution------------------------------------#
            print('Initializing population distribution...')
            with open('/pop_blocks.json','r') as f:
                pop_block=json.load(f)
            nodes=[]
            block_num=len(pop_block)
            pop_block=np.array(pop_block)
            pop_total=0
            for i in range(block_num):
                nodes.append(node(i))
                nodes[i].set_susceptible(pop_block[i])
                pop_total+=pop_block[i]
            del pop_block
            print('Down!')
    #-----------------------------------------------------------------------------------------------------#

    #----------------------------------------initial infection--------------------------------------------#
            print('Initializing infection...')
            I0=0 #ID of outbreak block
            nodes[I0].set_infected(N0)
            nodes[I0].set_susceptible(nodes[I0].susceptible-N0)
            print('Down!')
    #-----------------------------------------------------------------------------------------------------#

    #============================================simulation===============================================#

            print('Start simulation...')
            control_mark=np.zeros(block_num)
            control_influence=[]
            S_temp=np.zeros((block_num,block_num+1))
            L_temp=np.zeros((block_num,block_num+1))
            I_temp=np.zeros((block_num,block_num+1))
            Ia_temp=np.zeros((block_num,block_num+1))
            R_temp=np.zeros((block_num,block_num+1))
            for time in range(int(LAST*48)):
                print('time'+str(ti+1)+' step'+str(time+1))
                fl=time>960
    #---------------------------------------------step1---------------------------------------------------#
                for i in range(block_num):
                    nodes[i].step()
    #-----------------------------------------------------------------------------------------------------#

    #---------------------------------------------step2---------------------------------------------------#
                for k in range(block_num):
                    S_temp[k]=np.random.multinomial(nodes[k].susceptible,od_prob1[time%(7*48)][k])
                    L_temp[k]=np.random.multinomial(nodes[k].latent,od_prob1[time%(7*48)][k])
                    I_temp[k]=np.random.multinomial(nodes[k].infected,od_prob1[time%(7*48)][k])
                    Ia_temp[k]=np.random.multinomial(nodes[k].infected_asymptomatic,od_prob1[time%(7*48)][k])
                    R_temp[k]=np.random.multinomial(nodes[k].recovered,od_prob1[time%(7*48)][k])
                total=0
                if(clever_strategy and fl):
                    if(time%strategy_freq==0):
                        print('Adujsting strategy...')
                        for i in range(block_num):
                            if(nodes[i].infected>=control_threshold):
                                control_mark[i]=1
                            else:
                                control_mark[i]=0
                        print('Down!')
                    for k in range(block_num):
                        S_temp[k][k]=0
                        L_temp[k][k]=0
                        I_temp[k][k]=0
                        Ia_temp[k][k]=0
                        R_temp[k][k]=0
                    total+=np.sum(np.sum(S_temp,axis=0),axis=0)
                    total+=np.sum(np.sum(L_temp,axis=0),axis=0)
                    total+=np.sum(np.sum(I_temp,axis=0),axis=0)
                    total+=np.sum(np.sum(Ia_temp,axis=0),axis=0)
                    total+=np.sum(np.sum(R_temp,axis=0),axis=0)
                    for k in range(block_num):
                        if(control_mark[k]):
                            S_temp[k,:]=0
                            S_temp[:,k]=0
                            L_temp[k,:]=0
                            L_temp[:,k]=0
                            I_temp[k,:]=0
                            I_temp[:,k]=0
                            Ia_temp[k,:]=0
                            Ia_temp[:,k]=0
                            R_temp[k,:]=0
                            R_temp[:,k]=0
                S_temp_sum0=np.sum(S_temp,axis=0)
                L_temp_sum0=np.sum(L_temp,axis=0)
                I_temp_sum0=np.sum(I_temp,axis=0)
                Ia_temp_sum0=np.sum(Ia_temp,axis=0)
                R_temp_sum0=np.sum(R_temp,axis=0)
                S_temp_sum1=np.sum(S_temp,axis=1)
                L_temp_sum1=np.sum(L_temp,axis=1)
                I_temp_sum1=np.sum(I_temp,axis=1)
                Ia_temp_sum1=np.sum(Ia_temp,axis=1)
                R_temp_sum1=np.sum(R_temp,axis=1)
                if(clever_strategy and fl):
                    total1=0
                    total1+=np.sum(S_temp_sum0,axis=0)
                    total1+=np.sum(L_temp_sum0,axis=0)
                    total1+=np.sum(I_temp_sum0,axis=0)
                    total1+=np.sum(Ia_temp_sum0,axis=0)
                    total1+=np.sum(R_temp_sum0,axis=0)
                    control_influence.append((1-(total1/total))*traffic_restrict)
                else:
                    control_influence.append(1-traffic_restrict)
                for k in range(block_num):
                    nodes[k].set_susceptible(nodes[k].susceptible+S_temp_sum0[k]-S_temp_sum1[k]+S_temp[k][block_num])
                    nodes[k].set_latent(nodes[k].latent+L_temp_sum0[k]-L_temp_sum1[k]+L_temp[k][block_num])
                    nodes[k].set_infected(nodes[k].infected+I_temp_sum0[k]-I_temp_sum1[k]+I_temp[k][block_num])
                    nodes[k].set_infected_asymptomatic(nodes[k].infected_asymptomatic+Ia_temp_sum0[k]-Ia_temp_sum1[k]+Ia_temp[k][block_num])
                    nodes[k].set_recovered(nodes[k].recovered+R_temp_sum0[k]-R_temp_sum1[k]+R_temp[k][block_num])
    #-----------------------------------------------------------------------------------------------------#

    #---------------------------------save data in the current step---------------------------------------#
                save=[]
                for i in range(block_num):
                    temp1=[nodes[i].susceptible,nodes[i].latent,nodes[i].infected,nodes[i].infected_asymptomatic,nodes[i].recovered,nodes[i].death]
                    save.append(temp1)
                save=np.array(save)
                save=save.astype(np.float)
                with open('/temp/result_'+str(time)+'.json','w') as f:
                    json.dump(save.tolist(),f)
    #-----------------------------------------------------------------------------------------------------#

    #============================================data saving==============================================#

    #------------------------------save influence of mobility cointrol------------------------------------#
            with open('/results/control-influence_parameter{}_time{}.json'.format(I,ti+1),'w') as f:
                json.dump(control_influence,f)
    #-----------------------------------------------------------------------------------------------------#

    #------------------------------------merge data saved in each step------------------------------------#
            print('Merging data...')
            T=LAST*48
            result=[]
            for i in range(T):
                with open('/temp/result_'+str(i)+'.json','r') as f:
                    temp=json.load(f)
                result.append(temp)
                print('{}/{}'.format(i+1,T))
            print('saving...')
            with open('/results/result_parameter{}_time{}.json'.format(I,ti+1),'w') as f:
                json.dump(result,f)
            print('Down!')
    #-----------------------------------------------------------------------------------------------------#