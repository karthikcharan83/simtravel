import copy

from numpy import array, logical_and, histogram, zeros, amax, unique


from openamos.core.models.abstract_model import Model
from openamos.core.data_array import DataArray


class UniqueRecordsProcessing(Model):

    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification

        self.uniqueRecordsColName = self.specification.uniqueRecordsColName

    def create_col_numbers(self, colnamesDict):
        # print colnamesDict
        self.uniqueRecordsCol = colnamesDict[self.uniqueRecordsColName]

    def create_indices(self, data):
        uniqueCols = data.columns([self.uniqueRecordsColName]).data

        uniqueRecs, reverse_indices = unique(uniqueCols, return_inverse=True)

        binsIndices = array(range(reverse_indices.max() + 2))
        histIndices = histogram(reverse_indices, bins=binsIndices)

        indicesRowCount = histIndices[0]
        indicesRow = indicesRowCount.cumsum()

        self.indicesOfRecs = zeros((uniqueRecs.shape[0], 3))

        self.indicesOfRecs[:, 0] = uniqueRecs
        self.indicesOfRecs[1:, 1] = indicesRow[:-1]
        self.indicesOfRecs[:, 2] = indicesRow

    def resolve_consistency(self, data, seed):
        data.sort([self.uniqueRecordsColName])

        self.create_col_numbers(data._colnames)
        self.create_indices(data)

        # print data.data.astype(int)

        newData = []
        for uniqueId in self.indicesOfRecs:
            strtRow = uniqueId[1]
            endRow = uniqueId[2]

            strtRecNew = copy.deepcopy(data.data[strtRow, :])

            newData.append(list(strtRecNew))

        newData = array(newData)
        # print newData.astype(int)
        # print 'person count - %s and hhld count - %s' %(data.rows, self.indicesOfRecs.shape[0])
        #raw_input('unique records identification ... ')

        return DataArray(newData, data.varnames)
