from sympy import symbols, Symbol, init_printing,latex
from sympy.parsing.sympy_parser import parse_expr
from functools import reduce
from operator import add
from IPython.display import Latex#
import numpy as np
#init_printing()
class reaction(object):
    def __init__(self, inexp, outexp, rate):
        self.lhs = parse_expr(str(inexp))
        self.rhs = parse_expr(str(outexp))
        self.rate= rate
    
    @property
    def terms(self): return set(list(self.lhs.free_symbols)+ list(self.rhs.free_symbols))     
    def _populate_(self, arr, keys):
        ld = self.lhs.as_coefficients_dict()
        rd = self.rhs.as_coefficients_dict()
        for k in keys.keys():
            if k in ld:arr[keys[k]][0] = ld[k]
            if k in rd:arr[keys[k]][1] = rd[k]
    
    @staticmethod   
    def reaction_system(reactions):
        all_terms = list(set(reduce(add, [list(r.terms) for r in reactions], [])))
        all_terms.sort(key=lambda x: str(x))
        keys = dict(zip(all_terms, range(len(all_terms))))
        arr =  np.zeros((len(reactions), len(all_terms),2),np.int)
        for i,r in enumerate(reactions):r._populate_(arr[i], keys)
        return arr,keys, np.array([r.rate for r in reactions])
    
    def __repr__(self):  return self._repr_latex_()
    def _repr_latex_(self):
        init_printing(use_latex='mathjax')
        return latex(str(self.lhs) +"\\to "+str(self.rhs),  mode='inline')