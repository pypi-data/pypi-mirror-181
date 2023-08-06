
import numpy as np
import random
import matplotlib.pyplot as plt
import Levenshtein
import math
import pandas as pd

from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform, pdist, cdist
from sklearn.feature_extraction.text import TfidfVectorizer as TFIDF
from sklearn import preprocessing
from collections import Counter

from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import sparse_dot_topn.sparse_dot_topn as ct




"""
   -----------------------------------------------------------------------------
   --------------------------- CLONES IDENTIFICATION ---------------------------
   -----------------------------------------------------------------------------
   
   Implementation of clone identification methods and sequences metrics

"""




def identify_clonal_group(seq_df_: pd.DataFrame, method = 'junction', embeddings = None, metric = None, clone_threshold = None, verbose = False):
    
    seq_df_.index = np.arange(len(seq_df_))
    
    '''
    Return clone clusters of the BCR sequences
    
    seq_df:
        Panda dataframe containing (optional depending on the method used):
            junctionH: Junction sequence of the BCR receptor heavy chain
            embeding:
            VgeneH:
            JgeneH:
            VgeneL:
            HgeneL:
                  
    method:
        junction, VDJunction, VDJunctionHL, alignfree
              

        
    metric:
        Levenshtein, Hamming, Cosine, Euclidean
        
    clone_threshold: 
        cuttof distance value used by the Hierarchical clustering
        required for all methods except for 'junction'
        
    If method == junction, VDJunction:
        seq_df should contain [junctionH:]
        
    If method == VDJunction:
        seq_df should contain [junctionH,VgeneH,JgeneH]
        - metric should be Levenshtein or Hamming
        
    If method == VDJunctionHL:
        seq_df should contain [junctionH,VgeneH,JgeneH,VgeneL,JgeneL]
        - metric should be Levenshtein or Hamming
        
    If method == alignfree:
        embeding: vectorised representation of the sequence
        - metric should be Cosine or Euclidean
    '''
    
    if method.lower() not in ['junction','alignfree','vdjunction', 'vdjunctionhl','af','baseline','vjj','vdj']:
        print('ERROR: Method %s is not implemented. currently supported methods are')
        print('  junction, VDJunction, VDJunctionHL, alignfree')
    
    if method.lower() not in ['junction','baseline'] and clone_threshold is None:
        print('ERROR: Method %s requires the definition of a cuttof threshold for clonal identification' % method)
        print('You can obtain it with the distance to nearest distribution to the negation sequence')
        return None
    
    # |--------------------------------------------------------------------------|
    # |--------------------------------------------------------------------------|    
    junction_groups = group_seq_cluster(seq_df_, keys=['junctionH'])  
    if method.lower() in ['junction','baseline']:
        final_clusters = junction_groups 
        
    # |--------------------------------------------------------------------------|
    # |--------------------------------------------------------------------------|          
        
    elif method.lower() in ['alignfree','af']:
        
        junctions = seq_df_.loc[:,'junctionH'].values
        seq_df = seq_df_.drop_duplicates(subset='junctionH')
        unique_junctions = list(seq_df.loc[:,'junctionH'].values)
        representor = [unique_junctions.index(x) for x in junctions]
        
        if embeddings is None:
            vector_array = get_kmer_representation(seq_df['VDJ_sequence'].to_numpy())
        else:
            vector_array = embeddings[seq_df.index]
        
        seq_df.index = np.arange(len(seq_df))
                
        if metric is None:
            metric = 'cosine'
            
        if metric.lower() not in ['cosine', 'euclidean']:
            print('ERROR: The supported metrics for method alignfree are ')
            print('Cosine and Euclidean, but you chosed %s' % metric)
            return None
            
        if len(seq_df) > 10000 and metric.lower() != 'cosine':
            print('  Computing distance matrix for %s sequences...' % len(seq_df))
            print('     Beware that pairwise distance matrix for more than 10k samples may take a long time or run out of memory')
            
        #Distance_matrix = squareform(pdist(vector_array, metric))
        #STILL TOO SLOW !!!, need to implement sparse !
        #https://stackoverflow.com/questions/17627219/whats-the-fastest-way-in-python-to-calculate-cosine-similarity-given-sparse-mat
        
        if metric.lower() == 'cosine':
            #Implementation from Klenshtein
            matches_fast_s= awesome_cossim_top(vector_array, vector_array.transpose(), 1800, 0.5)
            clusters = assign_clones(matches_fast_s,clone_threshold)
        else:
            Distance_matrix = squareform(pdist(vector_array, metric))
            Z = linkage(Distance_matrix, 'complete')
            clusters = fcluster(Z, clone_threshold, criterion='distance')
        
        final_clusters = []
        for i in representor:
            final_clusters.append(clusters[i])
        
    # |--------------------------------------------------------------------------|
    # |--------------------------------------------------------------------------|

    elif method.lower() in ['vdjunction', 'vdjunctionhl','vjj','vdj']:
        
        junctions = seq_df_.loc[:,'junctionH'].values
        seq_df = seq_df_.drop_duplicates(subset='junctionH')
        unique_junctions = list(seq_df.loc[:,'junctionH'].values)
        representor = [unique_junctions.index(x) for x in junctions]
        seq_df.index = np.arange(len(seq_df))
        
        if metric is None:
            metric = 'levenshtein'
        
        if metric.lower() not in ['levenshtein', 'hamming']:
            print('ERROR: The supported metrics for method alignfree are ')
            print('Levenshtein and Hamming, but you chosed %s' % metric)
            return None
        le = preprocessing.LabelEncoder()
        if method.lower() == 'vdjunctionhl':
            clusters0 = group_seq_cluster(seq_df, keys=['VgeneH', 'JgeneH', 'VgeneL', 'JgeneL'])
        else:
            clusters0 = group_seq_cluster(seq_df, keys=['VgeneH', 'JgeneH'])
            
        junctions = seq_df['junctionH'].to_numpy()

        HAC_clusters = clusters0.copy()
        clone_ID_list = list(set(clusters0))
        nclones = len(clone_ID_list)
        for ci,cloneID in enumerate(clone_ID_list):
            subclones_index = np.where(clusters0 == cloneID)[0]
            nsubclones = np.size(subclones_index)
                
            junction_set = list(set(junctions[subclones_index]))
            nsubclones_set = len(junction_set)
                
            if len(junctions[subclones_index[0]]) > 0 and nsubclones_set > 1:
                if verbose:
                    print()
                    print("   Clone %s/%s" % (ci+1,nclones))
                    print("   %s unique subclones" % nsubclones_set)
                    print("   %s total subclones" % nsubclones)
                Hamming_matrix = np.zeros((nsubclones_set,nsubclones_set))
                for si in range(nsubclones_set):
                    Hamming_matrix[si,si] = 0
                for si in range(nsubclones_set):
                    for sj in range(nsubclones_set):
                        Hamming_matrix[si,sj] = Normalized_Levenshtein_dist(junction_set[si],junction_set[sj])
                        Hamming_matrix[sj,si] = Hamming_matrix[si,sj]
            
                #do HAC, create new clusters (check raman)
                X = squareform(Hamming_matrix)
                Z = linkage(X, 'complete')
                clusters = fcluster(Z, clone_threshold, criterion='distance')
                    
                                        
                junction_cluster = dict()
                for i in range(len(junction_set)):
                    junction_cluster[junction_set[i]] = clusters[i]
                    
                n_clust = int(np.max(HAC_clusters))
                if n_clust > 1:
                    for s in subclones_index:
                        HAC_clusters[s] = int((clusters0[s]+100000)*1000 + junction_cluster[junctions[s]]) #make sure we dont overlap with an existing cluster
        le.fit(HAC_clusters)
        clusters = le.transform(HAC_clusters)
        
        final_clusters = []
        for i in representor:
            final_clusters.append(clusters[i])
       
        
       
    else:
        return None
        
    final_clusters = np.array(final_clusters)
    singletons = detect_singletons(final_clusters)
    return final_clusters, singletons


