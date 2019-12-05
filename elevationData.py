import gdal
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class elevation:

    def __init__(self,filename):
        data = gdal.Open(filename)
        band = data.GetRasterBand(1)
        no_data_val = band.GetNoDataValue()

        self.elevation_array = data.ReadAsArray().astype(np.float)
        if np.any(data == no_data_val):
            self.elevation_array[data == no_data_val] = np.nan

    def display(self,resolution = 500):
        fig = plt.figure(figsize = (12, 12))
        ax = fig.add_subplot(111)
        plt.contourf(self.elevation_array, cmap = "viridis",
                    levels = list(range(0, int(np.amax(map.elevation_array))+resolution, resolution)))
        plt.title("Yosemite")
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def get_elevation(self, xy):
        return self.elevation_array[xy[0]][xy[1]]

    def get_slope(self, xy1, xy2):
        rise = self.get_elevation(xy1)-self.get_elevation(xy2)
        run = dist = np.linalg.norm(np.array(xy1)-np.array(xy2))
        return rise/run

    def normalize(self):
        new_data_array = []
        temp_array = []
        OldMin = np.amin(self.elevation_array)
        OldMax = np.amax(self.elevation_array)
        NewMax = 255
        NewMin = 0

        for row in self.elevation_array:
            for val in row:
                new_val = int(np.round((((val - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin))
                temp_array.append(new_val)
            new_data_array.append(temp_array)
            temp_array = []

        return np.array(new_data_array)



map = elevation("map.tif")
print(map.elevation_array)
#map.display(500)
print(map.normalize())
