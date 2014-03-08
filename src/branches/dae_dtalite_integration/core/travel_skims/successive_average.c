/* File: arrayex.c */
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<malloc.h>
#include<math.h>
#include<string.h>
#include "successive_average.h"

#define MAX 100

//declare the files
char *temp_file_name;
char *ts_file_name_1;
char *ts_file_name_2;
char *ts_write_file;

//dynamic array
float **avg_travel_skim;

//initialize edges and nodes
int nodes;
int edges;



/* String Functions */
/*********************************************/
/*
This function gets the file paths for the travel skims files and 
assigns them to the respective variables
*/
char* set_file(char *s)
{
    int length = 1;
    length = strlen(s);
    
    temp_file_name = (char *)malloc(length*sizeof(char));
    temp_file_name = s;
    
    return temp_file_name;
}

/*
This function prints the file paths of the travel skims files
*/
void print_file_path()
{
    printf("C--> printing the file names\n");
    printf("C--> file name 1:  %s\n", ts_file_name_1);
    printf("C--> file name 2:  %s\n", ts_file_name_2);
}
/*********************************************/


/*File functions */
/*********************************************/
/*
This function writes all the locations to the file
*/
void write_avg_ts_to_file()
{
    //write all locations to a temp file 
    int columns;
    FILE *fp = NULL;
    int i, j;
    
    printf("C--> Write to file\n");
    fp = fopen(ts_write_file, "w");
    columns = 3;

    //file open error return error message
    if(fp == NULL)
    {
        printf("C--> Error opening file ");
        printf("\n");
    }
    //else write all locations to file
    else
    {
        for(i = 0; i < edges; i++)
        {
            for(j = 0; j < columns; j++)
            {
                if(j == columns-1)
                {
                    fprintf(fp, "%g\n", avg_travel_skim[i][j]);
                }
                else
                {
                    fprintf(fp, "%d,", (int)avg_travel_skim[i][j]);
                }
            }
        }
        fclose(fp);
    }
    //after writing the file delete the old file and rename the new file
    delete_file(ts_file_name_1);
    rename_file(ts_write_file, ts_file_name_1);
}
/*********************************************/


/* Main functions */
/*********************************************/
/*
This function initializes the dynamic array/graph.
It allocates memory to the array/graph based on the number of nodes.
*/
void initialize_ts_array(int nodes_temp)
{
    int x;
    int columns;
    columns = 3;
    nodes = nodes_temp;
    edges = nodes * nodes;
    printf("C--> Nodes: %d Edges: %d \n", nodes, edges);
    printf("C--> Initializing average travel skims\n");
    
    //initialize the 2D array to the size of the number of nodes
    avg_travel_skim = (float **)malloc(edges*sizeof(float *));
        
    //create all the nodes
    for(x = 0; x < edges; x++)
    {
        avg_travel_skim[x] = (float *)malloc(columns*sizeof(float));
    }
    printf("C--> Graph created\n");
}


/*
This function reads the origin, destination and tt from a file.
It then sets the array/graph elements to tt read from the file.
*/
void set_ts_array(char *file_1, char *file_2, char *file_3, int iteration)
{
    int i, j;
    int org1, dest1;
    int org2, dest2;
    float tt1, tt2;
    int columns;
    float iter;

    iter = (float)iteration;
    
    printf("C--> Iteration: %d \n", iteration);
    columns = 3;
    
    //set all the file names
    ts_file_name_1 = set_file(file_1);
    ts_file_name_2 = set_file(file_2);
    ts_write_file = set_file(file_3);
    
    //open both the files to read data
    printf("C--> Opening the files\n");
    FILE *file1 = fopen(ts_file_name_1, "r");
    FILE *file2 = fopen(ts_file_name_2, "r");

    //process till end of file
    if( ts_file_name_1 != NULL && ts_file_name_2 !=NULL)
    {
        //read line by line from both files
        for(i = 0; i < edges; i++)
        {
            fscanf(file1, "%d, %d, %f", &org1, &dest1, &tt1);
            fscanf(file2, "%d, %d, %f", &org2, &dest2, &tt2);

            //if(org1 == org2 && dest1 == dest2)
            //{
                avg_travel_skim[i][0] = org1;
                avg_travel_skim[i][1] = dest1;
                avg_travel_skim[i][2] = (1/iter*tt1+(iter-1)/iter*tt2);
            //}
            /*else
            {
                avg_travel_skim[i][0] = 0;
                avg_travel_skim[i][1] = 0;
                avg_travel_skim[i][2] = 0;
                printf("C--> Org1 not equal to Org2. TT saved as zero. Invalid.\n");
            }*/
        }
        //close the file
        printf("C--> Closing the files\n");
        fclose(file1);
        fclose(file2);
    }
    else
    {
        //error if file is null
        printf("C--> Error reading the file.\n");
    }
    
    printf("C--> Graph created with new values\n");
}



/*
This function is used to delete the original graph 
and travel times array and free memory.
*/
void delete_ts_array()
{
    int i;
    
    //delete all the rows
    for ( i = 0; i < edges; i++ )
    {
        free(avg_travel_skim[i]);
    }
    
    //delete the pointer to the array
    free(avg_travel_skim);  
        
    //set the pointer to NULL to avoid any memory access
    avg_travel_skim = NULL;
    
    printf("C--> Array deleted\n");
}

/*********************************************/


/* Print functions */
/*********************************************/
/* Print the travel times array */
void print_ts_array()
{
    int i, j;    
    printf("C--> Printing avg travel skims\n");
    for(i = 0; i < 9; i++)
    //for(i = 0; i < edges; i++)
    {
        for(j = 0; j < 3; j++)
        //for(j = 0; j < nodes; j++)
        {
            printf("%f \t", avg_travel_skim[i][j]);
        }
        printf("\n");
    }
    printf("C--> Print complete\n");
}
/*********************************************/



/* File functions */
/*********************************************/
/* delete and rename the file */
void delete_file(char *s)
{
    int removeFile;
    
    //delete the file
    removeFile = remove(s);
    if(removeFile != 0)
        printf("C--> Error removing file \n");

}


void rename_file(char *s1, char *s2)
{
    int renameFile;

    //rename the file
    //rename(rename from, rename to)
    renameFile = rename(s1, s2);
    if(renameFile != 0)
        printf("C--> Error renaming file \n");
        
}
/*********************************************/