def detect_singletons(clusters):
    counter_dict = Counter(clusters)
    clone_count = np.array([counter_dict[cluster] for cluster in clusters])
    singletons = (clone_count==1)
    
    return singletons



def group_seq_cluster(df: pd.DataFrame, keys:list):
    
    '''Note that df should be indexed from 0 to N, without break'''
    
    nseq = len(df)
    if keys is None:
        return np.zeros(nseq).astype(int)
    groups = df.groupby(list(keys)).groups
    clone_cluster = np.zeros(nseq).astype(int)
    
    i = 1
    for keys,indexes in groups.items():
        for value in indexes:
            clone_cluster[value] = i
        i+= 1
        
    return clone_cluster


def get_kmer_representations_both(sequences, sequences_neg, k=4, L=130):
    
    seq_full = list(sequences) + list(sequences_neg)
    len_seq = len(sequences)
    tf_idf = get_kmer_representation(seq_full, k=4, L=130)
 
    return tf_idf[:len_seq,:], tf_idf[len_seq:,:]


def get_kmer_representation(sequences, k=4, L=130):
    len_df = len(sequences)
    
    def cal_tf_idf(sequences, k):
        textword = [getKmers(x,k=k) for x in sequences]
        for i in range(len(textword)):
            textword[i] = ' '.join(textword[i])
        vec = TFIDF()
        # Default L2 regularization
        tfidf = vec.fit(textword)
        X = tfidf.transform(textword)
        # Produce tf-idf matrix
        kmers = tfidf.get_feature_names()
        idf = tfidf.idf_
        return X.toarray(), idf
    
    def getKmers(sequence:str, k=4):
        """
        Break DNA into kmer and process into word format.
        :param sequence: a DNA sequence
        :return:
        """
        # including 'k' increases a lot of memory usage: 5^k - 4^k
        return [sequence[x:x+k].lower() for x in range(len(sequence)-k+1) if 'n' not in sequence[x:x+k].lower()]    
    
    tf_idf, idf = cal_tf_idf(sequences, k=k) 
    return tf_idf



