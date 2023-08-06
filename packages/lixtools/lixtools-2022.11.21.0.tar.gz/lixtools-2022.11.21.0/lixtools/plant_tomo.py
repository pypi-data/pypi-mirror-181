"""
This file provide functions specific to tomography measurements on plants
Assume that the growth direction is roughly aligned with the rotation axis
"""
import numpy as np
import pylab as plt
from py4xs.hdf import h5xs,h5exp,lsh5
from lixtools.hdf import h5xs_an,h5xs_scan
from lixtools.hdf.scan import gen_scan_report
from py4xs.utils import get_grid_from_bin_ranges
import os

from sklearn.utils.extmath import randomized_svd 
from sklearn.decomposition import NMF
from scipy.signal import butter,filtfilt
from scipy.ndimage import gaussian_filter

q_bin_ranges = [[[0.0045, 0.0995], 95], [[0.0975, 0.6025], 101], [[0.605, 2.905], 230]]
qgrid0 = get_grid_from_bin_ranges(q_bin_ranges)

def BW_lowpass_filter(data, cutoff, order=4):
    b, a = butter(order, cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def remove_zingers(data, filt=[2, 1.5], thresh=4):
    mmd = gaussian_filter(data, filt)
    idx = ((data-mmd)>mmd/thresh)
    mmd2 = np.copy(data)
    mmd2[idx] = np.nan
    
    return mmd2

def scf(q, q0=0.08, ex=2):
    sc = 1./(np.power(q, -ex)+1./q0)
    return sc

def get_q_data(dt, q0=0.08, ex=2, q_range=[0.01, 2.5], skip=237):
    """ 
    """
    plt.figure()
    ax = plt.gca()
    mm = []
    for sn in dt.samples:
        for i in range(len(dt.proc_data[sn]['qphi']['merged'])):
            dm = dt.proc_data[sn]['qphi']['merged'][i].apply_symmetry()
            dm.d = dm.d*scf(dm.xc, q0=q0, ex=ex)
            dm.d = remove_zingers(dm.d)
            q,dd,ee = dm.line_profile(direction="x", xrange=q_range)
            mm.append(dd)
            if i%skip==0:  
                ax.plot(q, dd)
    ax.set_xscale("log")
    ax.set_yscale("log")

    return q,np.array(mm)
    
def sub_bkg(data, xcor, bkg_x_range=[0.03, 0.08], bkg_thresh=0.6e-2, skip=237):
    plt.figure()
    ax = plt.gca()
    xidx = ((xcor>bkg_x_range[0]) & (xcor<bkg_x_range[1]))
    mmb = []
    mm = []
    for i in range(data.shape[0]):
        dd = data[i][:]
        if np.average(dd[xidx])<bkg_thresh:
            mmb.append(dd)
        else:
            mm.append(dd)
        if i%skip==0:  
            ax.plot(xcor, dd)
    ax.set_xscale("log")
    ax.set_yscale("log")
    
    if len(mmb)>1:
        ax.plot(xcor, np.average(mmb, axis=0), "b", linewidth=3)
    else:
        raise Exception("did not find valid bkg ...")
        
    plt.show()
    return np.array(mm)-np.average(mmb, axis=0)
        
def get_phi_data(dt, q_range=[0.01, 2.5], bkg_thresh=0.6e-2):
    """ 
    """
    plt.figure()
    ax = plt.gca()
    mm = []
    mmb = []
    for sn in dt.samples:
        for i in range(len(dt.proc_data[sn]['qphi']['merged'])):
            dm = dt.proc_data[sn]['qphi']['merged'][i].apply_symmetry()
            dm.d = remove_zingers(dm.d)
            phi,dd,ee = dm.line_profile(direction="y", xrange=q_range)
            mm.append(dd)
            if np.max(dd)<bkg_thresh:
                mmb.append(dd)
            if i%237==0:  
                ax.plot(phi, dd)

    if len(mmb)>1:
        ax.plot(phi, np.average(mmb, axis=0), "b", linewidth=3)
        plt.show()
    
    return phi,np.array(mm),np.array(mmb)
        
def make_ev_maps(dt, x, mm, name="q", method="svd", N=5, max_iter=5000, offset=0.1):
    if method=="nmf":
        model = NMF(n_components=N, max_iter=max_iter)
        W = model.fit_transform(mm.T)
        eig_vectors = W
        coefs = model.components_
        N = model.n_components_
        print(f"NMF stopped after {model.n_iter_} iterations, err = {model.reconstruction_err_}")

        plt.figure(figsize=(6,5))
        for i in range(eig_vectors.shape[1]):
            plt.plot(x, eig_vectors[:,i]-i*offset)    
    elif method=="svd":
        V,S,U = randomized_svd(mm.T, N)
        print("SVD diagonal elements: ", S)
        eig_vectors = V*S
        coefs = U

        fig, axs = plt.subplots(1,2,figsize=(9,5), gridspec_kw={'width_ratios': [2, 1]})
        for i in range(eig_vectors.shape[1]):
            axs[0].plot(x, eig_vectors[:,i]-i*offset)
        axs[1].semilogy(S, "ko")
    else:
        raise Exception(f"unkown method: {method}")
        
    sl = 0
    for sn in dt.samples:
        ll = len(dt.proc_data[sn]['attrs']['transmission'])
        for j in range(N):
            dt.proc_data[sn]['attrs'][f'ev{j}_{name}_{method}'] = coefs[j,sl:sl+ll]
        sl += ll

    dt.make_map_from_attr(attr_names=[f'ev{i}_{name}_{method}' for i in range(N)])
    
    if not 'attrs' in dt.proc_data['overall'].keys():
        dt.proc_data['overall']['attrs'] = {}
    dt.proc_data['overall']['attrs'][f'evs_{name}_{method}'] = eig_vectors
    dt.proc_data['overall']['attrs'][f'ev_{name}'] = x

def recombine(coef, method="nmf"):
    """ coef should have the same dimension as dt.proc_data['overall']['attrs'][f'evs_{method}'].shape[1]
    """
    N = dt.proc_data['overall']['attrs'][f'evs_{method}'].shape[1]
    if len(coef)!=N:
        raise Exception(f"shape mismatch: {len(coef)} != {N}")
        
    return np.sum(coef*dt.proc_data['overall']['attrs'][f'evs_{method}'], axis=1)


def get_roi(d, qphirange):
    return np.nanmean(d.apply_symmetry().roi(*qphirange).d)

def create_maps():
    pass

def performNMF():
    pass

def proc_maps(sample_name, qgrid=qgrid0, detectors=None, Nphi=61, 
              attr_list = {"int_cellulose": [1.05, 1.15, -180, 180],
                           "int_amorphous": [1.25, 1.35, -180, 180],
                           "int_saxs":      [0.05, 0.2,  -180, 180]}, 
              datakey="qphi", subkey="merged", 
              reprocess=False):
    """ 
        assume that the first pass of data processing is already done: qphi maps already exists
    """
    data_file = f"{sample_name}_an2.h5"
    if os.path.exists(data_file):
        dt = h5xs_scan(data_file, load_raw_data=True)
        dt.load_data()
    else:
        if detectors is None:
            raise Exception("analysis file does not existing yet, must specify detectors ...")
        raw_data_files = sorted(glob.glob(f"{sample_name}-??.h5"))
        if len(raw_data_files)==0:
            raise Exception("must specify a list of raw data files ...")
        dt = h5xs_scan(data_file, [detectors, qgrid], Nphi=Nphi, pre_proc="2D")
        dt.import_raw_data(raw_data_files, force_uniform_steps=True, prec=0.001, debug=True)
        
        t0 = time.time()
        dt.process(N=8, debug=True)
        print(f"time elapsed: {time.time()-t0:.1f} sec")

    # build attribute maps
    if (not "overall" in dt.proc_data.keys()) or reprocess:
        if len(attr_list)==0:
            raise Exception("attribute list is empty ...")
            
        fast_axis = dt.attrs[dt.samples[-1]]['scan']['fast_axis']['motor']
        exp = dt.attrs[dt.samples[-1]]['header']['pilatus']['exposure_time']
        for sn,dh5 in dt.h5xs.items():
            dt.get_mon(sn=sn, trigger=fast_axis, exp=exp, force_synch="auto")
            for attr in attr_list.keys():
                dt.extract_attr(sn, attr, get_roi, "qphi", "merged", qphirange=attr_list[attr])
        
        maps_list = ["absorption"]+attr_list.keys()
        dt.make_map_from_attr(attr_names=maps_list)
        dt.save_data(save_data_keys="attrs")
        dt.calc_tomo_from_map(attr_names=maps_list, algorithm="pml_hybrid", num_iter=100)
        dt.save_data()


def 
    if Nc==0: 
        print("Nc not specified, test using SVD ...")
        
        