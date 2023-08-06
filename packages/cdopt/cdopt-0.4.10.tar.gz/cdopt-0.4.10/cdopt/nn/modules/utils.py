import torch 
import torch.nn as nn
from collections import OrderedDict

def get_quad_penalty(local_module: torch.nn.Module):
    if hasattr(local_module, 'quad_penalty'):
        quad_all = local_module.penalty_param * local_module.quad_penalty()
        
    else:
        quad_all = 0

    for child in local_module.children():
        quad_all += get_quad_penalty(child)

    return quad_all


def get_constraint_violation_vector(local_module: torch.nn.Module):
    if hasattr(local_module, 'quad_penalty'):
        quad_all = [ local_module.quad_penalty(), ]
        
    else:
        quad_all = []

    for child in local_module.children():
        quad_all += get_constraint_violation_vector(child)

    return quad_all


def get_constraint_violation(local_module:torch.nn.Module, ord = None, **kwargs):
    con_vec = torch.tensor(get_constraint_violation_vector(local_module))
    return torch.linalg.norm(con_vec, ord = ord, **kwargs)


def single_module_get_params_manifold(module:nn.Module):
    if hasattr(module, 'manifold'):
        
        manifold = getattr(module, 'manifold')
    else:
        manifold = None
        
    members = module._parameters.items()
    tmp = OrderedDict()
    for k,v in members:
        # print(k)
        tmp[k] = (v, manifold)

    return tmp.items()


def _named_members(module, get_members_fn, prefix='', recurse=True):
    r"""Helper method for yielding various names + members of modules.""" 
    modules = module.named_modules(prefix=prefix) if recurse else [(prefix, module)]
    for module_prefix, module in modules:
        members = get_members_fn(module)
        for k, v in members:
            name = module_prefix + ('.' if module_prefix else '') + k
            yield name, v

def get_named_params_manifolds(module:nn.Module, prefix: str = '', recurse: bool = True):
    '''
    This function relies on the torch.nn.module._name_members. Therefore, the order of the outputed manifolds is exactly the same as the
    outputs of the torch.nn.module.parameters. 

    If the layer are set with no manifolds, the function will return a str; otherwise, the function
    will return the manifolds that corresponds to the weights.
    '''


    # gen = _named_members(module, single_module_get_manifold, prefix = prefix, recurse = recurse)
    gen = module._named_members(single_module_get_params_manifold, prefix = prefix, recurse = recurse)
    for name, params_manifold in gen:
        yield name, params_manifold

def get_params_manifolds(module, prefix: str = '', recurse: bool = True):
    gen = get_named_params_manifolds(module, prefix = prefix, recurse=recurse)
    for name, params_manifold in gen:
        yield  params_manifold



def set_attributes(local_module: torch.nn.Module, attr_name:str,  value):
    if hasattr(local_module, 'attr_name'):
        setattr(local_module, 'attr_name', value)

    for child in local_module.children():
        set_attributes(child, attr_name, value)

def set_forward_type(local_module: torch.nn.Module, forward_with_A: bool):
    set_attributes(local_module, 'forward_with_A', forward_with_A)


    



# def set_forward_type(local_module: torch.nn.Module, forward_with_A: bool):
#     if hasattr(local_module, 'forward_with_A'):
#         setattr(local_module, 'forward_with_A', forward_with_A)

#     for child in local_module.children():
#         set_forward_type(child, forward_with_A)



def wvt_flatten2d(tensor_shape):
    tensor_shape_ref = (tensor_shape[1], tensor_shape[0], *tensor_shape[2:]  )
    var_shape = (torch.prod(torch.tensor( tensor_shape_ref[1:] )), torch.tensor(tensor_shape_ref[0]))
    var_shape_ref = (var_shape[1], var_shape[0])
    
    # var_shape_transp = ( torch.tensor(tensor_shape[0]), torch.prod(torch.tensor(tensor_shape[1:])))
    weight_to_var = lambda X_tensor : torch.reshape(X_tensor.transpose(0,1), var_shape_ref).T
    var_to_weight = lambda X_var: torch.reshape(X_var.T, tensor_shape_ref).transpose(0,1)
    return weight_to_var, var_to_weight, var_shape


def wvt_flatten2d_transp(tensor_shape):
    var_shape = (torch.prod(torch.tensor( tensor_shape[1:] )), torch.tensor(tensor_shape[0]))
    var_shape_ref = (var_shape[1], var_shape[0])
    
    # var_shape_transp = ( torch.tensor(tensor_shape[0]), torch.prod(torch.tensor(tensor_shape[1:])))
    weight_to_var = lambda X_tensor : torch.reshape(X_tensor, var_shape_ref).T
    var_to_weight = lambda X_var: torch.reshape(X_var.T, tensor_shape)
    return weight_to_var, var_to_weight, var_shape


def wvt_identical(tensor_shape):
    var_shape = tensor_shape
    weight_to_var = lambda X_tensor : X_tensor
    var_to_weight = lambda X_var: X_var 
    return weight_to_var, var_to_weight, var_shape

def wvt_transp(tensor_shape):
    var_shape = (*tensor_shape[:-2], tensor_shape[-1], tensor_shape[-2])
    weight_to_var = lambda X_tensor : X_tensor.transpose(-2,-1) 
    var_to_weight = lambda X_var: X_var.transpose(-2,-1)  
    return weight_to_var, var_to_weight, var_shape