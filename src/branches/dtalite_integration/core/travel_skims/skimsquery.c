#include<stdio.h>
#include<stdlib.h>
#include<malloc.h>
#include<math.h>
#include<string.h>

#include "skimsquery.h"

struct Mode alloc_mode(struct Mode mode)
{
    int x;

    mode.skims = (struct Skim *)malloc(mode.count_skims*sizeof(struct Skim));


    for (x = 0; x < mode.count_skims; x++)
    {
        mode.skims[x] = alloc_skim_memory(mode.nodes);
    }
    return mode;
}


struct Skim alloc_skim_memory(int nodes)
{
    //initialize the 2D array to the size of the number of nodes
    int x, matrix_size;
    struct Skim skim;

    matrix_size = nodes+1;

    //The matrix size is actually (nodes + 1) X (nodes + 1)
    //Actual data gets stored in indexes 1 through nodes
    //Therefore, when looping through the matrix go from 1 through nodes


    skim.tt_matrix = (float **)malloc(matrix_size*sizeof(float *));
    skim.dist_matrix = (float **)malloc(matrix_size*sizeof(float *));

    //create all the nodes
    for(x = 0; x <= nodes; x++)
    {
	skim.tt_matrix[x] = (float *)malloc(matrix_size*sizeof(float));
	skim.dist_matrix[x] = (float *)malloc(matrix_size*sizeof(float));
    }
    //printf("\nC--> Graph created");
    return skim;
}

void populate_skim(struct Mode mode, int index, char *loc)
{
    int x, origin, dest, num_records;
    float tt, dist;
    //open the file to read data
    //printf("\nC--> Starting to populate - %d skim", index);
    num_records = mode.nodes * mode.nodes;

    FILE *fileSkim = fopen(loc, "r");
    if(fileSkim != NULL)
    {
        for(x = 0; x < num_records; x++)
        {
            //read the origin, destination, tt (in min), and distance (in miles else need to add conversion factor /5280.0) and save it
            fscanf(fileSkim, "%d, %d, %f, %f", &origin, &dest, &tt, &dist);
	    //printf("%d, %d, %f, %f\n", origin, dest, tt, dist);
            //set the value of tt to the graph
            mode.skims[index].tt_matrix[origin][dest] = tt;
	    mode.skims[index].dist_matrix[origin][dest] = dist;
        }
        fclose(fileSkim);
    }
    else
    {
        //error if file is null
        perror(loc);
    }
    //printf("\nC--> Travel time matrix populated");
}
/*
void get_tt(struct Mode mode, int skim_index, int *origin, int *dest, double *tt, int size)
{
    //local variables
    int x;

    //get the travel times using the origin and destination
    for ( x = 0; x < size; x++ )
    {
        //if origin or destination are zero set travel time to 0
        if (origin[x] == 0 | dest[x] == 0)
        {
            tt[x] = 0;
            continue;
        }
        tt[x] = mode.skims[skim_index].tt_matrix[origin[x]][dest[x]];            
        //printf("\nthis is what is assigned - %d,%d,%.4f", origin[x], dest[x],res.data[x]);   
    }
    //printf("\nC--> Travel times retrieved");
}
*/
void get_dist(struct Mode mode, int skim_index, int *origin, int *dest, double *dist, int size)
{
    //local variables
    int x;

    //get the travel times using the origin and destination
    for ( x = 0; x < size; x++ )
    {
        //if origin or destination are zero set dist to 0
        if (origin[x] == 0 | dest[x] == 0)
        {
            dist[x] = 0;
            continue;
        }
        dist[x] = mode.skims[skim_index].dist_matrix[origin[x]][dest[x]];
    }
}

void get_tt(struct Mode mode, int skim_index, int *origin, int *dest, double *tt, double *votd, int size)
{
    //local variables
    int x;
    double tempdist;
    double temptt;

    //get the travel times using the origin and destination
    for ( x = 0; x < size; x++ )
    {
        if (origin[x] == 0 | dest[x] == 0)
        {
            tt[x] = 0;
            continue;
        }
        //if origin or destination are zero the location is invalid. set travel time to 0
        temptt = mode.skims[skim_index].tt_matrix[origin[x]][dest[x]];
        tempdist = mode.skims[skim_index].dist_matrix[origin[x]][dest[x]];

	tt[x] = temptt + tempdist*votd[x];
        if (tt[x] < 3)
        {
            tt[x] = 3;
        }
    }
}

void print_2d_array(int *arr, int dim1, int dim2)
{
    int x,y;
    printf("\nPrinting array of dimensions - (%d,%d)\n", dim1, dim2);
    for (x = 0; x < dim1; x++)
    {
        for (y = 0; y < dim2; y++)
        {
            printf("%d,", arr[x*dim2 + y]);
        }
        printf("\n");
    }
}

