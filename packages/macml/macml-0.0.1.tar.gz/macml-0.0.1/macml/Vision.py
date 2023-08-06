from typing import Union
import tempfile
import time

import Foundation
import Vision

from .utilities import _nsurl

class Image:
    """Wrapper around NSImage providing convenience methods.
    
    .. versionadded:: 0.0.1
    """
    def __init__(self, image_reference: Union[str, Foundation.NSImage]):
        # TODO: Add support for other types of image references, e.g. bytes
        if isinstance(image_reference, str):
            url = _nsurl(image_reference)
            self.image = Foundation.NSImage.alloc().initWithContentsOfURL_(url)
        elif isinstance(image_reference, Foundation.NSImage):
            self.image = image_reference.copy()

    @property
    def size(self) -> tuple[int, int]:
        """The width and height of the image in pixels.
        """
        return tuple(self.image.size())

    @size.setter
    def size(self, size: tuple[int, int]):
        self.image.setSize_(size)

    def show_in_preview(self):
        """Opens the image in Preview.
        
        .. versionadded:: 0.0.1
        """
        tmp_file = tempfile.NamedTemporaryFile()
        with open(tmp_file.name, 'wb') as f:
            f.write(self.image.TIFFRepresentation())

        config = Foundation.NSWorkspaceOpenConfiguration.alloc().init()
        config.setActivates_(True)

        img_url = _nsurl(tmp_file.name)
        preview_url = _nsurl("/System/Applications/Preview.app/")
        Foundation.NSWorkspace.sharedWorkspace().openURLs_withApplicationAtURL_configuration_completionHandler_([img_url], preview_url, config, None)
        time.sleep(1)

    # * Feature Detection
    def detect_rectangles(self):
        return FeatureDetector(self).detect_rectangles()

    def detect_faces(self):
        return FeatureDetector(self).detect_faces()

    # * Feature Extraction
    def extract_text(self):
        return FeatureExtractor(self).extract_text()

    def extract_rectangles(self):
        return FeatureExtractor(self).extract_rectangles()

class FeatureDetector:
    """Image feature detection manager.
    
    A FeatureDetector reports information about features within images, such as their location, rotation, and quality. Does not extract the features into their own images -- use :class:`FeatureExtractor` for that.

    :param image: The image or path to an image to detect features within
    :type image: Union[Image, str]

    .. versionadded:: 0.0.1
    """
    def __init__(self, image: Union[Image, str]):
        if isinstance(image, str):
            self.image = Image(image)
        elif isinstance(image, Image):
            self.image = image.image

    def detect_text(self):
        pass

    def detect_rectangles(self, minimum_confidence: float = 0.5, minimum_aspect_ratio: float = 0.2) -> list[dict]:
        """Detects rectangles of any orientation within the image.

        :param minimum_confidence: The minimum confidence level for a detected rectangle to be included in the results, defaults to 0.5
        :type minimum_confidence: float, optional
        :param minimum_aspect_ratio: The minimum aspect ratio for a detected rectangle to be included in the results, defaults to 0.2
        :type minimum_aspect_ratio: float, optional
        :return: A list of dictionaries describing the properties of each detected rectangle
        :rtype: list[dict]

        .. versionadded:: 0.0.1
        """
        detected_rects = []
        def request_rect_handler(request, error):
            results = request.results()
            detected_rects.extend([{
                "bottom_left": tuple(result.bottomLeft()),
                "bottom_right": tuple(result.bottomRight()),
                "top_right": tuple(result.topRight()),
                "top_left": tuple(result.topLeft()),
                "bounding_box": (*result.boundingBox().origin, *result.boundingBox().size),
                "confidence": result.confidence()
            } for result in results])
        
        request = Vision.VNDetectRectanglesRequest.alloc().initWithCompletionHandler_(request_rect_handler)
        request.setMaximumObservations_(16)
        request.setMinimumConfidence_(minimum_confidence)
        request.setMinimumAspectRatio_(minimum_aspect_ratio)

        request_handler = Vision.VNImageRequestHandler.alloc().initWithData_options_(self.image.TIFFRepresentation(), None)
        request_handler.performRequests_error_([request], None)
        return detected_rects

    def detect_faces(self) -> list[dict]:
        """Detects the bounding rectangles of faces within the image.

        :return: A list of dictionaries describing the pitch, roll, yaw, and capture quality of each detected face
        :rtype: list[dict]

        .. versionadded:: 0.0.1
        """
        detected_faces = []
        def request_face_handler(request, error):
            results = request.results()
            detected_faces.extend([{
                "pitch": result.pitch(),
                "roll": result.roll(),
                "yaw": result.yaw(),
                "quality": result.faceCaptureQuality()
            } for result in results])
        
        request = Vision.VNDetectFaceRectanglesRequest.alloc().initWithCompletionHandler_(request_face_handler)

        request_handler = Vision.VNImageRequestHandler.alloc().initWithData_options_(self.image.TIFFRepresentation(), None)
        request_handler.performRequests_error_([request], None)
        return detected_faces

    def detect_facial_features(self):
        pass

    def detect_body_parts(self):
        pass

    def detect_body_pose(self):
        pass

    def detect_hand_pose(self):
        pass

    def detect_animal(self):
        pass

    def detect_contours(self):
        pass

    def detect_barbodes(self):
        pass

    def detect_horizon(self):
        pass


class FeatureExtractor:
    def __init__(self, image: Union[Image, None] = None):
        self.image = image

    def extract_text(self):
        extracted_strings = []
        def request_text_handler(request, error):
            observations = request.results()
            extracted_strings.extend([o.topCandidates_(1)[0].string() for o in observations])
        
        request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(request_text_handler)

        request_handler = Vision.VNImageRequestHandler.alloc().initWithData_options_(self.image.image.TIFFRepresentation(), None)
        request_handler.performRequests_error_([request], None)
        return extracted_strings

    def extract_rectangles(self, minimum_confidence: float = 0.5, minimum_aspect_ratio: float = 0.2):
        rect_images = []
        rects = FeatureDetector(self.image).detect_rectangles()
        for rect in rects:
            box = Foundation.NSMakeRect(*rect["bounding_box"])

            new_image = Foundation.NSImage.alloc().initWithSize_((box.size[0] * self.image.size[0], box.size[1] * self.image.size[1]))

            bounds = Foundation.NSMakeRect(box.origin[0] * self.image.size[0], box.origin[1] * self.image.size[1], *new_image.size())
            
            new_image.lockFocus()
            self.image.image.drawInRect_fromRect_operation_fraction_(Foundation.NSMakeRect(0, 0, *new_image.size()), bounds, 1, 1.0)
            new_image.unlockFocus()
            rect_images.append(Image(new_image))
        return rect_images