def compute_negation_threshold(array_sample, array_neg, metric = 'Cosine', plot = False):
    
    array_sample = array_sample[:5000]
    array_neg = array_neg[:5000]
    nseq = len(array_sample)
    nseq_neg = len(array_neg)
    if metric.lower() in ['lev', 'levenshtein', 'ham', 'hamming']:
        Distance_matrix_neg = np.ones((nseq,nseq_neg)) #TODO, axis 1 or 0 ?
        for si, seqi in enumerate(array_sample):
            for sj, seqj in enumerate(array_neg):
                if metric.lower() in ['lev', 'levenshtein']:
                    dist = Normalized_Levenshtein_dist(seqi, seqj)
                else:
                    dist = Normalized_Hamming_dist(seqi, seqj)
                Distance_matrix_neg[si,sj] = dist
                
        n_nearest_neg = np.argmin(Distance_matrix_neg, axis = 1) 
        dist_to_nearest_neg = np.array([Distance_matrix_neg[i,n_nearest_neg[i]] for i in range(nseq)])
                
    elif metric.lower() in ['cos', 'cosine'] and False:
        matches_fast_neg = awesome_cossim_top(array_sample,array_neg.transpose(), 1800, 0.5)
        dist_to_nearest_neg = compute_dist2nearest(matches_fast_neg)
    
    else:
        Distance_matrix_neg = cdist(array_sample, array_neg, metric) 
        n_nearest_neg = np.argmin(Distance_matrix_neg, axis = 1) 
        dist_to_nearest_neg = np.array([Distance_matrix_neg[i,n_nearest_neg[i]] for i in range(nseq)])
        

    #d_threshold = np.percentile(dist_to_nearest_neg, 3)
    d_threshold = find_tolerance_threshold(dist_to_nearest_neg)
    print('    Threshold set to %.2f' % d_threshold)     
    
    if plot:
        plt.hist(dist_to_nearest_neg, bins=25, density=True, color = 'green', alpha = 0.5)
        plt.xlim(xmin=0)
        plt.axvline(x=d_threshold, color='black', ls='--')
        plt.yscale('log')
        plt.xlabel('Distance to Nearest')
        plt.ylabel('Density')
        plt.show()
        
    return d_threshold


