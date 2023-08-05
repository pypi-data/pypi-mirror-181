import h5py
from numba import njit, prange
import numpy as np
import shutil
from scipy.sparse import csr_matrix, csc_matrix


def cp(file1,file2 = None):
    if file2 is None:
        ## check if a single string was given in, separated by a space
        temp_f_list = file1.split(" ")
        if len(temp_f_list)==2:
            file1 = temp_f_list[0]
            file2 = temp_f_list[1]
        else:
            print("\n\nsomething wrong with the cp syntax!\n\n")
            print("don't know how to interpret:",file1)
            sys.exit()
    with open(file1, 'rb') as f_in:
        with open(file2, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return()


def get_bins(total_vars, bin_size=5000):
    bins = []
    cur_bin = 0
    while cur_bin<total_vars:
        bins.append(min(cur_bin, total_vars))
        cur_bin+=bin_size
    bins.append(total_vars)
    return(bins)



@njit
def re_collate_vect(in_vect, full_length):
    out_vect = np.zeros((full_length),dtype=np.int32)
    for i in prange(len(in_vect)):
        out_vect[int(in_vect[i])]=1.+out_vect[in_vect[i]]
    return(out_vect)



@njit
def get_full_vect(in_vect):
    out_vect = np.zeros((np.sum(in_vect)),dtype=np.int32)
    counter_start=0
    for i in range(len(in_vect)):
        counter_end=counter_start+in_vect[i]
        out_vect[counter_start:counter_end]=int(i)
        counter_start=counter_end
    return(out_vect)


@njit
def get_split_counts(in_vect, percent_1=0.5):
    temp_counts = get_full_vect(in_vect)
    np.random.shuffle(temp_counts)
    if len(temp_counts)%2==0:
        first_len = int(float(len(temp_counts))*percent_1)
    elif np.random.random()>0.5:
        first_len = int(float(len(temp_counts))*percent_1)+1
    else:
        first_len = int(float(len(temp_counts))*percent_1)
    first = re_collate_vect(temp_counts[:first_len], len(in_vect))
    second = re_collate_vect(temp_counts[first_len:], len(in_vect))
    return(first, second)


@njit
def split_mat_counts_jit(in_mat, percent_1=0.5):
    out_mat_1 = np.zeros(in_mat.shape,dtype=np.int64)
    out_mat_2 = np.zeros(in_mat.shape,dtype=np.int64)
    for i in prange(in_mat.shape[1]):
        temp_vect_1, temp_vect_2 = get_split_counts(in_mat[:,i], percent_1=percent_1)
        out_mat_1[:,i]=temp_vect_1
        out_mat_2[:,i]=temp_vect_2
    return(out_mat_1, out_mat_2)


def split_mat_counts(in_mat, percent_1=0.5, bin_size = 5000, return_sparse=False):
    if in_mat.dtype!=np.int64:
        print("coercing to int64: make sure this is safe to do")
        in_mat=in_mat.astype(np.int64)
    if not return_sparse:
        return(split_mat_counts_jit(in_mat, percent_1=percent_1))
    else:
        res1, res2 = split_mat_counts_jit(in_mat, percent_1=percent_1)
        return(csc_matrix(res1), csc_matrix(res2))


def split_mat_counts_h5(in_mat_file, out_mat_file_1, out_mat_file_2, percent_1=0.5, bin_size=5000, key="infile"):
    cp(in_mat_file,out_mat_file_1)
    cp(in_mat_file,out_mat_file_2)
    in_mf=h5py.File(in_mat_file,'r')
    out_mf1=h5py.File(out_mat_file_1,'r+')
    out_mf2=h5py.File(out_mat_file_2,'r+')
    in_mat = in_mf[key]
    out_1 = out_mf1[key]
    out_2 = out_mf2[key]
    print(in_mat.shape)
    bin_size = np.min([in_mat.shape[1],bin_size])
    print(bin_size)
    bins = get_bins(in_mat.shape[1],bin_size)
    for i in range(len(bins)-1):
        start = bins[i]
        end = bins[i+1]
        print("splitting cells",start, "to",end)
        temp_1, temp_2 = split_mat_counts(in_mat[:,start:end], percent_1=percent_1)
        out_1[:,start:end]=temp_1
        out_2[:,start:end]=temp_2
    print("\n\nFinished splitting!\n")
    in_mf.close()
    out_mf1.close()
    out_mf2.close()
    return



def split_sparse(in_mat, percent_1=0.5, bin_size=5000):
    out_1 = csc_matrix(in_mat.shape,dtype=np.float32)
    out_2 = csc_matrix(in_mat.shape,dtype=np.float32)
    bins = get_bins(in_mat.shape[1],bin_size)
    for i in range(len(bins)-1):
        start = bins[i]
        end = bins[i+1]
        print("splitting cells",start, "to",end)
        temp_1, temp_2 = split_mat_counts(in_mat[:,start:end].todense(), percent_1=percent_1, return_sparse = True)
        out_1[:,start:end]+=temp_1
        out_2[:,start:end]+=temp_2
    print("\n\nFinished splitting!\n")
    return out_1, out_2



def multi_split(in_mat, 
                percent_vect=[0.45,0.25,0.3],
                bin_size = 5000):
    percent_vect = np.array(percent_vect)
    percent_vect /= np.sum(percent_vect)
    is_sparse = "todense" in dir(in_mat)
    if is_sparse:
        split_func = split_sparse
    else:
        split_func = split_mat_counts
    out_vect = []
    temp_mat = in_mat
    for i in range(1,len(percent_vect)):
        temp_out, temp_mat = split_func(temp_mat, 
                                        percent_1 = percent_vect[i-1],
                                        bin_size = bin_size)
        out_vect.append(temp_out)
    out_vect.append(temp_mat)
    return(out_vect)


#split_mat_counts_h5('/media/scott/ssd_2tb/Lung9_Rep1-Flat_files_and_images/polarization_analysis/exprs/exprs.hdf5' , '/media/scott/ssd_2tb/Lung9_Rep1-Flat_files_and_images/polarization_analysis/exprs/exprs_clust_split.hdf5','/media/scott/ssd_2tb/Lung9_Rep1-Flat_files_and_images/polarization_analysis/exprs/exprs_deg_split.hdf5'  )



