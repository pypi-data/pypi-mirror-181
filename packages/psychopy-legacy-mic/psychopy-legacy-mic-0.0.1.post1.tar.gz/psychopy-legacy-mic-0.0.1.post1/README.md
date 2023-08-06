# psychopy-legacy-mic

Extension that enables audio capture and analysis using Pyo.

This is the 'legacy' microphone library written by Jeremy R. Gray that was originally found in `psychopy.microphone`. 
This library provides advanced, but rarely used features for processing audio which users may still find useful. For
audio capture, this library has since been deprecated and replaced by the newer Psychtoolbox based microphone library in 
`psychopy.sound.microphone`.

Some features may no longer work as the library has not been maintained for some time. Depends on the `psychopy-pyo`
extension package being installed in the same environment. 
    
## Installing

Install this package with the following shell commands:: 
    
    pip install psychopy-pyo 
    pip install psychopy-legacy-mic

You may also use PsychoPy's builtin package manager to install this package.

## Usage

Once the package is installed, PsychoPy will automatically load it when started and make objects available within the
`psychopy.microphone` namespace. 
