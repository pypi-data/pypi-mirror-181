#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Originally part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2022 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

"""Audio capture and analysis using Pyo.

This is the legacy microphone library originally written by Jeremy R. Gray that
was originally found in `psychopy.microphone`. This library provides advanced,
but rarely used features. It has since been deprecated and replaced by the newer
Psychtoolbox based microphone library in `psychopy.sound.microphone`.

Some features may no longer work as the library has not been maintained for some
time.

"""

__version__ = '0.0.1'

from .microphone import (
    haveMic,
    FLAC_PATH,
    AudioCapture,
    AdvAudioCapture,
    getMarkerOnset,
    readWavFile,
    getDftBins,
    getDft,
    getRMSBins,
    getRMS,
    SoundFormatNotSupported,
    SoundFileError,
    MicrophoneError,
    Speech2Text,
    BatchSpeech2Text,
    flac2wav,
    wav2flac,
    switchOn,
    switchOff,
    _getFlacPath)
