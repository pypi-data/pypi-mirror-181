Description: 

This is a mini version of super vrp version 3 that include three main modules: 

1. create base_data from input json 

2. create vrp_data from base_data

3. vrp_solution from vrp_data

How to use this package? 

installation: 

!pip install supervrpv3

import supervrpv3 as superv3

store file 'stm_input.json' in the same folder of the main code

1. create base_data 

    req_body = open('stm_input.json', encoding='utf-8-sig')

    client = 'test'

    base_data = superv3.get_base_data(req_body, client)

2. create vrp_data 

    service = superv3.VRPService(base_data, client)

    service.preprocessing() # run only one time for each input 
    
    vrp_data = service.create_vrp_data()

3. create vrp_solution

    vrp_params = service.param_preprocessor.vrp_params

    context = superv3.ContextManager.from_vrp_data(vrp_data, vrp_params)
    
    vrp_solution = superv3.VRPSolution.from_vrp_data(vrp_data)


4. initialize free_vehicle in vrp_solution
    
    vrp_solution = select_vehicle_strategy(context, vrp_solution)

