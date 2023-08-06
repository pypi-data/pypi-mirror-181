import numpy as np
import jax 
import jax.numpy as jnp 
from cdopt.manifold import basic_manifold
from jax import random


from .basic_manifold_jax import basic_manifold_jax

class stiefel_range_constraints_jax(basic_manifold_jax):
    def __init__(self, var_shape, e_vec = None, tau = 1, train_mode = False, device = None) -> None:
        self._n = var_shape[-2]
        self._p = var_shape[-1]
        self.dim = var_shape[:-2]


        self.device = device
        if not train_mode:
            super().__init__('Stiefel with range constraints', var_shape, (self._n + self._p ** 2,), device= self.device)
        # self._parameters['Ip'] = Parameter(torch.diag_embed(torch.ones((*self.dim, self._p), device=self.device, dtype=self.dtype)), False)

        
        self.Ip = jax.device_put(np.eye(self._p), self.device)
        

        if e_vec is None:
            self.e_vec =jax.device_put( np.ones((self._n,1))/np.sqrt(self._n), self.device)
        else:
            self.e_vec = jax.device_put(e_vec, self.device)

        self.tau = tau



    def Phi(self, M: np.ndarray) -> np.ndarray:
        return (M + M.swapaxes(-2,-1) )/2

    def A(self, X:np.ndarray) -> np.ndarray:
        XX = X.swapaxes(-2,-1) @ X 
        eX = self.e_vec.swapaxes(-2,-1) @ X
        # return X@(1.5 * self.Ip - 0.5 * XX) +  X @(XX - self.Ip) @ (eX.transpose(-2,-1) @ eX) - (X@ eX.transpose(-2,-1) - self.e_vec) @ eX
        return X@(1.5 * self.Ip - 0.5 * XX +  (((XX - 2* self.Ip) @(eX).swapaxes(-2,-1))@ eX   )) + self.e_vec@ eX

    def C(self, X:np.ndarray):
        XX = X.swapaxes(-2,-1) @ X
        eX = (self.e_vec).swapaxes(-2,-1) @ X
        return jnp.concatenate(((XX-self.Ip).flatten(),  self.tau * (X @ eX.swapaxes(-2,-1) - self.e_vec).flatten() ),axis = 0)


    def JA(self, X:np.ndarray, D:np.ndarray) -> np.ndarray:
        XX = X.swapaxes(-2,-1) @ X
        eX = (self.e_vec).swapaxes(-2,-1) @ X
        DX = D.swapaxes(-2,-1) @ X 
        eD = (self.e_vec).swapaxes(-2,-1) @ D 

        D1 = D@(1.5 * self.Ip - 0.5 * XX +  ((eX).swapaxes(-2,-1)@ (eX  @(XX - 2* self.Ip)) ) ) +  self.e_vec@ eD  
        
        D2 = X @(  -self.Phi(DX) + 2 * self.Phi(( eX.swapaxes(-2,-1) @ (eX @DX)))    ) + 2 * self.e_vec @ (eX @ self.Phi( DX @ (XX - 2* self.Ip)))
        return D1 + D2 



    def JA_transpose(self, X:np.ndarray, D:np.ndarray):
        XX = X.swapaxes(-2,-1) @ X
        eX = (self.e_vec).swapaxes(-2,-1) @ X
        DX = D.swapaxes(-2,-1) @ X 
        eD = (self.e_vec).swapaxes(-2,-1) @ D 
        return D@(1.5 * self.Ip - 0.5 * XX +  (((XX - 2* self.Ip) @(eX).swapaxes(-2,-1))@ eX   )) +  self.e_vec@ eD + X @(  -self.Phi(DX) + 2 * (self.Phi(DX) @eX.swapaxes(-2,-1)) @ eX  + 2 * (XX - 2* self.Ip) @ self.Phi((eX.swapaxes(-2,-1) @ eD ))    )


    def JC(self, X, Lambda):
        T = jnp.reshape(Lambda[:self._p **2], (self._p, self._p) )
        gamma = jnp.reshape(Lambda[self._p **2:], (self._n, 1))
        return 2 * X@ T  + self.e_vec @ (gamma.T @ X) + self.tau * gamma @ ((self.e_vec).swapaxes(-2,-1) @ X) 
        


    def Init_point(self, Xinit: np.ndarray = None, seed = 0):
        if Xinit is None:
            key = random.PRNGKey(seed)
            Xinit = random.uniform(key, self.var_shape)


        UX, SX, VX = jnp.linalg.svd(Xinit, full_matrices= False)
        Xinit = jnp.matmul(UX, VX)
        Xinit = jax.device_put(Xinit, self.device)
        return Xinit