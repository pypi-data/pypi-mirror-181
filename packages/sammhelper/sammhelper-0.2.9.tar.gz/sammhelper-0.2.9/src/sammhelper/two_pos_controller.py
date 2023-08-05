import numpy as np
import tqdm as tq

from .sol_ode import sol_ode
from .delay import delay
from .two_position import two_position

def two_pos_controller(model, var0, t, param, Tt, xlimit, ylimit, x_index = -1, y_index = -1, n = 1, n_meas = 0):
    
    """
    Create a two position controller to adjust the parameter of the input ode function,
    calculate the controlled variable x with the adjusted parameter.

    Args:
        model (callable(y,t,...)): The function computes the derivative of y at t.
        time (array): A sequence of time points for which to solve for y . The initial
                      value point should be the first element of this sequence.
        xlimit (list): Setpoints for controlled variable x.
        ylimit (list): Setpoints for control member y (actuator).
        Tt (float): Specified dead time.
        
        x_index (int, optional): Index of the controlled element x in var0. Default is -1.
        y_index (int, optional): Index of control member y in param. Default is -1.
        
        n (int, optional): For a cascade of CSTRS, Number of total CSTRs n. Default is 1.
        n_meas (int,optional): In which reactor does is the controlled variable x measured. Default is the last reactor.
    
    Returns:
        results: The solved differential equation using the controller.
        y_final: The log of the adjusted control member y.
    """
    
    # create the y value list with initial value.
    y = ylimit[0]
    y_final = np.zeros(len(t))
    x = np.zeros(len(t))

    # empty dataframe for saving results
    results = list(range(len(t)))

    #  store the value calculated from last time.
    for i in tq.tqdm(range(len(t)-1),position=0,leave=True):
        
        y_final[i] = y
        param[y_index] = y

        #   get the solved results and get the new kla
        df = sol_ode(model, var0, t[i:i+2], param)

        # save the solved results, drop the duplicated value with the same time index,
        # only keeping the last one.
        
        if n == 1:
            results[i] = np.transpose(df)[-1]
            var0 = np.transpose(df)[-1]
            x[i] = df[x_index][-1]
        else:
            results[i] =np.array(df)[:,-1]
            var0 = np.array(df)[:,-1]
            x[i] = df[x_index][-1,n_meas-1]
        
        if Tt != 0:
            x_delay = delay(t, x, Tt, value = 0)

        else:
            x_delay = x

        # control the y value by two position controller.
        y = two_position(x_delay[i], y, xlimit, ylimit)
    
    y_final[len(t)-1] = y_final[len(t)-2]
    results[len(t)-1] = results[len(t)-2]
    
    if n != 1: 
        r = np.array(results)
        results = r.transpose(1,0,2)
    else: results = np.transpose(results)
    
    return results, y_final