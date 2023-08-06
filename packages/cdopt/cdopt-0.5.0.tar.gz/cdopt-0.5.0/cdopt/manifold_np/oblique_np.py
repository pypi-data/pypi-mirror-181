import numpy as np


from .basic_manifold_np import basic_manifold_np

class oblique_np(basic_manifold_np):
    def __init__(self, var_shape) -> None:
        
        self.dim = var_shape[:-1]

        super().__init__('Oblique', var_shape, (*self.dim,1))

    


    def A(self, X):
        X_rvec = np.sum( X * X, -1, keepdims=True )
        return (2*X)/( 1 + X_rvec )


    def JA(self, X, G):
        XG = np.sum(X*G,-1, keepdims=True)
        X_rvec = np.sum( X * X, -1, keepdims= True ) +1
        return (2*G - (4*X *XG)/X_rvec )/X_rvec

    def JA_transpose(self, X, D):
        return self.JA(X,D) 


    def hessA(self, X, gradf, D):
        XG = np.sum(X*gradf,-1, keepdims=True)
        XD = np.sum(X * D, -1, keepdims=True)
        GD = np.sum(gradf * D, -1, keepdims=True)
        X_rvec = np.sum( X **2, -1, keepdims=True) +1
        return -(4/(X_rvec**2))*( gradf * XD + D * XG + X * GD ) + 16/( X_rvec**3 ) * (X * XG * XD)






    def JC(self, X, Lambda):
        return 2 * X * Lambda

    
    def C(self, X):
        return np.sum( X * X, -1, keepdims=True) - 1

    


    def C_quad_penalty(self, X):
        return np.sum( self.C(X) **2  )

    def Feas_eval(self, X):
        return np.sqrt(self.C_quad_penalty(X))


    def hess_feas(self, X, D):
        return 2 * D * self.C(X) + 4 * X * np.sum(X*D, -1, keepdims=True)



    def Init_point(self, Xinit = None):
        if Xinit is None:
            Xinit = np.random.randn(*self.var_shape)
        
        X_rvec = np.sqrt(np.sum( Xinit * Xinit, -1, keepdims=True ))
        Xinit = Xinit / X_rvec
        
        return Xinit

    def Post_process(self,X):
        X_rvec = np.sqrt(np.sum( X * X, -1, keepdims=True ))
        X = X / X_rvec
        return X
