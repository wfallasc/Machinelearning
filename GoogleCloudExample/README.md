
### William Fallas. williamfallas@gmail.com

#### Spech and translation with  Google API

The following project shows how to extract audio from video and translate  the same from english to spanish


Main Steps

     -extract audio was format
    - Change stereo to mono
    - upload wav file to google bucket
    - Use the SpeechClient API, long_running_recognize method to get the english transcript
    - Use translate_v2 API to translate the transcript from english to spanish
    - Transform the spanish transcript to voice with  the texttospeech API 
    - Save the result in a mp3 file and play