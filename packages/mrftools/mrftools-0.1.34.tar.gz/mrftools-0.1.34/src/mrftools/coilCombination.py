# Many Elements Adapted to PyTorch from: https://github.com/ismrmrd/ismrmrd-python-tools/blob/master/ismrmrdtools/coils.py
import numpy as np
from scipy import ndimage
import torch

# Calculates noise prewhitening matrix
# noise: Input noise data (array or matrix), [coil, nsamples]
# scale_factor: Applied on the noise covariance matrix. Used to adjust for effective 
# noise bandwith and difference in sampling rate between noise calibration and actual measurement:
# Should use: scale_factor = (T_acq_dwell/T_noise_dwell)*NoiseReceiverBandwidthRatio
# returns w: Prewhitening matrix, (w*data is prewhitened)
def calculateNoisePrewhitening(noise, scale_factor=1.0):
    noise_int = noise.reshape((noise.shape[0], noise.size//noise.shape[0]))
    M = float(noise_int.shape[1])
    dmtx = (1/(M-1))*np.asmatrix(noise_int)*np.asmatrix(noise_int).H
    dmtx = np.linalg.inv(np.linalg.cholesky(dmtx))
    dmtx = dmtx*np.sqrt(2)*np.sqrt(scale_factor)
    return dmtx

# Applies noise prewhitening matrix to dataset
## noise: Input noise data (array or matrix)`
## dmtx: Input noise prewhitening matrix
## returns w_data: Prewhitened data
def applyNoisePrewhitening(data,dmtx):
    s = data.shape
    w_data = np.asarray(np.asmatrix(dmtx)*np.asmatrix(data.reshape(data.shape[0],data.size//data.shape[0]))).reshape(s)
    return w_data

# Calculates the coilmaps for 2D data using an iterative version of the Walsh method
## img: Input images, ``[coil, y, x]``
## smoothing: Smoothing block size (default ``5``)
## niter: Number of iterations for the eigenvector power method (default ``3``)
## returns csm: Relative coil sensitivity maps, ``[coil, y, x]``
## returns rho: Total power in the estimated coils maps, ``[y, x]``
def calculateCoilmapsWalsh(input, smoothing=5, niter=3):
    ncoils = input.shape[0]
    nz = input.shape[1]
    nx = input.shape[2]
    ny = input.shape[3]

    rho = torch.zeros((nz, nx, ny))
    csm = torch.zeros((ncoils, nz, nx, ny),dtype=input.dtype)
    for z in range(nz):
        img = input[:,z,:,:]
        # Compute the sample covariance pointwise
        Rs = torch.zeros((ncoils,ncoils,nx,ny),dtype=img.dtype)
        for p in range(ncoils):
            for q in range(ncoils):
                Rs[p,q,:,:] = img[p,:,:] * torch.conj(img[q,:,:])

        # Smooth the covariance
        for p in range(ncoils):
            for q in range(ncoils):
                Rs[p,q] = smooth(Rs[p,q,:,:], smoothing)

        # At each point in the image, find the dominant eigenvector and corresponding eigenvalue
        # of the signal covariance matrix using the power method
        for x in range(nx):
            for y in range(ny):
                R = Rs[:,:,x,y].numpy()
                v = np.sum(R,axis=0)
                lam = np.linalg.norm(v)
                v = v/lam

                for iter in range(niter):
                    v = np.dot(R,v)
                    lam = np.linalg.norm(v)
                    v = v/lam

                rho[z, x, y] = torch.tensor(lam)
                csm[:,z, x, y] = torch.tensor(v)
    return (csm, rho)

# Fast, iterative coil map estimation for 2D or 3D acquisitions.
## im : Input images, [coil, y, x] or [coil, z, y, x].
## smoothing: Smoothing block size(s) for the spatial axes.
## niter: Maximal number of iterations to run.
## thresh: Threshold on the relative coil map change required for early termination of iterations.
## verbose: Print progress information at each iteration.
## device: The desired pytorch device to perform calculations on
## returns coil_map: Relative coil sensitivity maps, [coil, y, x] or [coil, z, y, x].
## returns coil_combined: The coil combined image volume, [y, x] or [z, y, x].
def calculateCoilmapsInati(im, smoothing=5, niter=5, thresh=1e-3,verbose=False, device=None):
    if(device==None):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    im = im.to(device)
    ncha = im.shape[0]
    D_sum = torch.sum(im, axis=(1, 2, 3))
    v = 1/torch.linalg.norm(D_sum)
    D_sum *= v
    R = 0
    for channel in np.arange(0, ncha):
        R += torch.conj(D_sum[channel]) * im[channel, ...]
    del D_sum, v     
    eps = torch.finfo(im.real.dtype).eps * torch.mean(torch.abs(im))
    print(np.shape(R))
    with torch.no_grad():
        for it in range(niter):
            if verbose:
                print("Coil map estimation: iteration %d of %d" % (it+1, niter))
            if thresh > 0:
                prevR = R.clone()
            R = R.conj()
            coil_map = im * R.unsqueeze(0)

            coil_map_smoothed = smooth_conv_3d(coil_map, kernelSize=smoothing)
            D = coil_map_smoothed * torch.conj(coil_map_smoothed)
            del coil_map

            R = torch.sum(D,axis=0)
            R = torch.sqrt(R) + eps
            R = 1/R
            coil_map = coil_map_smoothed * R.unsqueeze(0)
            del coil_map_smoothed

            D = im * torch.conj(coil_map)
            R = torch.sum(D, axis=0)
            D = coil_map * R.unsqueeze(0)
            D_sum = torch.sum(D, axis=(1, 2, 3))
            del D

            v = 1/torch.linalg.norm(D_sum)
            D_sum *= v
            del v

            imT = 0
            for cha in range(ncha):
                imT += torch.conj(D_sum[cha]) * coil_map[cha, ...]
            del D_sum

            magT = torch.abs(imT) + eps
            imT /= magT
            del magT

            R = R * imT
            imT = torch.conj(imT)
            coil_map = coil_map * imT.unsqueeze(0)
            del imT

            if thresh > 0:
                diffR = R - prevR
                vRatio = torch.linalg.norm(diffR) / torch.linalg.norm(R)
                del diffR
                if verbose:
                    print("vRatio = {}".format(vRatio))
                if vRatio < thresh:
                    del vRatio
                    break
    coil_combined = torch.sum((im * torch.conj(coil_map)), axis=0)
    del ncha, im, eps
    output = (coil_map, coil_combined)
    return output

# Smooths coil images
## img: Input complex images, ``[y, x] or [z, y, x]``
##  box: Smoothing block size (default ``5``)
## returns simg: Smoothed complex image ``[y,x] or [z,y,x]``
def smooth(img, box=5):
    t_real = torch.zeros(img.shape)
    t_imag = torch.zeros(img.shape)
    img = img.cpu()
    ndimage.uniform_filter(img.real,size=box,output=t_real)
    ndimage.uniform_filter(img.imag,size=box,output=t_imag)
    simg = t_real + 1j*t_imag
    return simg

def smooth_conv_3d(img, kernelSize, device=None):
    if(device==None):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    mean_conv = torch.nn.Conv3d(in_channels=1, out_channels=1, kernel_size=kernelSize, bias=False, padding='same')
    kernel_weights = (torch.ones((kernelSize, kernelSize, kernelSize), dtype=torch.complex64)/(kernelSize*kernelSize*kernelSize)).to(device)
    mean_conv.weight.data = kernel_weights.unsqueeze(0).unsqueeze(0)
    output = mean_conv(img.unsqueeze(1)).squeeze()
    del kernel_weights, mean_conv, img
    return output 