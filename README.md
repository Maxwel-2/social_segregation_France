# social_segregation_France

Lil' Python program I've coded during an R&D internship used to analyse social segregation at multiple scales on a geodataframe. It agregate two populations distincly, here social housing and total housing, and we're looking at the social housing rate for every starting point and every agregation level. 

All data come from the 2013 national Census leaded by the INSEE. 

!!!! NEED OPTIMIZATION AND ADAPTIBILITY !!!! 

Based on a method developped by Julien RANDON-FURLING in "From urban segregation to spatial structure detection" published in 
Environment and Planning B: Urban Analytics and City Science in 2017. This model was generalized since, more details in "Segregation through the multiscalar lens" published in PNAS in 2019.

## How to use ? 

1) Open Segregation_analysis.py 

2) Put your geodataframe in df. 

3) Choose the name of the two variables you want to consider in the rename statement. Take care : calculation will be logs/logt.

## Paris Example : 