def compute_dist2nearest(matches_fast):
    
    def sort_coo(csr_row):
        result=zip(csr_row.indices,csr_row.data)
        return sorted(result,key=lambda x: -x[1])
    
    dist2nearestcosine=[]
    for i in range(0,matches_fast.shape[0]):
        if sort_coo(matches_fast[i,:]).__len__()>1:
            second_val=sort_coo(matches_fast[i,:])[1][1]
        else:
            second_val=0
        dist2nearestcosine=np.append(dist2nearestcosine,1-second_val)
       
    return dist2nearestcosine 




def find_tolerance_threshold(distance_array, tol = 0.03):
    
    '''
    Input:
        distance_array: 1D dimensional array of nearest neighbor distance
        tol: tolerance in %
    Output:
        cutoff distance such that only tol% of points are below that distance
    '''
    
    min_dist = np.min(distance_array)
    max_dist = np.max(distance_array)
    
    if min_dist == max_dist:
        print('WARNING: All distances are the same (returns 0)')
        return 0
    
    else:
        test_cutoff = np.linspace(min_dist,max_dist, num = 1000)
        
        i = 0
        FPR = 0
        ns = len(distance_array)
        while FPR < tol or i == ns-2:
            i += 1
            cutoff = test_cutoff[i]
            nwhere = np.where(distance_array < cutoff)[0]
            FPR = len(nwhere)/ns * 100
            
        return cutoff




def Normalized_Hamming_dist(string1,string2):
    """Returns the Hamming distance between array A and B
    if A and B are of different length, the distance is 1"""
    if len(string1) != len(string2):
        return 1
    else:
        H = 0
        for i in range(len(string1)):
            if string1[i] != string2[i]:
                H += 1     
        return H/len(string1)


def Normalized_Levenshtein_dist(string1, string2):
    """
    [ref] Yujian, Li, and Liu Bo. "A normalized Levenshtein distance metric." 
    IEEE transactions on pattern analysis and machine intelligence 29.6 (2007): 1091-1095.
    """
    if len(string1)==0 and len(string2)==0:
        return 1
    else:
        Lev = Levenshtein.distance(string1, string2)
        norm_lev = 2*Lev/(len(string1)+len(string2)+Lev)
        return norm_lev


def Cosine_dist(vec1, vec2):
    "Calculate the cosine distance between two vectors of te same dimension."
    if len(vec1) != len(vec2):
        raise ValueError("different length! Cannot compute the inner product.")
    return 1-np.dot(vec1, vec2)


def fast_cosine_pairwise(A): #Not used

    # base similarity matrix (all dot products)
    # replace this with A.dot(A.T).toarray() for sparse representation
    similarity = np.dot(A, A.T)
    
    # squared magnitude of preference vectors (number of occurrences)
    square_mag = np.diag(similarity)
    
    # inverse squared magnitude
    inv_square_mag = 1 / square_mag
    
    # if it doesn't occur, set it's inverse magnitude to zero (instead of inf)
    inv_square_mag[np.isinf(inv_square_mag)] = 0
    
    # inverse of the magnitude
    inv_mag = np.sqrt(inv_square_mag)
        
    # cosine similarity (elementwise multiply by inverse magnitudes)
    cosine = similarity * inv_mag
    cosine = cosine.T * inv_mag
    
    return cosine


def sparse_fast_cosine_pairwise(A): #Not used
    
    A_sparse = sparse.csr_matrix(A)
    similarities = cosine_similarity(A_sparse)
    #similarities_sparse = cosine_similarity(A_sparse,dense_output=False)
    
    return similarities


