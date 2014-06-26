#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <malloc.h>
#include <string.h>

char *input_file_name;
char *output_file_name;
char *temp_file_name_1;
char *temp_file_name_2;
char *temp_file_name_3;


/* delete and rename the file */
void delete_file(char *file_name)
{
    int removeFile;
    
    //delete the file
    removeFile = remove(file_name);
    if(removeFile != 0)
        printf("C--> Error removing file \n");

}

void rename_file(char *old_file, char *new_file)
{
    int renameFile;

    //rename the file
    //rename(rename from, rename to)
    renameFile = rename(old_file, new_file);
    if(renameFile != 0)
        printf("C--> Error renaming file \n");
        
}


/*
This method creates a new file and saves the travel times after a transpose.
Arguments:
interval - the interval length i.e after what interval the links repeat. example: 20522
number_intervals - the number of intervals that are present in the input file. example: 1400
file1 - input file to read all the links from
file2 - temporary file
file3 - temporary file
file4 - final output file name
file2 and file3 need be created. the files are created when the code executes.
*/
void flatten_link_attributes(int interval, int number_intervals, char *input_file_name, char *output_file_name, char *refLinkOrder)
{
	float **org_graph, **ord_graph, *ordToStore_graph;
	int i, j, k, length, intOrder;

	float travel_time, fin_tt;
	float temp1, temp2, temp3, temp4, temp5, temp6, temp, stNode, endNode, rowNo;
	char tt_temp[10];

	char *temp_str;

	FILE *ip_file, *tp_file_2, *ref_file;

	//initialize mystring and temp string
	
	temp_str = (char *)malloc(1000*sizeof(char));
	//mystring = (char *)malloc(10*sizeof(char));
	

	//initialize the 2D array to the number of edges times 1440
    	org_graph = (float **)malloc(interval*sizeof(float *));
    	for(i = 0; i < interval; i++)
    	{
        	org_graph[i] = (float *)malloc(number_intervals*sizeof(float));

    	}


	//initialize the graph to store the edges REFERENCE order
    	ord_graph = (float **)malloc(interval*sizeof(float *));
    	for(i = 0; i < interval; i++)
    	{
        	ord_graph[i] = (float *)malloc(3*sizeof(float));

    	}

	//initialize the graph to store the order in which the rows need to be stored
    	ordToStore_graph = (float *)malloc(interval*sizeof(float));


	// populate the reference order graph
	ref_file = fopen(refLinkOrder, "r");

	if (ref_file !=NULL)
	{
		
		for(j = 0; j < interval; j++)
		{
			fscanf(ref_file, "%f,%f,%f,%f,%f,%f,%f", &rowNo, &temp2, &temp3, &temp4, &temp5, &stNode, &endNode);
			ord_graph[j][0] = rowNo;
			ord_graph[j][1] = stNode;
			ord_graph[j][2] = endNode;
			//printf("%f, %f, %f", rowNo, stNode, endNode);
		}
	}
	else
	{
	printf("ref file not found- %s", refLinkOrder);
	}




	//open the files and assigning the graph for link skims
	ip_file = fopen(input_file_name, "r");
	
	if(ip_file != NULL)
	{
		fscanf(ip_file, "%s", temp_str);
		printf("Header - %s", temp_str);
		//Identifying the order in which records need to be written
		for(i = 0; i < 1; i++)
		{
			printf("\n\t-->Interval count - %d", i);

			for(j = 0; j < interval; j++)
			{
				fscanf(ip_file, "%f;%f;%f;%f;%f;%f;%f", &temp1, &temp2, &temp3, &temp4, &temp5, &temp6, &travel_time);
				org_graph[j][i] = travel_time;

				for (k = 0; k < interval; k++)
				{

					//printf("lnk_St-%f, lnk_En-%f, ord_st-%f, ord_en-%f\n", temp1, temp2, ord_graph[k][1], ord_graph[k][2]);
					if (temp1 == ord_graph[k][1] & temp2 == ord_graph[k][2])
					{
					 	ordToStore_graph[k] = j;
						//printf("\nrow - %f %f, order - %f", temp1, temp2, ord_graph[k][0]);
					}

				}
			

			}
		}


		for(i = 1; i < number_intervals; i++)
		{

			printf("\n\t-->Interval count - %d", i);

			for(j = 0; j < interval; j++)
			{
				fscanf(ip_file, "%f;%f;%f;%f;%f;%f;%f", &temp1, &temp2, &temp3, &temp4, &temp5, &temp6, &travel_time);
				org_graph[j][i] = travel_time;
			}
		}

	}
		
		printf("\nLink 1: ");
		for(j = 0; j < number_intervals; j++)
		{
			printf("%f\t", org_graph[0][j]);		

		}



		printf("\nLink 2: ");
		for(j = 0; j < number_intervals; j++)
		{
			printf("%f\t", org_graph[1][j]);		

		}




	//Writing to file
	tp_file_2 = fopen(output_file_name, "w");

	if(tp_file_2 != NULL)
	{
		//now open the files for writing
		for(i = 0; i < interval; i++)
		{

			intOrder = (int) ordToStore_graph[i];
			//printf("MATCH FOUND - %d", i);
			//keep reading the file
			for(j = 0; j < number_intervals; j++)
			{
				sprintf(tt_temp, "%f", org_graph[intOrder][j]);
				fputs(tt_temp, tp_file_2);
				if (j < number_intervals -1)
				{
				fputs(" ", tp_file_2);
				}
			}
			fputs("\n", tp_file_2);

		}
	}
}
