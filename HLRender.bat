@set AnacondaPath="%HomeDrive%%HomePath%\Anaconda2"
@CALL %AnacondaPath%\Scripts\activate.bat %AnacondaPath%
START /min python HLRender.py
