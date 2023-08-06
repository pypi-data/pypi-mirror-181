from detextify.detextifier import Detextifier
from detextify.inpainter import DiffusersSDInpainter
from detextify.text_detector import PaddleTextDetector

text_detector = PaddleTextDetector()
inpainter = DiffusersSDInpainter()

detextifier = Detextifier(text_detector, inpainter)

detextifier.detextify("/home/venus/Downloads/images/DALL·E_2022_12_07_14.46.09.png", "dalle_detextified.png")
