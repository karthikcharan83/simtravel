import shutil
import time
import csv
import os
from numpy import array, average


class SuccessiveAverageLinkAttributes(object):

    def __init__(self, edges=20522, timeIntervals=1440):
        self.edges = edges
        self.timeIntervals = timeIntervals
        pass

    def sort_recs(self, refOrderFile, linkListFile, linkAttrUnsortFile, outputSortedFile):
        f = csv.reader(open(refOrderFile, 'r'), delimiter="\t")
        # Assumes that the second and third columns in the file give the start
        # and end node

        pass

    def get_avg_link_attributes(self, sa_filePath, new_filePath, temp_filePath, iteration):
        ti = time.time()
        sa_linkAttr = self.load_file(sa_filePath)
        new_linkAttr = self.load_file(new_filePath)
        print 'Time taken to load - %.4f' % (time.time() - ti)
        ti = time.time()
        self.copy_to_temp(sa_filePath, temp_filePath)
        sa_new = self.calculate_average(
            sa_linkAttr, new_linkAttr, iteration, sa_filePath)
        print 'Time taken to calculate and write to the file - %.4f' % (time.time() - ti)

    def get_deviation_link_attributes(self, sa_filePath, new_filePath):
        ti = time.time()
        sa_linkAttr = self.load_file(sa_filePath, "\t")
        new_linkAttr = self.load_file(new_filePath)
        print 'Time taken to load - %.4f' % (time.time() - ti)
        ti = time.time()
        self.copy_to_temp(sa_filePath, temp_filePath)
        avgVal = self.calculate_deviation(sa_linkAttr, new_linkAttr)
        print 'Time taken to calculate and write to the file - %.4f' % (time.time() - ti)
        return avgVal

    def calculate_deviation(self, sa, new):
        meanAbsDiff = average(abs(new - sa))

        return meanAbsDiff

    def load_file(self, filePath, delimiterChar=" "):
        f = csv.reader(open(filePath, 'r'), delimiter=delimiterChar)

        arr = []
        for i in f:
            if delimiterChar == "\t":
                arr.append(i)
            elif delimiterChar == " ":
                arr.append(i)
        arr = array(arr, float)
        print arr[:5, :].shape

        return arr

    def copy_to_temp(self, sa, temp):
        try:
            os.remove(temp)
        except Exception, e:
            print 'Error occurred while deleting file - %s: %s' % (temp, e)

        shutil.copyfile(sa, temp)

    def calculate_average(self, sa, new, iteration, filePath):
        new_sa = 1. / iteration * new + (iteration - 1.) / iteration * sa

        print new_sa[:5, :5]
        f = csv.writer(open(filePath, 'w'), delimiter=" ")

        for i in new_sa:
            f.writerow(list(i))

        return 1


if __name__ == "__main__":
    obj = SuccessiveAverageLinkAttributes()

    sa_filePath = "/simtravel/malta/input_HTDSP_tdcost_MAG_24hr.dat"
    new_filePath = "/simtravel/malta/input_HTDSP_tdcost_MAG_24hr_new.dat"
    temp_filePath = "/simtravel/malta/input_HTDSP_tdcost_MAG_24hr_temp.dat"

    obj.get_avg_link_attributes(sa_filePath, new_filePath, temp_filePath, 3)
