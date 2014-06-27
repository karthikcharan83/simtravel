%module skimsquery

%{
    #define SWIG_FILE_WITH_INIT
    #include "skimsquery.h"
%}

%include "numpy.i"
%init %{
    import_array();
%}

%apply (int* IN_ARRAY1, int DIM1) {(int * origin, int origin_size)}
%apply (int* IN_ARRAY1, int DIM1) {(int * dest, int dest_size)}
%apply (int* IN_ARRAY1, int DIM1) {(int * nodes_available, int nodes_available_size)}
%apply (int* IN_ARRAY1, int DIM1) {(int * seed, int seed_size)}

/*%apply (int* INPLACE_ARRAY2, int DIM1, int DIM2) {(int * nodes_available, int nodes_available_dim1, int nodes_available_dim2)}*/
%apply (int* INPLACE_ARRAY2, int DIM1, int DIM2) {(int * locations, int locations_dim1, int locations_dim2)}

%apply (double* INPLACE_ARRAY1, int DIM1) {(double * tt, int tt_size)}
%apply (double* IN_ARRAY1, int DIM1) {(double * available_tt, int available_tt_size)}
%apply (double* INPLACE_ARRAY1, int DIM1) {(double * dist, int dist_size)}
%apply (double* IN_ARRAY1, int DIM1) {(double * votd, int votd_size)}


%inline %{
    /*  takes as input two numpy arrays */
    void get_dist_w(struct Mode mode, int skim_index, int * origin, int origin_size, int * dest, int dest_size, double * dist, int dist_size, int size) {
        /*  calls the original funcion, providing only the size of the first */
        get_dist(mode, skim_index, origin, dest, dist, size);
    }
%}

%inline %{
    /*  takes as input two numpy arrays */
    void get_tt_w(struct Mode mode, int skim_index, int * origin, int origin_size, int * dest, int dest_size, double * tt, int tt_size, double * votd, int votd_size, int size) {
        /*  calls the original funcion, providing only the size of the first */
        get_tt(mode, skim_index, origin, dest, tt, votd, size);
    }
%}

%inline %{
    /*  takes as input two numpy arrays */
    void get_locations_w(struct Mode mode, int skim_index, int * origin, int origin_size, 
                        int * dest, int dest_size, double * available_tt, int available_tt_size, 
                        double * votd, int votd_size, int size, int * nodes_available, int nodes_available_size,
                        int * locations, int locations_dim1, int locations_dim2, int count,
                        int * seed, int seed_size) {
        /*  calls the original funcion, providing only the size of the first */
        get_locations(mode, skim_index, origin, dest, available_tt, votd, size, nodes_available, nodes_available_size, locations, count, seed);
    }
%}


%include "skimsquery.h"

