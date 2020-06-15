#  Epidemic simulator for COVID-19

#### The following parameters are required to be set:

See step.py, the default value corresponds those in the paper

- t_eps——incubation period(day)
- t_I——lasting of I(day)
- t_Ia——lasting of Ia(day)
- d——death rate
- R_0——basic reproduction number
- Pa——proportion of Ia
- r_L
- r_a

####  The following data files are required:

- od_prob.json——array in size **[336]\[number of blocks]\[number of blocks]**, recording the probability for people in the i-th block to travel to the j-th during the t-th time step.
- pop_blocks.json——array in size **[number of blocks]**, recording the population size in each blocks.

#### The following results will be saved:

The results will be defaultly saved to path "c:\results"

- control-influence_parameter{θ}_time{t}.json——array in size **[lasting steps]**, recording the percentage of population mobility being influenced due to mobility control during each time steps, in the t-th simulation with parameter θ.
- result_parameter{θ}_time{t}.json——array in size **[lasting steps]\[number of blocks]\[6]**, recording the number of people in state S, L, I, Ia, R, D (by order) in each block at each time step, in the t-th simulation with parameter θ.
