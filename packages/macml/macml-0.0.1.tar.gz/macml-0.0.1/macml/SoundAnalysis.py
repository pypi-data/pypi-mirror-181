from typing import Callable, Union
from time import sleep

import AVFoundation
import Foundation
import SoundAnalysis
import CoreMedia

from .CoreML import Model
from .utilities import _nsurl

class _Analyzer:
    def __init__(self):
        pass
    
    @property
    def overlap_factor(self) -> float:
        """The percentage overlap between analysis windows.
        """
        return self._request.overlapFactor()

    @overlap_factor.setter
    def overlap_factor(self, overlap_factor: float):
        self._request.setOverlapFactor_(overlap_factor)

    @property
    def window_duration(self) -> int:
        """The duration of audio input classified for each prediction.
        """
        return CoreMedia.CMTimeMultiplyByRatio(self._request.windowDuration(), 1, 10000000).value

    @window_duration.setter
    def window_duration(self, window_duration: int):
        cmtime = CoreMedia.CMTimeMakeWithSeconds(window_duration, 10000000)
        self._request.setWindowDuration_(cmtime)

    @property
    def labels(self) -> list[str]:
        """The list of supported sound classification labels.
        """
        return list(self._request.knownClassifications())


class FileAnalyzer(_Analyzer):
    """A sound classifier for audio files with the ability to utilize custom classifier models.

    :param file_path: The path to the audio file to analyze
    :type file_path: str
    :param model: The custom model to use for classification, defaults to None
    :type model: Union[Model, None], optional

    .. versionadded:: 0.0.1
    """
    def __init__(self, file_path: str, model: Union[Model, None] = None):
        super().__init__()
        self.file_url = _nsurl(file_path)
        self.model = model

        self._analyzer = SoundAnalysis.SNAudioFileAnalyzer.alloc().initWithURL_error_(self.file_url, None)[0]

        if self.model is None:
            self._sound_request = SoundAnalysis.SNClassifySoundRequest.alloc().initWithClassifierIdentifier_error_(SoundAnalysis.SNClassifierIdentifierVersion1, None)[0]
        else:
            self._sound_request = SoundAnalysis.SNClassifySoundRequest.alloc().initWithMLModel_error_(self.model._MLModel, None)

    def analyze(self) -> list[dict[str, Union[int, list[tuple[str, float]]]]]:
        """Runs the audio file analyzer.

        :return: A dictionary containing the start time, duration, and classification confidence measures
        :rtype: list[dict[str, Union[int, list[tuple[str, float]]]]]

        .. versionadded:: 0.0.1
        """
        results = []
        class ResultsObserver(Foundation.NSObject):
            def request_didProduceResult_(oself, request, result):
                results.append({
                    "start_time": CoreMedia.CMTimeMultiplyByRatio(result.timeRange()[0], 1, 10000000).value,
                    "duration": CoreMedia.CMTimeMultiplyByRatio(result.timeRange()[1], 1, 10000000).value,
                    "classifications": [(classification.identifier(), classification.confidence()) for classification in result.classifications()]
                })

            def request_didFailWithError_(self, request, error):
                if error is not None:
                    raise Exception(error)

        results_observer = ResultsObserver.alloc().init().retain()
        self._analyzer.addRequest_withObserver_error_(self._sound_request, results_observer, None)
        self._analyzer.analyze()
        return results


class StreamAnalyzer(_Analyzer):
    """A sound classifier for realtime audio from the device's microphone.

    .. versionadded:: 0.0.1
    """
    def __init__(self):
        super().__init__()
        self._audio_engine = AVFoundation.AVAudioEngine.alloc().init()
        self._input_format = self._audio_engine.inputNode().inputFormatForBus_(0)
        self._analyzer = SoundAnalysis.SNAudioStreamAnalyzer.alloc().initWithFormat_(self._input_format)
        self._request = SoundAnalysis.SNClassifySoundRequest.alloc().initWithClassifierIdentifier_error_(SoundAnalysis.SNClassifierIdentifierVersion1, None)[0]
        self.last_result = None #: The most recently observed result

    def analyze(self, duration: float = -1.0, realtime_callback: Union[Callable[['StreamAnalyzer'], None], None] = None) -> list[dict[str, Union[int, list[tuple[str, float]]]]]:
        """Runs the audio stream analyzer for the specified duration.

        :param duration: The duration of the audio analysis session, in seconds, or -1.0 for infinite duration, defaults to -1.0
        :type duration: float, optional
        :param realtime_callback: A method to run upon each update in the analysis observer, defaults to None
        :type realtime_callback: Union[Callable[['StreamAnalyzer'], None], None], optional
        :return: A dictionary containing the start time, duration, and classification confidence measures
        :rtype: list[dict[str, Union[int, list[tuple[str, float]]]]]

        .. versionadded:: 0.0.1
        """
        self._audio_engine.startAndReturnError_(None)

        results = []
        class ResultsObserver(Foundation.NSObject):
            def request_didProduceResult_(oself, request, result):
                self.last_result = {
                    "start_time": CoreMedia.CMTimeMultiplyByRatio(result.timeRange()[0], 1, 10000000).value,
                    "duration": CoreMedia.CMTimeMultiplyByRatio(result.timeRange()[1], 1, 10000000).value,
                    "classifications": [(classification.identifier(), classification.confidence()) for classification in result.classifications()]
                }
                results.append(self.last_result)

                if callable(realtime_callback):
                    realtime_callback(self)

            def request_didFailWithError_(self, request, error):
                if error is not None:
                    raise Exception(error)

        results_observer = ResultsObserver.alloc().init().retain()
        self._analyzer.addRequest_withObserver_error_(self._request, results_observer, None)

        def analyze_audio(buffer, time):
            self._analyzer.analyzeAudioBuffer_atAudioFramePosition_(buffer, time.sampleTime())

        self._audio_engine.inputNode().installTapOnBus_bufferSize_format_block_(0, 8192, self._input_format, analyze_audio)
        
        sleep(duration)
        self._audio_engine.inputNode().removeTapOnBus_(0)
        self._audio_engine.disconnectNodeInput_(self._audio_engine.inputNode())
        self._audio_engine.stop()
        return results

    