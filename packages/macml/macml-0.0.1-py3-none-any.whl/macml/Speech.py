from datetime import datetime, timedelta
from typing import Callable, Union
import time

import AppKit
import AVFoundation
import Speech

from .utilities import _nsurl

voices = [x.replace("com.apple.speech.synthesis.voice.", "").replace(".premium", "").title() for x in AppKit.NSSpeechSynthesizer.availableVoices()] #: List of voice names available on the system

def speak(self, message: str, volume: float = 0.5, rate: int = 200, voice: Union[str, None] = None, save_file: Union[str, None] = None):
    # Get the selected voice by name
    if isinstance(voice, str):
        for available_voice in voices:
            if voice.lower() == available_voice.lower():
                voice = available_voice

    # Set up speech synthesis object
    synthesizer = AppKit.NSSpeechSynthesizer.alloc().initWithVoice_(voice)
    synthesizer.setVolume_(volume)
    synthesizer.setRate_(rate)

    # Start speaking
    if save_file is None:
        synthesizer.startSpeakingString_(message)
    else:
        path_url = _nsurl(save_file)
        synthesizer.startSpeakingString_toURL_(message, path_url)

    # Wait for speech to complete
    while synthesizer.isSpeaking():
        time.sleep(0.01)

class SpeechRecognizer:
    def __init__(self, rules: Union[None, dict[Callable[[str], bool], Callable[['SpeechRecognizer'], None]]] = None):
        default_rules = {
            lambda x: self.time_elapsed > timedelta(seconds = 10): lambda x: None,
        }
        self.rules = rules or default_rules
        self.full_transcription: str = "" #: The full spoken input, from the time listening begins until :func:`stop` is called
        self.last_spoken_query: str = "" #: The input since the last rule was passed
        self.start_time: datetime #: The time that the Speech Recognizer begins listening
        self.time_elapsed: timedelta #: The amount of time passed since the start time

    def on_detect(self, rule: Callable[[str], bool], action: Callable[['SpeechRecognizer'], None]):
        self.rules[rule] = action

    def listen(self):
        self.start_time = datetime.now()
        self.time_elapsed = None
        
        # Request microphone access if necessary
        Speech.SFSpeechRecognizer.requestAuthorization_(None)

        # Set up audio session
        self.audio_session = AVFoundation.AVAudioSession.sharedInstance()
        self.audio_session.setCategory_mode_options_error_(AVFoundation.AVAudioSessionCategoryRecord, AVFoundation.AVAudioSessionModeMeasurement, AVFoundation.AVAudioSessionCategoryOptionDuckOthers, None)
        self.audio_session.setActive_withOptions_error_(True, AVFoundation.AVAudioSessionSetActiveOptionNotifyOthersOnDeactivation, None)

        # Set up recognition request
        self.recognizer = Speech.SFSpeechRecognizer.alloc().init()
        self.recognition_request = Speech.SFSpeechAudioBufferRecognitionRequest.alloc().init()
        self.recognition_request.setShouldReportPartialResults_(True)

        # Set up audio engine
        self.audio_engine = AVFoundation.AVAudioEngine.alloc().init()
        self.input_node = self.audio_engine.inputNode()
        recording_format = self.input_node.outputFormatForBus_(0)
        self.input_node.installTapOnBus_bufferSize_format_block_(0, 1024, recording_format,
            lambda buffer, _when: self.recognition_request.appendAudioPCMBuffer_(buffer))
        self.audio_engine.prepare()
        self.audio_engine.startAndReturnError_(None)

        def detect_speech(transcription, error):
            if error is not None:
                print("Failed to detect speech. Error: ", error)
            else:
                self.last_spoken_query = transcription.bestTranscription().formattedString()[len(self.full_transcription):].strip()
                for rule in self.rules:
                    if rule(self.last_spoken_query):
                        self.rules[rule](self)
                        self.full_transcription = self.full_transcription + self.last_spoken_query

        recognition_task = self.recognizer.recognitionTaskWithRequest_resultHandler_(self.recognition_request, detect_speech)

        while self.time_elapsed is None or self.audio_engine.isRunning():
            self.time_elapsed = datetime.now() - self.start_time
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(datetime.now() + timedelta(seconds = 0.5))

    def stop(self):
        self.audio_engine.stop()