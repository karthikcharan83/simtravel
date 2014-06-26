#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <malloc.h>
#include <string.h>
#include "flattening_link_attr_alt.h"

int main()
{

    int interval, number_intervals;
    char *linkAttList_fileName, *refLinkOrder, *linkFlatten_fileName;

    linkAttList_fileName = "/home/karthik/simtravel/malta/output_gui_LinkStats_0.dat";
    linkFlatten_fileName = "/home/karthik/simtravel/malta/input_HTDSP_tdcost_MAG_24hr_new.dat";
    refLinkOrder = "/home/karthik/simtravel/malta/input_HTDSP_links_order.csv";
    interval = 20522;
    number_intervals = 1440;

    flatten_link_attributes(interval, number_intervals, linkAttList_fileName, linkFlatten_fileName, refLinkOrder);
}