def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = sparse.csr_matrix(A)
    B = sparse.csr_matrix(B)
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return sparse.csr_matrix((data,indices,indptr),shape=(M,N))



def assign_clones(matches_fast,thresh_cosine):
    from scipy.sparse import find
    M=matches_fast.shape[0]
    M_L=M+1
    clusters_cosine_full=np.array(list(range(M_L+1,M+M_L+1)))
    t=0
    for i in range(0,M):
        matches_clust_ind=find(matches_fast[i,:]>1-thresh_cosine)
        if (matches_clust_ind[1].shape[0]>1):

            temp=np.where(clusters_cosine_full[matches_clust_ind[1]]<M_L)[0]
            if temp.shape[0]==0:
                clusters_cosine_full[matches_clust_ind[1]]=t
                t=t+1
            else: 
                clusters_cosine_full[matches_clust_ind[1]]=clusters_cosine_full[matches_clust_ind[1][temp[0]]]
    clusters_cosine_full[clusters_cosine_full>M_L]=clusters_cosine_full[clusters_cosine_full>M_L]-M_L\
    +np.max(clusters_cosine_full[clusters_cosine_full<M_L])
    return clusters_cosine_full









"""
   -----------------------------------------------------------------------------
   ----------------------------- DIVERSITY METRICS -----------------------------
   -----------------------------------------------------------------------------
   
    Implementation various diversity metric for biological samples,
    and similarity metric between samples.

    A sample is a dictionary containing the name of the species as a key, 
    and the number of detected individual for that species as a value. ex:
        sample["mouse"] = 5
        sample["rat"] = 10

    During the calculations, the occurences are always normalized to the total number of detected individuals

    [ref] Hill MO. Diversity and evenness: a unifying notation and its consequences. 
          Ecology. 1973 Mar;54(2):427-32.
"""


# ----------------------- Biodiversity tools ----------------------- #
def normalize_sample(sample):
    Ntot = np.sum(np.array(list(sample.values())).astype(np.float))
    norm_sample = {k: float(v) / Ntot for k, v in sample.items()}
    return norm_sample



def cal_accumulation_curve(sample, Nrepeat = 100):
    """Calculate the species accumulation curve"""
    speciesID = []  # build a list of all individual wih their species
    for species, count in sample.items():
        for i in range(count):
            speciesID.append(species)

    Ntot = len(speciesID)
    accumulation = np.zeros(Ntot)
    for ni in range(Nrepeat):
        species_set = set()
        random_individuals = random.sample(range(Ntot), Ntot)
        i = 0
        for indiv in random_individuals:
            species_set.add(speciesID[indiv])
            accumulation[i] += len(species_set)
            i += 1

    return accumulation/Nrepeat


# ----------------------- Diversity indexes ----------------------- #
def Hill_diversity(sample, q):
    inf_threshold = 100
    if q == 0:
        Diversity = np.count_nonzero(np.array(list(sample.values())))
    elif q > 100:
        Diversity = 1/dominance(sample)
    else:
        sample = normalize_sample(sample)
        pi = np.array(list(sample.values()))  # relative  abundance  of  species
        pi = pi[pi > 0]
        if q == 1:  # exponential of Shanon entropy
            Diversity = np.exp(np.sum(-pi * np.log(pi)))
        elif q >= inf_threshold:
            Diversity = 1 / np.max(pi)
        else:
            Diversity = np.power(np.sum(np.power(pi, q)), 1 / (1 - q))
    return Diversity

def richness(sample):
    sample = {k: float(v) for k, v in sample.items()}
    ki = np.array(list(sample.values()))
    S_obs = np.count_nonzero(ki)
    return S_obs

