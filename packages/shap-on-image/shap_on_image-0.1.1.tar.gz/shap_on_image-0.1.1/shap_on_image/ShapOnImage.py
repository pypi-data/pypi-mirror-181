from matplotlib import pyplot as plt
import os

class ShapOnImage:

    def __init__(self, image, dimensions, values, alpha=1, suptitle="", title=""):
        """
        args:
            image: str, path to image
            dimensions: list, dimensions of output image (e.g. [0, 300, 0, 220])
            values: dict, positions on figure (verify dimensions) and shap values for every feature
            alpha: float, coefficient to multiply every shap values to better visualisation
            suptitle: str, main title of output figure
            title: str, title of output figure
        """
        self.image = image                      
        self.dimensions = dimensions           
        self.values = values                    
        self.alpha = alpha
        if self.alpha != 1: 
            self.adjusted_values(values, self.alpha)
        self.suptitle = suptitle               
        self.title = title                     
    
    def check_init(self):
        """
        Print results of few tests on class initialisation
        """
        print('---Initialisation Check---')
        if os.path.exists(self.image):
            print('Path to Image: OK')
        else:
            print('Path to Image: ERROR')
        dim_error = False
        for _, value in self.values.items():
            x = value['x']
            y = value['y']
            max_x = self.dimensions[1]
            max_y = self.dimensions[3]
            if x > max_x or y > max_y:
                dim_error = True
        if dim_error:
            print('Positions according to Image dimensions: ERROR')
        else:
            print('Positions according to Image dimensions: OK')
    
    def adjusted_values(self, values, alpha):
        """
        Adjust shap values by multiplying with coefficient alpĥa
        args:
            values: dict, positions and shap values of every feature
            alpha: float, coefficient to multiply shap values by
        """
        self.values = values
        self.alpha = alpha
        for _, value in self.values.items():
            value['shap'] = value['shap'] * alpha

    
    def plot(self):
        """
        Plot the figure with image and shap values at specific positions
        """
        try:
            im = plt.imread(self.image)
        except: 
            print('Can\'t load image, verify path to image -> cf. Check_init()')
            return
        fig, ax = plt.subplots()
        im = ax.imshow(im, extent=self.dimensions)
        plt.axis('off')

        plt.suptitle(self.suptitle, weight="bold")
        plt.title(self.title)

        for _, value in self.values.items():
            shap = value['shap']
            x = value['x']
            y = value['y']
            color = ["cornflowerblue" if shap > 0 else "crimson"]
            plt.scatter(x, y, s=abs(shap), color=color)

        plt.show()

        self.fig = fig
    
    def save(self, save_path="saved_shap_ez_image.png"):
        """
        Save figure at specific path
        args:
            save_path: str, specific path (with filename) to save figure"""
        try:
            self.fig.savefig(save_path)
        except:
            print('Can\'t save figure, verify plot -> cf. Check_init()')