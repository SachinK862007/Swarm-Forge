import pyswarms as ps
import numpy as np

def optimize_params(attack_type):
    def cost(params):
        delay = params[:, 0]
        svc_ver = params[:, 1]
        cred = params[:, 2]
        return -(delay * 0.5 + svc_ver * 0.3 + cred * 0.2)

    bounds = ([0,0,0], [3,5,5])
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=3, options=options, bounds=bounds)
    best_cost, best_pos = optimizer.optimize(cost, iters=5)
    return {
        "delay_idx": int(best_pos[0]),
        "service_version": int(best_pos[1]),
        "credential_strength": int(best_pos[2])
    }