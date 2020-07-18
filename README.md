# Text-Extraction-from-Image
A Tkinter GUI for Tesseract implementation to extract text from image. Includes extraction of 12 languages for now.
Install Tesseract-OCR from the link: https://github.com/UB-Mannheim/tesseract/wiki.
Install tesseract by typing "pip install tesseract" in cmd.
Copy the path of Tesseract-OCR. "C:\Program Files\Tesseract-OCR" is preferable.
Set pytesseract path in the code. By default, "C:\Program Files\Tesseract-OCR\tessdata.exe" is set.
Download training data from "https://tesseract-ocr.github.io/tessdoc/Data-Files" and copy them to location:"C:\Program Files\Tesseract-OCR\tessdata
Include those languages in the python code if not present. 
Now your text extractor is ready. 
Works for inclined images and for both light and dark backgrounds. 
