import PyPDF2, pyttsx3, os
from abc import ABC, ABCMeta, abstractmethod
from PIL import Image 
from pytesseract import pytesseract
        
class SpeechableInterface(ABC):
    @abstractmethod
    def get_texts(self, path:str ='test.ext') -> list:
        """
        Get text from the file
        """
        pass
    
class ReadableFile():
    def __init__(self, path:str) -> None:
        self.path = path
        self.read_file = self.get_instance()
        
    def get_instance(self) -> SpeechableInterface:
        """
            Returns the texts of whatever file is passed into it
            Only works for pdf, and image files for now.
            
            @todo: msword
        """
        try:
            file_extension = os.path.splitext(self.path)[1]
            
            if file_extension in ['.webp', '.png', 'jpeg', 'jpg']:
                return ImageFile(self.path)
                # return ImageFile(self.path).get_texts()
            
            elif file_extension in ['.pdf' ]:
                return PDFFIle(self.path)
                # return PDFFIle(self.path).get_texts()
            
        except:
            print("an error occurred while reading file")
            exit()
        
    def speak(self, texts: str):
        """
        Speak the text
        """
        speak=pyttsx3.init()
        
        for text in texts:
            speak.say(text)
            speak.runAndWait()
        speak.stop()    
    
    def read_out(self):
        file_text = self.read_file.get_texts()
        self.speak(file_text)
        
class PDFFIle(SpeechableInterface):
    def __init__(self, path:str ='test.pdf') -> list:
        self.path = path
        
    def get_texts(self) -> list:
        """
        Get text from the PDF file
        """
        path=open(self.path, 'rb')
        pdf_reader = PyPDF2.PdfReader(path)
        
        full_text = []
        for page in range(len(pdf_reader.pages)):
            text=pdf_reader.pages[page].extract_text()
            full_text.append(text)
        
        return full_text
    
class ImageFile(SpeechableInterface):
    """
    Gets texts from Image
    """
    def __init__(self, path:str='test.webp') -> list:
        self.path = path
    
    def get_texts(self) -> list:
        pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
                
        #Open image with PIL
        img = Image.open(self.path)

        #Extract text from image
        texts = pytesseract.image_to_string(img)
        
        return [texts]
      
file_path = 'test2.png'
file_text = ReadableFile(file_path).read_out()