void print_1d_array(int *arr, int dim1)
{
    int x,y;
    printf("\nPrinting array of dimensions - (%d)\n", dim1);
    for (x = 0; x < dim1; x++)
    {
        printf("%d,", arr[x]);
    }
    printf("\n");
}


void get_locations(struct Mode mode, int skim_index, int *origin, int *dest, double *available_tt, double *votd, int size, int *nodes_available, int nodes_available_size, int *locations, int count, int* seed)
{
    //local variables
    //TODO: Change nodes_available to be individual specific
    int x, y, node, from, to, count_sampled, count_nodes, rand_node_index, seed_x;
    double tt_from, tt_to, dist_from, dist_to, gen_tt_from, gen_tt_to;
    int* nodes_checked_copy;
    int* nodes_checked;

    srand(seed[0]);

    nodes_checked_copy = (int *)malloc(nodes_available_size*sizeof(int));
 
    for (x = 0; x < nodes_available_size; x++)
    {
        nodes_checked_copy[x] = 0;
    }
    
    for (x = 0; x < size; x++)
    {
        from = origin[x];
        to = dest[x];

        if (from == 0 | to == 0)
        {
            continue;
        }

        count_sampled = 0;
        count_nodes = 0;
	//seed_x = seed[x];
        //srand(seed_x); TODO: Moving this to outside the loop because the seed
        // is same across individuals needs to be changed once seed varies across
        // individuals

        // Implementation where the number of options is less than the count
        if (nodes_available_size <= count)
        {
            for (y = 0; y < nodes_available_size; y++)
            {
                node = nodes_available[y];
                tt_from = mode.skims[skim_index].tt_matrix[origin[x]][node];
                tt_to = mode.skims[skim_index].tt_matrix[node][dest[x]];

                dist_from = mode.skims[skim_index].dist_matrix[origin[x]][node];
                dist_to = mode.skims[skim_index].dist_matrix[node][dest[x]];

                gen_tt_from = tt_from + dist_from*votd[x];
                gen_tt_to = tt_to + dist_to*votd[x];

	        if (gen_tt_from < 3)
	        {
	            gen_tt_from = 3;
	        }

	        if (gen_tt_to < 3)
	        {
	            gen_tt_to = 3;
	        }

                if (gen_tt_from + gen_tt_to <= available_tt[x])
                {
                    locations[x*count + count_sampled] = node;
                    count_sampled = count_sampled + 1;
                }
            }
            continue;
        }
    
        // Implementation where the number of options is more than the count
        nodes_checked = (int *)malloc(nodes_available_size*sizeof(int));
        //memcpy(&nodes_checked, &nodes_checked_copy, sizeof(nodes_checked_copy));
        //printf("\nThis is the checked array");
        //print_1d_array(nodes_checked, nodes_available_size);
        //printf("\nThis is the default copy");
        //print_1d_array(nodes_checked_copy, nodes_available_size);
        memset(nodes_checked, 0, nodes_available_size*sizeof(int));

        //printf("\nFirst origin-%d,dest-%d", origin[x],dest[x]);
        while((count_sampled < count) & (count_nodes < nodes_available_size))
        {
            rand_node_index = rand() % nodes_available_size;
            //printf("\n\t%d rand node is - %d",count_sampled, nodes_available[rand_node_index]);
            if (nodes_checked[rand_node_index] == 1)
            {
                continue;
            }
            nodes_checked[rand_node_index] = 1;
            node = nodes_available[rand_node_index];
            count_nodes = count_nodes + 1;

            tt_from = mode.skims[skim_index].tt_matrix[origin[x]][node];
            tt_to = mode.skims[skim_index].tt_matrix[node][dest[x]];

            dist_from = mode.skims[skim_index].dist_matrix[origin[x]][node];
            dist_to = mode.skims[skim_index].dist_matrix[node][dest[x]];

            gen_tt_from = tt_from + dist_from*votd[x];
            gen_tt_to = tt_to + dist_to*votd[x];

	    if (gen_tt_from < 3)
	    {
	        gen_tt_from = 3;
	    }

	    if (gen_tt_to < 3)
	    {
	        gen_tt_to = 3;
	    }


            if (gen_tt_from + gen_tt_to <= available_tt[x])
            {
                locations[x*count + count_sampled] = node;
                count_sampled = count_sampled + 1;
                //printf("\nThis node is selected - %d ", node);
            }
        }
    }
}
 

void release_memory(struct Mode mode)
{
    int x, y;

    for(x = 0; x <= mode.count_skims; x++)
    {
	for(y = 0; y <= mode.count_skims; y++)
        {
	    free(mode.skims[x].tt_matrix[y]);
	    free(mode.skims[x].dist_matrix[y]);
	}
        free(mode.skims[x].tt_matrix);
        free(mode.skims[x].dist_matrix);
    }
    mode.skims[x].tt_matrix = NULL;
    mode.skims[x].dist_matrix = NULL;
    printf("\nC--> Graph deleted");
        
}

