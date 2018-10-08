import cv2
import numpy as np
import glob
import imutils
from PIL import Image
import pytesseract
import pandas as pd
import re
import matplotlib.pyplot as plt


class receipt_analyser:
    #def __init__(self):
        

    def main(self, receipt):
        ORG = []
        DATE = []
        TOTAL = [] 
        GST =[]
        # Regex for money
        pattern_money = re.compile('\$([0-9]+\.[0-9]+)|([0-9]+\.[0-9]+)\s+AUD|\$AUD\s+([0-9]+\.[0-9]+)|([0-9]+\.[0-9]+[\s\n])|\$([0-9]+[\s\n])', re.IGNORECASE)
        pattern_date = re.compile('[0-9]+/[0-9]+/[0-9]+')
        # Pre-process image
        img = cv2.imread(receipt,0)
        ret1, img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY) #180
        ret2, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img = cv2.GaussianBlur(img, (1, 1), 0)
        ret3, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img = Image.fromarray(img)
        # Visualise
        #plt.subplot(111)
        #plt.imshow(img, cmap = 'gray')
        #plt.show()
        # Apply OCR
        txt = pytesseract.image_to_string(img)
        sentences = txt.split('\n')
        sentences = [sent for sent in sentences if sent != '']
        print(txt)
        print('---')
        # Grab sentence with total and GST mentionned
        Total_sentence = ' '.join([sent for sent in sentences if(('total' in sent.lower() or 'purchase' in sent.lower()) and any(char.isdigit() for char in sent))])
        GST_sentence = ' '.join([sent for sent in sentences if('gst' in sent.lower() and any(char.isdigit() for char in sent))])
        if Total_sentence == '':    Total_sentence = txt
        if GST_sentence == '':    GST_sentence = txt
        # Apply spacy for total
        TOTAL = pattern_money.findall(Total_sentence)
        try:
            tot = []
            for tu in TOTAL:
                for s in tu:
                    if(s != ''): tot.append(s)
            TOTAL = tot
        except:
            TOTAL = []
        if(len(TOTAL) > 1):
            try:
                TOTAL = '$'+str(max([float(x) for x in TOTAL]))
            except:
                TOTAL = []
        elif(len(TOTAL) == 1):
            TOTAL = '$'+TOTAL[0]
        # Apply spacy for GST
        GST = pattern_money.findall(GST_sentence)
        try:
            tot = []
            for tu in GST:
                for s in tu:
                    if(s != ''): tot.append(s)
            GST = tot
        except:
            GST = []
        try:
            GST = '$'+str(min([float(x) for x in GST]))
        except:
            GST = []
        # search for a date
        DATE = pattern_date.findall(txt)
        if(len(DATE) !=0): DATE = DATE[0]    
        # Oragnisation
        ORG = ' '.join(sentences[0].split(' ')[0:2])
        return ORG, DATE, TOTAL, GST

if __name__ == '__main__':
    # Initialise process
    process = receipt_analyser()
    # Apply for each receipt
    receipts = []
    for receipt in sorted(glob.glob("../../Data/Receipts/*.jpg")):
        ORG, DATE, TOTAL, GST = process.main(receipt)
        receipts.append({'Receipt':receipt, 'Shop':ORG,'Date':DATE,'Total':TOTAL,'GST':GST})
        print('>> Receipt: ', receipt, "ORG: ", ORG, "Date: ", DATE, "Total: ", TOTAL, "GST: ", GST)
        print('===========================')
    DF = pd.DataFrame(receipts)
    DF.to_csv('Results.csv')
