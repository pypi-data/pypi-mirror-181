"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import os
import pathlib
import matplotlib
import pandas as pd
import tifffile
import numpy as np

from napari.utils.colormaps import colormap_utils as cu
from napari.layers.labels._labels_constants import Mode
from napari.layers import Layer

from qtpy import QtCore
from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QGridLayout

from scipy import ndimage
from skimage import io, measure
from skimage.filters import threshold_otsu as sk_threshold_otsu, gaussian, sobel
from skimage.segmentation import watershed
from skimage.measure import label
from skimage.morphology import local_minima
from skimage.feature import blob_dog, blob_log, blob_doh
from scipy import ndimage as ndi
from scipy.spatial.distance import cdist
from matplotlib import pyplot as plt 

if TYPE_CHECKING:
    import napari


class Preprocessing(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        # Create Mask for bud detection
        button_mask_detection = QPushButton("Create Mask (Detection)", self)
        button_mask_detection.clicked.connect(self._draw_mask_detection)

        button_run_masks = QPushButton("Run", self)
        button_run_masks.clicked.connect(self._run_masks)

        # Layout
        self.preprocessing_layout = QVBoxLayout()
        self.preprocessing_layout.setSpacing(15)
        self.preprocessing_layout.setContentsMargins(10, 10, 10, 10)
        self.preprocessing_layout.setAlignment(QtCore.Qt.AlignBottom)

        # Adding the widgets to the layout
        self.preprocessing_layout.addWidget(button_mask_detection)
        self.preprocessing_layout.addWidget(button_run_masks)  # , 1, 0)

        self.setLayout(self.preprocessing_layout)

        # Create tabs for widgets
        #dw1 = self.viewer.window.add_dock_widget(button_mask_detection)
        #dw2 = self.viewer.window.add_dock_widget(button_run_masks)
        #self.viewer.window._qt_window.tabifyDockWidget(dw1, dw2)
        #self.viewer.window.add_dock_widget(self._segment_seeded_watershed, area ='right', name = "Cells Segmentation")


    def _draw_mask_detection(self, button):
        """
        Add a shape layer to manually outline the mask (bud outline) used for distance map computation.   
        """
        LAYER_NAME = 'mask_detection'

        self.viewer.add_shapes(name=LAYER_NAME, shape_type='polygon',
                               face_color='darkorange', edge_color='darkorange', opacity=0.2)


    def _run_masks(self, button):
        """
        Crop the channels images with repect to the manually drawn bud mask. 
        Compute the distance map 
        Add new layers. 
        """
        # Create shape of the same size as the channel data
        data = self.viewer.layers[0].data
        mask_shape = np.shape(np.squeeze(data))
        #print("\nmask_shape: ", mask_shape)

        ########################################################
        # Mask for Segmentation and distance map 
        ########################################################

        # Convert Shape to Binary mask 
        mask_detection = self.viewer.layers['mask_detection'].to_masks(mask_shape=mask_shape)
        mask_detection = np.squeeze(mask_detection)
        bud_distancemap = ndimage.distance_transform_edt(mask_detection)
        
        # Crop the channels according to the mask
        ch1_cropped = np.zeros(np.shape(data))
        ch2_cropped = np.zeros(np.shape(data))
        ch3_cropped = np.zeros(np.shape(data))
        ch4_cropped = np.zeros(np.shape(data))

        ch1_cropped[mask_detection] = self.viewer.layers["ch1"].data[mask_detection]
        ch2_cropped[mask_detection] = self.viewer.layers["ch2"].data[mask_detection]
        ch3_cropped[mask_detection] = self.viewer.layers["ch3"].data[mask_detection]
        ch4_cropped[mask_detection] = self.viewer.layers["ch4"].data[mask_detection]

        # Add the cropped channel data and the distance map to the viewer
        self.viewer.add_image(ch1_cropped, colormap="red", visible=False)
        self.viewer.add_image(ch2_cropped, colormap="green", visible=False)
        self.viewer.add_image(ch3_cropped, colormap="blue", visible=False)
        self.viewer.add_image(ch4_cropped, colormap="gray", visible=True)
        self.viewer.add_image(bud_distancemap, visible=False)


class ManualCorrections(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        # Manual correction Widgets
        correction_button = QPushButton("Manual Corrections", self)
        correction_button.clicked.connect(self._manual_corrections)

        mergeLabels_button = QPushButton("Merge", self)
        mergeLabels_button.clicked.connect(self._merge_labels)

        splitLabels_button = QPushButton("Split", self)
        splitLabels_button.clicked.connect(self._split_labels)

        deleteLabels_button = QPushButton("Delete Labels", self)
        deleteLabels_button.clicked.connect(self._delete_labels)

        addLabels_button = QPushButton("Add Labels", self)
        addLabels_button.clicked.connect(self._add_labels)

        # Layout
        self.correction_layout = QVBoxLayout()
        self.correction_layout.setSpacing(15)
        self.correction_layout.setContentsMargins(10, 10, 10, 10)
        self.correction_layout.setAlignment(QtCore.Qt.AlignBottom)

        # Adding the widgets to the layout
        self.correction_layout.addWidget(correction_button)
        self.correction_layout.addWidget(mergeLabels_button)
        self.correction_layout.addWidget(splitLabels_button)
        self.correction_layout.addWidget(deleteLabels_button)
        self.correction_layout.addWidget(addLabels_button)
        self.setLayout(self.correction_layout)

    def _manual_corrections(self, button):
        """
        Create a new point layer named "points_manual_corrections"
        The points created in this layer are used for label merging and splitting in _merge_labels() _split_labels() respectively.
        """
        points_layer = self.viewer.add_points(data = [], name="points_manual_corrections")
        points_layer.mode = 'ADD'

    def _merge_labels(self, button):
        """
        Merge multiple labels corresponding to the points created in the "point_manual_corrections" layer.
        The minimum label is kept.
        """
        # Select the point and label layers
        points_layer = self.viewer.layers['points_manual_corrections']
        labels_layer = self.viewer.layers['segmentation_ch4_cropped'] 
      
        # Access the point and label layers's data
        points = points_layer.data
        labels = np.asarray(labels_layer.data)

        label_ids = [labels.item(tuple([int(j) for j in i])) for i in points]

        # Replace labels with minimum of the selected labels
        new_label_id = min(label_ids)
        for l in label_ids:
            if l != new_label_id:
                labels[labels == l] = new_label_id

        labels_layer.data = labels
        points_layer.data = []

    def _split_labels(self, button):
        """
        Split multiple labels corresponding to the points created in the "point_manual_corrections" layer.
        The minimum label is kept. Intensity layer is used to perform watershed splitting. 
        """

        # Select the the point, label and intensity layers
        points_layer = self.viewer.layers['points_manual_corrections']
        labels_layer = self.viewer.layers['segmentation_ch4_cropped']
        intensity_layer = self.viewer.layers['ch4_cropped']

        # Access the point, label and intensity layers's data
        labels = np.asarray(labels_layer.data)
        points = points_layer.data
        intensity = intensity_layer.data

        label_ids = [labels.item(tuple([int(j) for j in i])) for i in points]

        # Make a binary image first
        binary = np.zeros(labels.shape, dtype=bool)
        new_label_id = min(label_ids)
        for l in label_ids:
            binary[labels == l] = True

        # origin: https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_watershed.html
        mask = np.zeros(labels.shape, dtype=bool)
        for i in points:
            #mask[tuple(points)] = True
            mask[tuple([int(j) for j in i])] = True

        markers, _ = ndi.label(mask)

        # Apply watershed on image intensity rather than binary mask
        #new_labels = watershed(binary, markers, mask=binary)
        new_labels = watershed(intensity, markers, mask=binary)
        labels[binary] = new_labels[binary] + labels.max()

        # Update the labels layer and clear the point layer
        labels_layer.data = labels
        points_layer.data = []


    def _delete_labels(self, button):
        """
        Select the fill tool of the label layer with the background label
        """
        labels_layer = self.viewer.layers['segmentation_ch4_cropped']

        labels_layer.mode = Mode.FILL
        labels_layer.selected_label = 0
        labels_layer.preserve_labels = False

    def _add_labels(self, button):
        """
        Select the pick tool with a new label
        """
        labels_layer = self.viewer.layers['segmentation_ch4_cropped']

        labels_layer.mode = Mode.PAINT
        labels_layer.selected_label = np.max(labels_layer.data) + 1
        labels_layer.preserve_labels = True

        @labels_layer.mouse_wheel_callbacks.append
        def update_brush_size(layer, event): 
            MAX_BRUSH_SIZE = 40

            if layer.mode == Mode.PAINT: 
                delta = int(event.delta[1])
                if abs(delta) >= 1:
                    for i in range(abs(delta)):
                        if delta < 0:
                            #self.dims._increment_dims_left()
                            if (layer.brush_size > 0): 
                                layer.brush_size -= 1
                        else:
                            #self.dims._increment_dims_right()
                            if (layer.brush_size < MAX_BRUSH_SIZE): 
                                layer.brush_size += 1

               

@magic_factory(call_button="Load", filename={"label": "Select a .tiff file:"})
def load_data(filename=pathlib.Path()) -> "napari.types.LayerDataTuple":
    """
    Widget to select a multichannel .tiff image to be loaded. 
    Splits the images in the different channels and add them to the viewer. 

    Returns
    -------
    list[napari.types.LayerDataTuple]
        list of tuple of (data, meta, 'labels') for consumption by napari
    """

    # Image Loading and reshaping
    im_ori = io.imread(filename)
    im_ori = np.transpose(im_ori, (2, 0, 1))
    im_ori = np.reshape(
        im_ori, (1, 4, np.shape(im_ori)[1], np.shape(im_ori)[2]))
    #print("np.shape(im_ori): ", np.shape(im_ori))

    # Image Splitting
    list_channels = [im_ori[0, 0, :, :], im_ori[0, 1, :, :],
                     im_ori[0, 2, :, :], im_ori[0, 3, :, :]]
    list_layer_type = 'image'
    list_metadata = [{'name': "ch1", 'colormap': "red"},
                     {'name': "ch2", 'colormap': "green"},
                     {'name': "ch3", 'colormap': "blue"},
                     {'name': "ch4", 'colormap': "gray"}]

    # Return a list of LayerDataTuple
    layer_list = []
    for idx in range(len(list_channels)):
        layer_list.append((list_channels[idx], list_metadata[idx], 'image'))

    return layer_list


@magic_factory(call_button="Segment")
def segmentation(viewer: 'napari.viewer.Viewer', layer: Layer, spot_sigma: float = 15, outline_sigma: float = 3) -> "napari.types.LayerDataTuple":
    """
    Segment cells in images with fluorescently marked membranes.
    The two sigma parameters allow tuning the segmentation result. The first sigma controls how close detected cells
    can be (spot_sigma) and the second controls how precise segmented objects are outlined (outline_sigma). Under the
    hood, this filter applies two Gaussian blurs, local minima detection and a seeded watershed.
    See also
    --------
    .. [1] https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_watershed.html
    """
    LAYER_NAME = "segmentation_" + str(layer.name)

    image = layer.data 
    image = np.asarray(image)

    # ------------------------------------------
    #            SEEDS DETECTION 
    # ------------------------------------------
    spot_blurred = gaussian(image, sigma=spot_sigma)
    spots = label(local_minima(spot_blurred))

    #print("\n------------------------------")
    #print("\nlocal minima: ", local_minima(spot_blurred))
    #print("\nspots: ", spots)
    #print("\n np.unique(spots): ", np.unique(spots) )
    #print("-------------------------------\n")

    spots = np.subtract(spots, np.ones(np.shape(spots)))
    spots[spots==-1] = 0
    spots = spots.astype('int')
    #print("\n np.unique(spots): ", np.unique(spots) )
    seeds_points = label_to_point(spots)
   
    # Remove the seeds by setting their value to zero 
    #df_distance_seeds.drop(df_distance_seeds[df_distance_seeds['keep'] == 0].index, inplace = True)
    
    # CHECK SEEDS
    currated_seeds = seeds_auto_check(seeds = spots)
    currated_seeds_points = label_to_point(currated_seeds)
    #print("np.unique(currated_seed): ", np.unique(currated_seeds))
    #print("\n")

  
    # ---------------------------------------
    #               WATERSHED 
    # ---------------------------------------
    if outline_sigma == spot_sigma:
        outline_blurred = spot_blurred
    else:
        outline_blurred = gaussian(image, sigma=outline_sigma)

    labels = watershed(outline_blurred, spots)
    labels_currated = watershed(outline_blurred, currated_seeds)

    print("watershed segmentation labels: ", labels)

    # Set background label to 0
    labels_cst = np.ones(np.shape(labels))
    labels = np.subtract(labels, labels_cst)
    labels = labels.astype('int')

    labels_currated = np.subtract(labels_currated, labels_cst)
    labels_currated = labels_currated.astype('int')

    # CHECK SEGMENTATION 
    labels_checked, points_to_merge_1, points_to_merge_2  = labels_auto_check(labels, image, THR_AREA=100) 
    labels_checked = label(labels_checked)
    labels_checked = np.subtract(labels_checked, np.ones(np.shape(labels_checked)))
    labels_checked = labels_checked.astype('int')

    #spots = np.subtract(spots, labels_cst)
    #spots = spots.astype('int')
    
    #print("watershed segmentation labels: ", labels)
    
    #return labels
    #labels_layer = (labels, {'name': LAYER_NAME}, 'labels')
    #return labels_layer

    # Return a list of LayerDataTuple
    layer_list = [#(spot_blurred, {'name': 'spot_blurred'}, 'image'),
                  #(local_minima(spot_blurred), {'name': 'local_min_spot_blurred'}, 'image'),
                  #(outline_blurred, {'name': 'outline_blurred'}, 'image'), 
                  #(spots, {'name': 'spots'}, 'labels'),
                  #(currated_seeds, {'name': 'spots_currated'}, 'labels'),
                  #(seeds_points, {'name': 'seeds_points'}, 'points'),
                  (currated_seeds_points, {'name': 'seeds_points'}, 'points'),
                  #(points_to_merge_1, {'name': 'points_to_merge', 'face_color': 'red'}, 'points'),
                  #(points_to_merge_2, {'name': 'points_to_merge_2', 'face_color': 'green'}, 'points'),
                  #(labels, {'name': LAYER_NAME}, 'labels'),
                  #(labels_checked, {'name': LAYER_NAME + "_shape"}, 'shapes'),
                  (labels_checked, {'name': LAYER_NAME}, 'labels')]
                  #(labels_currated, {'name': 'labels_currated'}, 'labels')]
    
    #for idx in range(len(list_channels)):
    #    layer_list.append((list_channels[idx], list_metadata[idx], 'image'))

    # create mpl figure with subplots
    #mpl_fig = plt.figure()
    #ax = mpl_fig.add_subplot(111)
    #(line,) = ax.plot(layer.data[123])  # linescan through the middle of the image

    # add the figure to the viewer as a FigureCanvas widget
    #viewer.window.add_dock_widget(FigureCanvas(mpl_fig))

    return layer_list


def seeds_auto_check(seeds, display_check=False):
    """
    Remove seeds that are too close to each others 
    Compute the distance between closest seeeds 
    Compute outliers 
    Remove one of the twoo seeds that are too close 
    """
    # Get distance between detected seeds
    distance_btwn_spots = feature_dist(seeds)
    
    #print("\ndistance_btwn_spots: ", distance_btwn_spots)
    #print("np.shape(distance_btwn_spots): ", np.shape(distance_btwn_spots))

    # Get minimum distance between detected seeds 
    distance_btwn_spots_min = []

    dict_distance_seeds = []
    for idx in range(len(distance_btwn_spots)): 
        dist_array = distance_btwn_spots[idx]
        idx_min = np.argmin(dist_array[np.nonzero(dist_array)])
        
        if idx <= idx_min: 
            idx_min = idx_min + 1 

        dist_min = dist_array[idx_min]

        #if dist_min == 0.0: 
        #    print("\ndist_array: ", dist_array)

        dict_distance_seeds.append({"seed": idx,  "closest_seed": idx_min, "dist": dist_min})

        #print("Closet to spot #", idx, ": spot #", idx_min, ' distance: ', dist_min)
        distance_btwn_spots_min.append(dist_min)

    df_distance_seeds = pd.DataFrame(dict_distance_seeds)
    #print("\n")
    #print(df_distance_seeds)

    # Threshold according to lower bound outliers 
    # Find outliers 
    # 1st, 3rd quartile and iqr 
    q1 = np.quantile(distance_btwn_spots_min, 0.25)
    q3 = np.quantile(distance_btwn_spots_min, 0.75)
    iqr = q3-q1
    upper_bound = q3+(1.5*iqr)
    lower_bound = q1-(1.5*iqr)

    for index, row in df_distance_seeds.iterrows():
        if row['dist'] < lower_bound:
            idx_keep = max(row['seed'], row['closest_seed'])
            idx_del  = min(row['seed'], row['closest_seed'])
        
            df_distance_seeds.loc[int(idx_keep), 'keep'] = 1
            df_distance_seeds.loc[int(idx_del), 'keep'] = 0
        else: 
            df_distance_seeds.loc[int(row['seed']), 'keep'] = 1

    #print("\n")
    #print(df_distance_seeds)

    df2 = df_distance_seeds.loc[df_distance_seeds['keep'] == 0, 'seed']
    #print("\ndf2: ", df2)
    #print("df2.tolist(): ", df2.tolist() )
    seeds_to_remove = df2.tolist()

    #print("\n spots: ", seeds)
    #print("np.shape(spots): ", np.shape(seeds))
    #print("np.unique(spots): ", np.unique(seeds))


    #print("\n df_distance_seeds['keep'] == 0] ", df_distance_seeds['keep'] == 0)
    currated_seeds = seeds
    currated_seeds[seeds == [df_distance_seeds['keep'] == 0]] = 0

    for seed in seeds_to_remove:
        #print("\n seed +1: ", seed + 1)
        #print("np.unique(currated_seeds): ", np.unique(currated_seeds))
        currated_seeds[currated_seeds == seed+1] = 0
        
    if display_check == True: 
        plt.figure()
        plt.subplot(121)
        plt.plot(distance_btwn_spots_min, '-o')
        plt.plot([0, len(distance_btwn_spots_min)], [np.mean(distance_btwn_spots_min), np.mean(distance_btwn_spots_min)], '-')
        plt.plot([0, len(distance_btwn_spots_min)], [upper_bound, upper_bound], '--', color='lightgrey')
        plt.plot([0, len(distance_btwn_spots_min)], [lower_bound, lower_bound], '--', color='lightgrey')
        for seed in seeds_to_remove:
            plt.plot(seed, distance_btwn_spots_min[seed], 'ro')
        plt.xlabel("Detected seed")
        plt.ylabel("Closest seed")

        plt.subplot(122)
        bplot = plt.boxplot(distance_btwn_spots_min)
        outliers = bplot["fliers"][0].get_xdata()
        #print("\noutliers: ", outliers)
        plt.show()

    return currated_seeds


def labels_auto_check(labels, image, THR_AREA, display_check = False):
    """
    
    """
     
    #print("\n----------------------")
    #print("labels_auto_check: ")
    #print("-----------------------\n")


    df_cells = pd.DataFrame(
        measure.regionprops_table(
            labels,
            intensity_image=image,
            properties=['label', 'centroid', 'area', 'orientation', 'axis_minor_length'])
    ).set_index('label')

    areas = df_cells['area'].tolist()
    areas.remove(max(areas))

    # Create a first list of points at the position of the label to be removed 
    list_p1_x = df_cells.loc[df_cells['area'] < THR_AREA, 'centroid-0']
    list_p1_y = df_cells.loc[df_cells['area'] < THR_AREA, 'centroid-1']
    list_p1 = np.column_stack((list_p1_x.tolist(), list_p1_y.tolist()))
    list_p1 = list_p1.astype(int)
    #print("points 1: ", list_p1) 

    list_p1_orientation = df_cells.loc[df_cells['area'] < THR_AREA, 'orientation']
    list_p1_minlength =  df_cells.loc[df_cells['area'] < THR_AREA, 'axis_minor_length']
  
    # Create a second point at the position of the adjacent label 
    #x1 = list_p1_x + np.sin(list_p1_orientation) * 0.5 * (list_p1_minlength + 1)
    #y1 = list_p1_y - np.cos(list_p1_orientation) * 0.5 * (list_p1_minlength + 1)
    list_p2_x = list_p1_x + list_p1_minlength + 1
    list_p2_y = list_p1_y + list_p1_minlength + 1
    list_p2 = np.column_stack((list_p2_x.tolist(), list_p2_y.tolist()))
    list_p2 = list_p2.astype(int)
    #print("points 2: ", list_p2) 

    # Merge labels 
    checked_labels = labels

    #for points_pair in np.column_stack((list_p1, list_p2)):
    for idx in range(len(list_p1)):
        points_pair = [list_p1[idx], list_p2[idx]]
        #print("points_pair: ", points_pair)
        label_ids = [labels.item(tuple([int(j) for j in i])) for i in points_pair]

        # Replace labels with minimum of the selected labels
        new_label_id = min(label_ids)
        for l in label_ids:
            if l != new_label_id:
                checked_labels[labels == l] = new_label_id

    #labels_layer.data = labels
    #checked_labels = labels

    #print("\n--------------------")
    #print("df_cells['area'].tolist(): ", df_cells['area'].tolist())

    if display_check == True: 
        plt.figure()
        plt.subplot(121)
        plt.plot(areas, '-o')
        plt.plot([0, len(areas)], [THR_AREA, THR_AREA], '--', color='lightgrey')
        for idx in range(len(areas)):
            if areas[idx] < THR_AREA: 
                plt.plot(idx, areas[idx], 'ro')
        plt.xlabel("Cells")
        plt.ylabel("area")
        plt.show()

        plt.subplot(122)
        plt.boxplot(areas)
        plt.xlabel("Cells")
        plt.ylabel("area [pixels]")
        plt.show()

    return checked_labels, list_p1, list_p2
    #return points

def label_to_point(label_data):
    """
    Convert a label data to points 
    """
    label_values = np.unique(label_data)

    points = np.argwhere(label_data > 0)
    #print("\n------------------------")
    #print("points: \n ", points)
    #print("------------------------")
    
    #for label in label_values:
    #    if label > 0: 
    #        x, y = np.where(label_data == label)

    return points



#def detect_blobs(image: "napari.types.ImageData", max_sigma: float = 20, threshold: float = 0.01) -> "napari.types.LayerDataTuple":
@magic_factory(call_button="Detect blobs")
def detect_blobs(viewer: 'napari.viewer.Viewer', layer: Layer, max_sigma: float = 2, threshold: float = 300) -> "napari.types.LayerDataTuple":
    #print("\n---------------------------------------")
    #print("  BLOB DETECTION ")
    #print("----------------------------------------\n")

    #print("max_sigma: ", max_sigma)
    #print("threshold: ", threshold)
    
    # Hide all layers except the seleceted one and the created point layer
    for existing_layer in viewer.layers:
        existing_layer.visible = False

    layer.visible = True


    #print(layer)
    #print(layer.name)
    LAYER_NAME = 'blobs_' + str(layer.name)
    #print("LAYER_NAME: ", LAYER_NAME)

    image = layer.data
    #print("image: ", image)
    # https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.blob_log
    # Normalize the image between 0 and 1 before detection
    image_normalized = (image - np.min(image)) / \
        (np.max(image) - np.min(image))

    # Compute Laplacian of Gaussian (raddi in the 3rd column)
    #blobs_log = blob_log(image_normalized, max_sigma=max_sigma,
    #                     num_sigma=1, threshold=threshold)
    blobs_log = blob_log(image, max_sigma=max_sigma,
                         threshold=threshold)

    #blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

    data_layer = []
    for blob in blobs_log:
        data_layer.append(blob[0:2])
    data_layer = np.array(data_layer)

    #print("blobs_log[0,:]: ", blobs_log[0, :])
    #print("data_layer: ", np.shape(data_layer))
    #print("data_layer[0,:]: ", data_layer[0, :])

    # Adapt point color to the channel color    
    image_colormap = layer.colormap 
    image_color = image_colormap.name
    #print("\n---------------------------------")
    #print("image colormap: ", image_colormap)
    #print("image color: ", image_color)
    #print("---------------------------------\n")

    # Create a new point layer 
    #points_layer = (data_layer, {'name': LAYER_NAME, "face_color": image_color }, 'points')
    
    points_layer = (data_layer, {'name': LAYER_NAME}, 'points')

    """
    #histogram, bin_edges = np.histogram(image)#, bins=65535, range=(0, 1))
    
    plt.figure()
    plt.hist(image_normalized.flatten())#, bins=65280, range=(0.0, 1.0))
    #plt.plot(bin_edges[0:-1], histogram)  
    plt.xlabel("Intensities")
    plt.ylabel("Occurence")
    plt.show()
    """

    return points_layer


@magic_factory(call_button="Statistics", dir_path={"widget_type": 'FileEdit', "mode": 'd', "label": "Export folder location:"})
def disp_statitics(labels: "napari.types.LabelsData", image: "napari.types.ImageData", points_markers1: "napari.types.PointsData", points_markers2: "napari.types.PointsData", dir_path=pathlib.Path()) -> "napari.types.LayerDataTuple":

    # Number of Significant digits
    DECIMALS = 2


    labels = measure.label(labels)


    # Create a pandas DataFrame sumarizing the cells characteristics
    df_cells = pd.DataFrame(
        measure.regionprops_table(
            labels,
            intensity_image=image,
            properties=['label', 'centroid', 'area', 'perimeter', 'min_intensity', 'max_intensity', 'mean_intensity'])
    ).set_index('label')

    # Create a pandas DataFrame sumarizing the marker1 characteristics
    df_marker1 = pd.DataFrame(
        {'label': np.arange(1, len(points_markers1)+1)}).set_index('label')
    points_markers1_pos_x = []
    points_markers1_pos_y = []
    points_markers1_dm = []
    points_markers1_cellLabel = []
    #print("np.min(image): ", np.min(image))
    #print("np.max(image): ", np.max(image))

    # Create a pandas DataFrame sumarizing the marker2 characteristics
    df_marker2 = pd.DataFrame(
        {'label': np.arange(1, len(points_markers2)+1)}).set_index('label')
    points_markers2_pos_x = []
    points_markers2_pos_y = []
    points_markers2_dm = []
    points_markers2_cellLabel = []

    print(df_cells.head())

    nb_cells = len(np.unique(labels)) - 1
    #nb_cells = np.max(labels)
    #print("\nnp.unique(labels): ", np.unique(labels))
    #print("len(np.unique(labels)", len(np.unique(labels)))
    #print("np.max(labels)", np.max(labels))

    

    cells_markers1 = np.zeros(nb_cells)
    cells_markers2 = np.zeros(nb_cells)

    # Get the number of detected markers per cells
    for point in points_markers1:
        #print("point: ", point)
        label = labels[int(point[0]), int(point[1])]
        #print("label: ", label)
        cells_markers1[label-1] += 1
        points_markers1_pos_x.append(point[0])
        points_markers1_pos_y.append(point[1])

        distance_map = image[int(point[0]), int(point[1])]
        points_markers1_dm.append(distance_map)
        points_markers1_cellLabel.append(label)

    for point in points_markers2:
        #print("point: ", point)
        label = labels[int(point[0]), int(point[1])]
        #print("label: ", label)
        cells_markers2[label-1] += 1
        points_markers2_pos_x.append(point[0])
        points_markers2_pos_y.append(point[1])
        distance_map = image[int(point[0]), int(point[1])]
        #distance_map = image[int(point[1]), int(point[0])]
        points_markers2_dm.append(distance_map)
        points_markers2_cellLabel.append(label)

    df_cells["markers_1"] = cells_markers1
    df_cells["markers_2"] = cells_markers2

    markers1_total_nb = np.sum(cells_markers1)
    markers2_total_nb = np.sum(cells_markers2)

    markers1_max_nb = np.max(cells_markers1)
    markers2_max_nb = np.max(cells_markers2)

    # Normalize the number of markers per cells 
    df_cells["markers_1_norm"] = np.divide(cells_markers1, markers1_max_nb) 
    df_cells["markers_2_norm"] = np.divide(cells_markers2, markers2_max_nb) 
   
    df_marker1["pos_x"] = points_markers1_pos_x
    df_marker1["pos_y"] = points_markers1_pos_y
    df_marker1["distanceMap"] = points_markers1_dm
    df_marker1["distanceMap_perc"] = df_marker1["distanceMap"]/np.max(image)
    df_marker1["cell_label"] = points_markers1_cellLabel

    df_marker2["pos_x"] = points_markers2_pos_x
    df_marker2["pos_y"] = points_markers2_pos_y
    df_marker2["distanceMap"] = points_markers2_dm
    df_marker1["distanceMap_perc"] = df_marker2["distanceMap"]/np.max(image)

    #print(df_cells.head())
    #print(df_marker1.head())

    
    # TODO: Custom colormap according to the markers presence
    #norm = matplotlib.colors.Normalize(vmin=0, vmax=1000)


    cmap = matplotlib.cm.get_cmap('viridis')
    #cmap_min = matplotlib.cm.viridis(norm(0),bytes=True) 
    #cmap_max = matplotlib.cm.viridis(norm(1000),bytes=True)

    cmap_min = cmap(0)
    cmap_mean = cmap(0.5)
    cmap_max = cmap(0.99)
    #print(rgba) 

    #colors = ["black", "green", "yellow", "red"]
    colors = ["black", cmap_min, cmap_max, cmap_mean]

    color_dict = {}
    ratio_dict = {}

    for id_cell in range(1, nb_cells+1):

        # For each cell get the number of detected markers 1 and 2
        nb_markers_1 = int(df_cells.loc[id_cell, ['markers_1']])
        nb_markers_2 = int(df_cells.loc[id_cell, ['markers_2']])
        
        # Create the colormap according to the presence of the markers
        if nb_markers_1 == 0 and nb_markers_2 == 0:
            # Black if the cell doesn't have any markers
            color_dict[id_cell] = colors[0]
            ratio_dict[id_cell] = np.NaN 
        elif nb_markers_1 > 0 and nb_markers_2 == 0:
            # Green if the cell have only type 1 markers
            color_dict[id_cell] = colors[1]
            ratio_dict[id_cell] = 0 
        elif nb_markers_1 == 0 and nb_markers_2 > 0:
            # Yellow if the cell have only type 2 markers
            color_dict[id_cell] = colors[2]
            ratio_dict[id_cell] = 1 
        elif nb_markers_1 > 0 and nb_markers_2 > 0:
            # Red if the cell have type 1 and type 2 markers
            #color_dict[id_cell] = colors[3]
            ratio_dict[id_cell] = np.divide(df_cells.loc[id_cell, ["markers_1_norm"]], 
                                            df_cells.loc[id_cell, ["markers_2_norm"]])

            #color_dict[id_cell] = cmap(ratio_marker_norm)
           
    #print('color_dict: ', color_dict)
    #print('ratio_dict: ', ratio_dict)

    
    ratio = list(ratio_dict.values())

    #df_cells["markers_ratio"] = np.divide(df_cells["markers_1_norm"], df_cells["markers_2_norm"])
    df_cells["markers_ratio"] = ratio

    """
    df_cells["markers_ratio_norm"] = np.divide(df_cells["markers_ratio"], np.max(df_cells["markers_ratio"])) 

    for id_cell in range(1, nb_cells+1):
        # For each cell get the number of detected markers 1 and 2
        nb_markers_1 = int(df_cells.loc[id_cell, ['markers_1']])
        nb_markers_2 = int(df_cells.loc[id_cell, ['markers_2']])
        ratio_marker_norm  = df_cells.loc[id_cell, ['markers_ratio_norm']]
        if nb_markers_1 > 0 and nb_markers_2 > 0:
            color_dict[id_cell] = cmap(ratio_marker_norm)

   
    min_ratio = min([i for i in ratio if i > 0])
    max_ratio = max([i for i in ratio if i > 0])
    """
    #df_cells["markers_ratio"] = np.divide(np.subtract(ratio, min_ratio), 
    #                                      np.subtract(max_ratio, min_ratio))

    df_cells["distanceMap_min"] = df_cells["min_intensity"]/np.max(image)
    df_cells["distanceMap_max"] = df_cells["max_intensity"]/np.max(image)
    df_cells["distanceMap_mean"] = df_cells["mean_intensity"]/np.max(image)
    #df_cells["color_map"] = color_dict.values()

    # TODO: add distancemap of the points per cells

    #print(df_cells.head())
    # Save as csv files
    #df_cells.to_csv(os.path.join(dir_path, 'cells.csv') )

    # Round all DataFrame values to a given decimal
    df_cells = df_cells.round(DECIMALS)
    df_marker1 = df_marker1.round(DECIMALS)
    df_marker2 = df_marker2.round(DECIMALS)

    # Save as excel file
    with pd.ExcelWriter(os.path.join(dir_path, "statistics.xlsx"), engine='xlsxwriter') as writer:
        df_cells.to_excel(writer, sheet_name="Cells", startrow=1, header=False)
        df_marker1.to_excel(writer, sheet_name="Marker1",
                            startrow=1, header=False)
        df_marker2.to_excel(writer, sheet_name="Marker2",
                            startrow=1, header=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book

        for sheet_name in writer.sheets:
            #print("\n-----------------------------------")
            #print("Export statistics as .xml file")
            #print("------------------------------------\n")

            #print("\nsheet_name: ", sheet_name)

            worksheet = writer.sheets[sheet_name]

            if sheet_name == "Cells":
                df = df_cells
            elif sheet_name == "Marker1":
                df = df_marker1
            elif sheet_name == "Marker2":
                df = df_marker2

            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape

            # Create a list of column headers, to use in add_table().
            #column_settings = [{'header': column} for column in df.columns]
            xcel_label = {'header': 'labels'}
            column_settings = [{'header': column} for column in df.columns]
            #print("column settings: ", column_settings)
            column_settings.insert(0, xcel_label)
            #print("column settings: ", column_settings)

            # Add the Excel table structure. Pandas will add the data.
            worksheet.add_table(0, 0, max_row, max_col, {
                                'columns': column_settings})

            # Make the columns wider for clarity.
            worksheet.set_column(0, max_col, 15)

            # Close the Pandas Excel writer and output the Excel file.
        writer.save()


    # Create a new label layer
    data_layer = np.array(labels)

    #print("\ndata_layer: ", data_layer)

    
    """
    data_layer_2 = data_layer.astype(np.float32)
    for row in range(data_layer.shape[0]): 
        for col in range(data_layer.shape[1]): 
            if col%100 == 0: 
                #print('[row, col]: [', row, ' ' , col ,']')
                #print("data_layer_2[row, col]: ", data_layer_2[row, col])
                #print('ratio: ', ratio[int(data_layer[row,col])])
                data_layer_2[row, col] = ratio[int(data_layer[row,col])]
                #print("data_layer_2[row, col]: ", data_layer_2[row, col])
            else: 
                data_layer_2[row, col] = ratio[int(data_layer[row,col])]
    """

 



    #mapped_data = list(map(lambda x: ratio[int(x]))
    #print("data_layer_2: ", data_layer_2)

    #print("data_layer:", data_layer)
    labels_layer = (data_layer,  {'name': "Probes labels", 'color': color_dict}, 'labels')

    #image_layer = (data_layer_2,  {'name': "Probes labels", 'colormap': 'viridis'}, 'image')
    return labels_layer
    #return image_layer



#@magic_factory(call_button="Visualization")
#def visualization(viewer: 'napari.viewer.Viewer'):

@magic_factory(call_button="Visualization")
def visualization(viewer: 'napari.viewer.Viewer'):
    
    #labels_data = viewer.layers['segmentation_ch4_cropped'].data
    labels_data = viewer.layers['labels'].data
    image = labels_data


    #image = np.zeros(im_w, im_h)
    #image[x,y] = markers_ratio[labels[x,y]]
    viewer.add_image(image, colormap="viridis", visible=True)


# @magic_factory(call_button="Export", filename={"Folder": "Export folder location:"})
# def export_data(filename=pathlib.Path()):
@magic_factory(call_button="Export", dir_path={"widget_type": 'FileEdit', "mode": 'd', "label": "Export folder location:"})
def export_data(viewer: 'napari.viewer.Viewer', dir_path=pathlib.Path()):
    """
    Export the cropped channels, the segmentation, the detections and the extracted statistics.

    Save
    -------
    - .tiff file containing the bud cropped channels 
    - .cvs file containing the statistics
    """

    # Asert that a folder has been selected
    if dir_path == ".":
        print("Please select a folder:")
        return

    im_export = []
    im_cropped_export = []

    #layers = self.viewer.layers
    layers = viewer.layers

    #print("\nlayers: ", layers)
    nb_layers = len(layers)
    #print("\nnb_layers: ", nb_layers)

    # TODO: find correct condition to add only Image layers
    # Select the 4 channels and the distance map
    #selected_layers = [layers[0], layers[1], layers[2], layers[3], layers[7]]
    selected_layers = layers

    for layer in selected_layers:
        #print("layer: ", layer)
        #print("layer.data: ", layer.data)
        #print("np.shape(layer.data): ", np.shape(layer.data))
        try:
            print(layer.dtype)
            im_export.append(layer.data)
        except:
            pass

    im_export = np.array(im_export)
    #print("np.shape(im_export)", np.shape(im_export))

    tifffile.imwrite(os.path.join(dir_path, "im_with_dm.tif"),
                     im_export.astype('float32'),
                     shape=im_export.shape,
                     imagej=True)

    # Save statistic data as cvs


def feature_dist(input):
    """
    Takes a labeled array as returned by scipy.ndimage.label and 
    returns an intra-feature distance matrix.
    """
    I, J = np.nonzero(input)
    labels = input[I,J]
    coords = np.column_stack((I,J))

    sorter = np.argsort(labels)
    labels = labels[sorter]
    coords = coords[sorter]

    sq_dists = cdist(coords, coords, 'sqeuclidean')

    start_idx = np.flatnonzero(np.r_[1, np.diff(labels)])
    nonzero_vs_feat = np.minimum.reduceat(sq_dists, start_idx, axis=1)
    feat_vs_feat = np.minimum.reduceat(nonzero_vs_feat, start_idx, axis=0)

    return np.sqrt(feat_vs_feat)


