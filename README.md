# social_segregation_France

Lil' Python program I've coded during a R&D internship used to analyse social segregation at multiple scales on a geodataframe. It agregate two populations distincly, here social housing and total housing, and we're looking at the social housing rate for every starting point and every agregation level. 

All data come from the 2013 national Census leaded by the INSEE. Avaible at https://www.insee.fr/fr/statistiques/2409491?sommaire=2409559.

Based on a method developped by Julien RANDON-FURLING and Madalina OLTEANU and Antoine LUCQUIAUD in "From urban segregation to spatial structure detection" published in Environment and Planning B: Urban Analytics and City Science in 2017. This model was generalized since, more details in "Segregation through the multiscalar lens" published in PNAS by Madalina OLTEANU, Julien RANDON-FURLING and William A. V. CLARK in 2019. 

!!!! NEED OPTIMIZATION AND ADAPTIBILITY !!!! 

## Required packages 
- Numpy 
- Pandas
- Matplotlib
- Geopandas 
- Scikit Learn

## How to use ? 

0) Download shapefile here : https://mega.nz/#F!nkJniKJR!vVM8WesHfdZ8CF7RiPw6EA 

1) Open Segregation_analysis.py 

2) Put your geodataframe in df. 

3) Choose two variables you want to consider in the dedicated statement. Take care : calculation will be logs/logt.

## Paris Example : 
 
This is the algorithme applied on the 10 most populated cities in france. On the first map, colors fit the ratio convergence speed and they fit starting social housing ratio in the second map. The first graph represent the trajectories for every starting point : a blue vertical bar mean a unit converges towards mean at this agregation level and horizontal bars reprensent boundaries.

You just have to run the script from terminal. In a compiler, you just have to put path of social_segregation_France file.

