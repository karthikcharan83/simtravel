struct Skim {
  float **tt_matrix;
  float **dist_matrix;
  char *loc;
};

struct Mode {
  struct Skim *skims;
  int count_skims;
  int nodes;
  char *desc;
};

typedef struct {
  float *data;
  int len;
} Result1D;


struct Mode alloc_mode(struct Mode mode);
struct Skim alloc_skim_memory(int nodes);
void populate_skim(struct Mode mode, int index, char *loc);
//void get_tt(struct Mode mode, int skim_index, int *origin, int *dest, double *tt, int size);
void get_dist(struct Mode mode, int skim_index, int *origin, int *dest, double *tt, int size);
void get_tt(struct Mode mode, int skim_index, int *origin, int *dest, double *tt, double *votd, int size);
void get_locations(struct Mode mode, int skim_index, int *origin, int *dest, double *available_tt, double *votd, int size, int *nodes_available, int nodes_available_size, int *locations, int count, int* seed);
