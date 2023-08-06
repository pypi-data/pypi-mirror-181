import numpy as np
import torch

# from numpy.linalg import svd, eig
from .basic_manifold_torch import basic_manifold_torch
from torch.nn.parameter import Parameter
from torch import Tensor, DeviceObjType
from typing import List, Tuple, Optional, Callable

class stiefel_range_constraint_torch(basic_manifold_torch):
    def __init__(self, var_shape, e_vec = None, tau = 1,   device = torch.device('cpu'), dtype = torch.float64) -> None:
        self._n = var_shape[-2]
        self._p = var_shape[-1]
        super().__init__('Stiefel with range constraints', var_shape, (self._n + self._p ** 2,), device= device ,dtype= dtype)
        # self._parameters['Ip'] = Parameter(torch.diag_embed(torch.ones((*self.dim, self._p), device=self.device, dtype=self.dtype)), False)

        
        self._parameters['I_p'] = Parameter(torch.eye(self._p, device=self.device, dtype=self.dtype))
        if e_vec == None:
            self._parameters['e_vec'] = Parameter( torch.ones((self._n,1), device=self.device, dtype=self.dtype))/np.sqrt(self._n)
        else:
            self._parameters['e_vec'] = Parameter(torch.tensor(e_vec, device=self.device, dtype=self.dtype))

        self.Ip = self._parameters['I_p']
        self.e_vec = self._parameters['e_vec']
        self.tau = tau

    def Phi(self, M: Tensor) -> Tensor:
        return (M + M.transpose(-2,-1) )/2

    def A(self, X:Tensor):
        XX = X.transpose(-2,-1) @ X 
        eX = (self.e_vec).transpose(-2,-1) @ X
        # return X@(1.5 * self.Ip - 0.5 * XX) +  X @(XX - self.Ip) @ (eX.transpose(-2,-1) @ eX) - (X@ eX.transpose(-2,-1) - self.e_vec) @ eX
        return X@(1.5 * self.Ip - 0.5 * XX +  (((XX - 2* self.Ip) @(eX).transpose(-2,-1))@ eX   )) + self.e_vec@ eX

    def C(self, X:Tensor):
        XX = X.transpose(-2,-1) @ X
        eX = (self.e_vec).transpose(-2,-1) @ X
        return torch.cat(((XX-self.Ip).flatten(), self.tau * (X @ eX.transpose(-2,-1) - self.e_vec).flatten() ),dim = 0)


    def JA(self, X:Tensor, D:Tensor) -> Tensor:
        XX = X.transpose(-2,-1) @ X
        eX = (self.e_vec).transpose(-2,-1) @ X
        DX = D.transpose(-2,-1) @ X 
        eD = (self.e_vec).transpose(-2,-1) @ D 

        D1 = D@(1.5 * self.Ip - 0.5 * XX +  ((eX).transpose(-2,-1)@ (eX  @(XX - 2* self.Ip)) ) ) +  self.e_vec@ eD  
        
        D2 = X @(  -self.Phi(DX) + 2 * self.Phi(( eX.transpose(-2,-1) @ (eX @DX)))    ) + 2 * self.e_vec @ (eX @ self.Phi( DX @ (XX - 2* self.Ip)))
        return D1 + D2 



    def JA_transpose(self, X:Tensor, D:Tensor):
        XX = X.transpose(-2,-1) @ X
        eX = (self.e_vec).transpose(-2,-1) @ X
        DX = D.transpose(-2,-1) @ X 
        eD = (self.e_vec).transpose(-2,-1) @ D 
        return D@(1.5 * self.Ip - 0.5 * XX +  (((XX - 2* self.Ip) @(eX).transpose(-2,-1))@ eX   )) +  self.e_vec@ eD + X @(  -self.Phi(DX) + 2 * (self.Phi(DX) @eX.transpose(-2,-1)) @ eX  + 2 * (XX - 2* self.Ip) @ self.Phi((eX.transpose(-2,-1) @ eD ))    )


    def JC(self, X, Lambda):
        T = torch.reshape(Lambda[:self._p **2], (self._p, self._p) )
        gamma = torch.reshape(Lambda[self._p **2:], (self._n, 1))
        return 2 * X@ T  + self.tau * self.e_vec @ (gamma.T @ X) + self.tau *gamma @ ((self.e_vec).transpose(-2,-1) @ X) 
        


    def Init_point(self, Xinit: Tensor = None):
        if Xinit is None:
            Xinit = torch.randn(*self.var_shape, device = self.device, dtype = self.dtype)
            Xinit[...,:,0] = torch.reshape(self.e_vec.clone().detach(), (self._n, ))
        else:
            Xinit = Xinit.detach()
        Xinit = Xinit.to(device = self.device, dtype = self.dtype)

        if self.Feas_eval(Xinit) > 1e-6:
            UX, SX, VX = torch.svd(Xinit)
            Xinit = torch.matmul(UX, VX.transpose(-2,-1))
        
        Xinit.requires_grad = True
        return Xinit