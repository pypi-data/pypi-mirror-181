from pyFAI import azimuthalIntegrator
from PyHyperScattering.PFGeneralIntegrator import PFGeneralIntegrator
import h5py
import warnings
import xarray as xr
import numpy as np
import pandas as pd
import math
from tqdm.auto import tqdm
#tqdm.pandas()

# the following block monkey-patches xarray to add tqdm support.  This will not be needed once tqdm v5 releases.
from xarray.core.groupby import DataArrayGroupBy,DatasetGroupBy

def inner_generator(df_function='apply'):
    def inner(df,func,*args,**kwargs):
        t = tqdm(total=len(df))
        def wrapper(*args,**kwargs):
            t.update( n=1 if not t.total or t.n < t.total else 0)
            return func(*args,**kwargs)
        result = getattr(df,df_function)(wrapper, **kwargs)
    
        t.close()
        return result
    return inner

DataArrayGroupBy.progress_apply = inner_generator()
DatasetGroupBy.progress_apply = inner_generator()

DataArrayGroupBy.progress_apply_ufunc = inner_generator(df_function='apply_ufunc')
DatasetGroupBy.progress_apply_ufunc = inner_generator(df_function='apply_ufunc')

#end monkey patch

class PFEnergySeriesIntegrator(PFGeneralIntegrator):

    def integrateSingleImage(self,img):
        # for each image: 
        #    get the energy and locate the matching integrator
        #    use that integrator to reduce
        #    return single reduced frame
        if type(img.energy) != float:
            en = img.energy.values[0]
        else:
            en = img.energy
        try:
            self.integrator = self.integrator_stack[en]
        except KeyError:
            self.integrator = self.createIntegrator(en)
        res = super().integrateSingleImage(img)
        try:
            if len(self.dest_q)>0:
                return res.interp(q=self.dest_q)
            else:
                return res
        except TypeError:
            return res
    def integrateImageStack(self,img_stack):
        
       
        # get just the energies of the image stack
        #energies = img_stack.energy.to_dataframe()
        
        #energies = energies['energy'].drop_duplicates()
        energies = np.unique(img_stack.energy.data)
        #create an integrator for each energy
        for en in energies:
            self.createIntegrator(en)
        self.createIntegrator(np.median(energies))
        # find the output q for the midpoint and set the final q binning
        try:
            self.dest_q = self.integrator_stack[np.median(energies)].integrate2d(np.zeros_like(self.mask).astype(int), self.npts, 
                                               unit='arcsinh(q.µm)' if self.use_log_ish_binning else 'q_A^-1',
                                               method=self.integration_method).radial
        except TypeError as e:
            if 'diffSolidAngle() missing 2 required positional arguments: ' in str(e):
                raise TypeError('Geometry is incorrect, cannot integrate.\n \n - Do your mask dimensions match your image dimensions? \n - Do you have pixel sizes set that are not zero?\n - Is SDD, beamcenter/poni, and tilt set correctly?') from e
            else:
                raise e
        if self.use_log_ish_binning:
            self.dest_q = np.sinh(self.dest_q)/10000
        # single image reduce each entry in the stack
        # + 
        # restack the reduced data
        data = img_stack
        indexes = list(data.indexes.keys())
        indexes.remove('pix_x')
        indexes.remove('pix_y')
        real_indexes = indexes
        for idx in indexes:
            if type(data.indexes[idx]) == pd.core.indexes.multi.MultiIndex:
                for level in data.indexes[idx].names:
                    try:
                        real_indexes.remove(level)
                    except ValueError:
                        pass
        indexes = real_indexes
        if len(indexes) == 1:
            if img_stack.__getattr__(indexes[0]).to_pandas().drop_duplicates().shape[0] != img_stack.__getattr__(indexes[0]).shape[0]:
                warnings.warn(f'Axis {indexes[0]} contains duplicate conditions.  This is not supported and may not work.  Try adding additional coords to separate image conditions',stacklevel=2)
            data_int = data.groupby(indexes[0],squeeze=False).progress_apply(self.integrateSingleImage)
        else:
            #some kinda logic to check for existing multiindexes and stack into them appropriately maybe
            data = data.stack({'pyhyper_internal_multiindex':indexes})
            if img_stack.pyhyper_internal_multiindex.to_pandas().drop_duplicates().shape[0] != img_stack.pyhyper_internal_multiindex.shape[0]:
                warnings.warn('Your index set contains duplicate conditions.  This is not supported and may not work.  Try adding additional coords to separate image conditions',stacklevel=2)
        
            data_int = data.groupby('pyhyper_internal_multiindex',squeeze=False).progress_apply(self.integrateSingleImage).unstack('pyhyper_internal_multiindex')
        return data_int
        #return img_stack.groupby('system',squeeze=False).progress_apply(self.integrateSingleImage)
    


    def createIntegrator(self,en):
        self.integrator_stack[en] = azimuthalIntegrator.AzimuthalIntegrator(
            self.dist, self.poni1, self.poni2, self.rot1, self.rot2, self.rot3 ,pixel1=self.pixel1,pixel2=self.pixel2, wavelength = 1.239842e-6/en)
        return self.integrator_stack[en]
    def __init__(self,**kwargs):
        self.integrator_stack = {}
        
        super().__init__(**kwargs)
    def recreateIntegrator(self):
        pass
    
    def __str__(self):
        return f"PyFAI energy-series integrator  SDD = {self.dist} m, poni1 = {self.poni1} m, poni2 = {self.poni2} m, rot1 = {self.rot1} rad, rot2 = {self.rot2} rad"