def richness_chao(sample):
    """
     [ref] A.  Chao,  “Nonparametric  estimation  of  the  number  of  classes  in  a  population"
           Scandinavian Journal of statistics, pp. 265–270, 1984.
    """
    sample = {k: float(v) for k, v in sample.items()}
    ki = np.array(list(sample.values()))
    S_obs = np.count_nonzero(ki)

    if np.min(ki) < 1:
        denormalize_factor = int(1 / np.min(ki))
        sample = {k: v * denormalize_factor for k, v in sample.items()}
        ki = np.array(list(sample.values()))
    f1 = np.size(np.where(ki == 1))
    f2 = np.size(np.where(ki == 2))

    if f1 == 0 or f2 == 0:
        S_chao = S_obs
    else:
        S_chao = S_obs + f1 * (f1 - 1) / (2 * (f2 + 1))
    return S_chao


def Shannon_entropy(sample):
    entropy = np.log(Hill_diversity(sample, 1))
    return entropy


def Shannon_entropy_Chao(sample):
    """
     [ref] A. Chao and T.-J. Shen, “Nonparametric estimation of shannon’s index of diversity
           when there are unseen species in sample,”Environmental and ecological statistics,
           vol. 10, no. 4, pp. 429–443, 2003.
    """
    sample = {k: float(v) for k, v in sample.items()}
    ki = np.array(list(sample.values()))
    if np.min(ki) < 1:
        denormalize_factor = int(1 / np.min(ki))
        sample = {k: v * denormalize_factor for k, v in
                  sample.items()}  # Sample should not be normalized to compute Shanon entropy
        ki = np.array(list(sample.values()))
    Ntot = np.sum(np.array(list(sample.values())).astype(np.float))
    f1 = np.size(np.where(ki == 1))
    C = 1 - f1 / Ntot

    pi = ki / Ntot * C
    pi = pi[pi > 0]
    entropy_chao = np.sum(-pi * np.log(pi) / (1 - np.power(1 - pi, Ntot)))
    return entropy_chao


def Simpson_index(sample):
    # probability that two  entities  taken  at  random  from
    # the  dataset  are  of  the  same  type
    Simpson = 1 / Hill_diversity(sample, 2)
    return Simpson


def eveness(sample, a=1, b=0):
    Eveness = Hill_diversity(sample, a) / Hill_diversity(sample, b)
    return Eveness


def eveness_chao(sample):
    Eveness_chao = np.exp(Shannon_entropy_Chao(sample)) / richness_chao(sample)
    return Eveness_chao


def dominance(sample):
    sample = normalize_sample(sample)
    Dominance = np.max(list(sample.values()))
    return Dominance


# ----------------------- Similarity indexes ----------------------- #
def Dice_similarity(sample1, sample2, normalize=True):
    if normalize == True:
        sample1 = normalize_sample(sample1)
        sample2 = normalize_sample(sample2)

    species_list = set(list(sample1.keys()) + list(sample2.keys()))
    Dice = 0
    for species in species_list:
        if species in sample1.keys() and species in sample2.keys():
            Dice += min(sample1[species], sample2[species])
    return Dice


def Jaccard_similarity(sample1, sample2):
    Dice = Dice_similarity(sample1, sample2)
    Jaccard = Dice / (2 - Dice)
    return Jaccard



# --------------------- Diversity profile ------------------------- #

def diversity_profile(sample, n=100):
    a = np.linspace(-1,1,num=n)
    alphas = transform_func(a)
    div_profile = np.zeros(n)
    for ai, alpha in enumerate(alphas):
        div_profile[ai] = Hill_diversity(sample, alpha)
        
    return div_profile, alphas
        

# get a series of alpha by transformation function
def transform_func(initial_axis, factor = 0.75):
    y1 = np.tan(math.pi*initial_axis/2)
    y2 = np.zeros(len(y1))
    y2[y1<=1e3] = np.exp(y1[y1<1e3]/factor)
    y2[y1>1e3] = np.inf
    
    return y2

def rev_transform(y2, factor = 0.75):
    try:
        L=len(y2)
    except:
        y2 = np.array([y2])
    y2 = np.array(y2)
    y1 = np.zeros(len(y2))
    y1[y2>0] = np.log(y2[y2>0])*factor
    y1[y2==0] = -np.inf
    
    initial_axis = np.arctan(y1)*2/math.pi
    return initial_axis