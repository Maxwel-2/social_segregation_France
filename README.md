# social_segregation_France

Lil' Python program I've coded during a R&D internship used to analyse social segregation at multiple scales on a geodataframe. It agregate two populations distincly, here social housing and total housing, and we're looking at the social housing rate for every starting point and every agregation level. 

All data come from the 2013 national Census leaded by the INSEE. 

!!!! NEED OPTIMIZATION AND ADAPTIBILITY !!!! 

Based on a method developped by Julien RANDON-FURLING and Madalina OLTEANU and Antoine LUCQUIAUD in "From urban segregation to spatial structure detection" published in Environment and Planning B: Urban Analytics and City Science in 2017. This model was generalized since, more details in "Segregation through the multiscalar lens" published in PNAS by Julien RANDON-FURLING, Madalina OLTEANU and William A. V. CLARK in 2019. 

## How to use ? 

1) Open Segregation_analysis.py 

2) Put your geodataframe in df. 

3) Choose two variables you want to consider in the dedicated statement. Take care : calculation will be logs/logt.

## Paris Example : 
 
This is the algorithme applied on the 10 most populated cities in france. On the first map, colors fit the ratio convergence speed and they fit starting social housing ratio in the second map. The other graph represent the trajectories for every starting point : a blue vertical bar mean a unit converges towards at this agregation level and horizontal bars reprensent boundaries.

You just have to put the path of the file (social_segregation_france) in "PATH" at the begining of the file and run the script. 
