# Whisper-voice-text-live
<p>This project is aimed at converting the speech to text which can be used for various applications. I have used OpenAi whisper model. Since the model doesnt have live transcription, i packeted the receiving the voice to 5s packets and process that for better live transcription</p>
<p>I processed this data which can be used to give direction commands like move forward, backward etc, which then is passed to velocity command topic in ros which is exectuted by the robot</p>
