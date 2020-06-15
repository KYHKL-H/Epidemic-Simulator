import numpy as np

'''
characters of COVID-19
'''
t_eps = 5.2 #incubation period(day)
t_I = 14 #lasting of I(day)
t_Ia = 14 #lasting of Ia(day)
d = 0.15 #death rate
R_0 = 2.68 #basic reproduction number
Pa = 0.018 #proportion of Ia
r_L = 1.0
r_a = 0.6

'''
get parameters and covert them to values measured under step(30min)
'''
#Lemma B.1
eps = (1 / t_eps) / 48
mu_a = (1 / t_Ia) / 48
#Lemma B.2
alpha = (d / t_I) / 48
mu = ((1 - d) / (t_I - d)) / 48
#beta
beta = R_0 / (r_L * t_eps + (Pa * r_a + (1- Pa)) * t_I)
beta = np.power(1 + beta , 1 / 48) - 1

'''
get state transition possibilities
'''
L_I = eps * (1 - Pa)
L_Ia = eps * Pa
I_D = alpha
I_R = mu
Ia_R = mu_a

'''
'''

class node :
    def __init__ (self,id ):
        self.id = id
        self.susceptible = 0
        self.latent = 0  
        self.infected = 0
        self.death = 0
        self.infected_asymptomatic = 0
        self.recovered = 0
    def set_susceptible(self,susceptible):
        self.susceptible = susceptible
    def set_latent(self,latent):
        self.latent = latent
    def set_infected(self,infected):
        self.infected = infected
    def set_infected_asymptomatic(self,infected_asymptomatic):
        self.infected_asymptomatic = infected_asymptomatic
    def set_death(self,death):
        self.death = death
    def set_recovered(self,recovered):
        self.recovered = recovered
    def step(self):
        if(self.susceptible+self.latent+self.infected+self.infected_asymptomatic+self.recovered>0):
            #S->L
            lambda_j = ((self.infected + self.infected_asymptomatic * r_a + self.latent * r_L) / (self.susceptible+self.latent+self.infected+self.infected_asymptomatic+self.recovered)) * beta
            susceptible_to_latent,__ = np.random.multinomial(self.susceptible,[lambda_j, 1])
            self.susceptible -= susceptible_to_latent
            self.latent += susceptible_to_latent
            #L->I,L->Ia
            latent_to_infected,latent_to_Ia,__ = np.random.multinomial(self.latent,[L_I, L_Ia, 1]) 
            self.infected += latent_to_infected
            self.infected_asymptomatic += latent_to_Ia
            self.latent -= (latent_to_Ia + latent_to_infected)
            #I->D,I->R
            infected_to_death,infected_to_recovered,__ = np.random.multinomial(self.infected,[I_D,I_R,1])
            self.death += infected_to_death
            self.recovered += infected_to_recovered
            self.infected -= (infected_to_death + infected_to_recovered)
            #Ia->R
            Ia_to_recovered , __ = np.random.multinomial(self.infected_asymptomatic,[Ia_R,1])
            self.recovered += Ia_to_recovered
            self.infected_asymptomatic -= Ia_to_recovered