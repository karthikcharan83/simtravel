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
void flatten_link_attributes(int interval, int number_intervals, char *file1, char *file2, char *file3, char *file4)
{
	int i, j;
	int test_interval;
	float travel_time, fin_tt;
	int no_of_intervals = 0;
	int file_flag = 0;
	int loop_counter = 0;
	float temp1, temp2, temp3, temp4, temp5, temp6, temp;
	int temp_tt;
	char mystring[20000];
	char tt_temp[10];
	int temp_int;
	int length = 1;
	char *temp_str;
	char* nl;
	FILE *ip_file, *tp_file_1, *tp_file_2;

	//set the file names
	length = strlen(file1) + 20;
    
    //initialize the file names
	input_file_name = (char *)malloc(length*sizeof(char));
    	temp_file_name_1 = (char *)malloc(length*sizeof(char));
	temp_file_name_2 = (char *)malloc(length*sizeof(char));
	output_file_name = (char *)malloc(length*sizeof(char));
    
	input_file_name = file1;
	temp_file_name_1 = file2;
	temp_file_name_2 = file3;
	output_file_name = file4;

	
	test_interval = interval;
	no_of_intervals = number_intervals;

	//initialize mystring and temp string
	
	temp_str = (char *)malloc(1000*sizeof(char));
	//mystring = (char *)malloc(10*sizeof(char));
	
	printf("File opened -->\n");

	//open input the file
	ip_file = fopen(input_file_name, "r");
	

	if(ip_file != NULL)
	{
		fscanf(ip_file, "%s", temp_str);
		printf("Header - %s", temp_str);
		//now open the files for writing
		for(i = 0; i < no_of_intervals; i++)
		{

			printf("\n\t-->Interval count - %d\n", i);
			//keep reading the file
			if(i == 0)
			{
				//first interval. read from input file only
				file_flag = 0;
				tp_file_2 = fopen(temp_file_name_2, "w");
                //write to file 2
				if(tp_file_2 != NULL)
				{
					for(j = 0; j < test_interval; j++)
					{
						fscanf(ip_file, "%f;%f;%f;%f;%f;%f;%f", &temp1, &temp2, &temp3, &temp4, &temp5, &temp6, &travel_time);
						//tt_temp = itoa(travel_time, tt_temp, 10);
						sprintf(tt_temp, "%f", travel_time);
						fputs(tt_temp, tp_file_2);
						//printf("Travel time - %f; string travel time - %s\n", travel_time, tt_temp);
						fputs("\n", tp_file_2);
					}
				fclose(tp_file_2);
				}
			else
			{
			printf("file unable to open");
			}
			printf("file 2 closed");
			}
			else if(i % 2 == 1)
			{
				//odd intervals. open the respective file
                //for odd intervals read from file 2 and write to file 1
				file_flag = 1;
				tp_file_1 = fopen(temp_file_name_1, "w");
				tp_file_2 = fopen(temp_file_name_2, "r");
				if(tp_file_2 != NULL && tp_file_1 !=NULL)
				{
					for(j = 0; j < test_interval; j++)
					{
						fscanf(ip_file, "%f;%f;%f;%f;%f;%f;%f", &temp1, &temp2, &temp3, &temp4, &temp5, &temp6, &travel_time);
						fgets (mystring , 20000 , tp_file_2);

						nl = strrchr(mystring, '\r');
						if (nl) *nl = '\0';
						nl = strrchr(mystring, '\n');
						if (nl) *nl = '\0';

						//tt_temp = itoa(travel_time, tt_temp, 10);
						sprintf(tt_temp, "%f", travel_time);
						//printf("I = 1; Travel time - %f; string travel time - %s; %s", travel_time, tt_temp, mystring);
						fputs(mystring, tp_file_1);
						fputs("\t", tp_file_1);
						fputs(tt_temp, tp_file_1);
						fputs("\n", tp_file_1);
					}
				}
				fclose(tp_file_1);
				fclose(tp_file_2);
			}
			else if(i % 2 == 0)
			{
				//even intervals. open the respective file
                //for even intervals read from file 1 and write to file 2
				file_flag = 0;
				tp_file_1 = fopen(temp_file_name_1, "r");
				tp_file_2 = fopen(temp_file_name_2, "w");
				if(tp_file_2 != NULL && tp_file_1 !=NULL)
				{
					for(j = 1; j <= test_interval; j++)
					{
						fscanf(ip_file, "%f;%f;%f;%f;%f;%f;%f", &temp1, &temp2, &temp3, &temp4, &temp5, &temp6, &travel_time);
						fgets (mystring , 20000 , tp_file_1);

						nl = strrchr(mystring, '\r');
						if (nl) *nl = '\0';
						nl = strrchr(mystring, '\n');
						if (nl) *nl = '\0';


						sprintf(tt_temp, "%f", travel_time);
						//printf("I is mult of 2; Travel time - %f; string travel time - %s; %s", travel_time, tt_temp, mystring);

						fputs(mystring, tp_file_2);
						fputs("\t", tp_file_2);
						fputs(tt_temp, tp_file_2);
						fputs("\n", tp_file_2);

						/*
						if(j % i == 0)
						{
							fscanf(ip_file, "%f;%f;%f;%f;%f;%f;%f", &temp1, &temp2, &temp3, &temp4, &temp5, &temp6, &travel_time);
							//tt_temp = itoa(travel_time, tt_temp, 10);
							sprintf(tt_temp, "%f", travel_time);
							printf("I is mult of 2; Travel time - %f; string travel time - %s\n", travel_time, tt_temp);
							fputs(tt_temp, tp_file_2);
							fputs("\n", tp_file_2);
						}	
						*/
					}
				}
				fclose(tp_file_1);
				fclose(tp_file_2);
			}
		}
	}
	fclose(ip_file);

    //based on the file_flag rename and delete the required the files
	if (file_flag)
	{
	delete_file(temp_file_name_2);
	rename_file(temp_file_name_1, output_file_name);
	}
	else
	{
	delete_file(temp_file_name_1);
	rename_file(temp_file_name_2, output_file_name);
	}


}
