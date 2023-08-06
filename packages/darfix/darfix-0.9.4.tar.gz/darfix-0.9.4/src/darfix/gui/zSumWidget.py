# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "20/07/2021"


import numpy

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D

from darfix.gui.utils import ChooseDimensionDock


class ZSumWidget(qt.QMainWindow):
    """
    Widget to apply PCA to a set of images and plot the eigenvalues found.
    """

    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self._plot = Plot2D(parent=self)
        self._plot.setDefaultColormap(Colormap(name="viridis", normalization="linear"))
        self._chooseDimensionDock = ChooseDimensionDock(self)
        self._chooseDimensionDock.hide()
        self._chooseDimensionDock.widget.filterChanged.connect(self._filterStack)
        self._chooseDimensionDock.widget.stateDisabled.connect(self._wholeStack)
        layout = qt.QVBoxLayout()
        layout.addWidget(self._plot)
        layout.addWidget(self._chooseDimensionDock)
        widget = qt.QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setDataset(
        self, parent, dataset, indices=None, bg_indices=None, bg_dataset=None
    ):
        # Make sum of dataset data
        self._parent = parent
        self.dataset = dataset
        self.indices = indices
        if len(self.dataset.data.shape) > 3:
            self._chooseDimensionDock.show()
            self._chooseDimensionDock.widget.setDimensions(self.dataset.dims)
        self._plot.setGraphTitle(self.dataset.title)
        self._addImage(self.dataset.zsum(indices=indices))

    def _filterStack(self, dim=0, val=0):
        image = self.dataset.zsum(indices=self.indices, dimension=[dim, val])
        if image.shape[0]:
            self._addImage(image)
        else:
            self._plot.clear()

    def _wholeStack(self):
        self._addImage(self.dataset.zsum())

    def _addImage(self, image):
        if self.dataset.transformation is None:
            self._plot.addImage(image, xlabel="pixels", ylabel="pixels")
            return
        if self.dataset.transformation.rotate:
            image = numpy.rot90(image, 3)
        self._plot.addImage(
            image,
            origin=self.dataset.transformation.origin,
            scale=self.dataset.transformation.scale,
            xlabel=self.dataset.transformation.label,
            ylabel=self.dataset.transformation.label,
        )
