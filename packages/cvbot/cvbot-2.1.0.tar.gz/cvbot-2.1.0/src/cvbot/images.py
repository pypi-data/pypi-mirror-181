import cv2 as cv
from cvbot._screen import crop as _crop


class Image:
    def __init__(self, img, name="snapshot"):
        self.img  = img
        self.name = name
        self.type = "grey" if len(img.shape) < 3 else "bgr"

    @property
    def size(self):
        """
        self -> tuple(int, int)
        Return current image width and height in a tuple
        """
        return self.img.shape[:2][::-1]

    def grey(self):
        """
        self -> npimage
        Convert current image to gray and return it as a numpy image/matrix
        """
        if self.type == "grey":
            return self.img
        elif self.type == "bgr":
            return cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        else:
            print("Conversion is not possible from type {} to {}".format(self.type, "grey"))

    def crop(self, region):
        """
        self, (int, int, int, int) -> Image 
        Crop part of current Image using 'region' (x, y, w, h)
        and return it as a new Image
        """
        img = _crop(self.img, region)
        return Image(img)

    def convert(self, tp):
        """
        self, str -> Image
        Convert current Image to a given type 'tp'
        """
        if tp == "grey" or tp == "gray":
            gimg = self.grey()
            if not (gimg is None):
                self.img = gimg
                self.type = "grey"

    def show(self, pos=None):
        """
        self, [Optional] tuple(x, y) -> None
        Display image in a window on screen
        """
        cv.namedWindow(self.name)
        if not (pos is None):
            x, y = pos
            cv.moveWindow(self.name, x, y)
        cv.imshow(self.name, self.img)
        cv.waitKey(0)
