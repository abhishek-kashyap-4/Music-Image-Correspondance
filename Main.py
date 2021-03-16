# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 04:12:27 2021

@author: kashy
"""
import numpy as np
from PIL import Image
from scipy.io import wavfile
import math

'''
use preprocessing to do other tasks such as 
Taking the averages in a wav file and then sending it to the functions
(The functions will not calculate the averages. They will just map each sound channel to each image channel )
compress or add aditional data
compute frequency
Other special editing you want to do.
'''

def preprocess_sound(sound):
    new_sound=[]
    return sound
def preprocess_image(image):
    new_image=[]
    return image

def wav_to_gray(sound,old_size):
    size= math.floor(math.sqrt(sound.shape[0]))
    if(old_size==-1):
        s1=size
        s2=size
    else:
        s1,s2 = old_size
    noch = np.size(sound,1)  
    if(noch==1):
        im = Image.new("L",(s1,s2))
        for i in range(s2):
            for j in range(s1):
                dat1=int(sound[i * s1 + j,0]) #assuming wav is 2d with size 1 instead of 1d
                im.putpixel((i, j), (dat1))
    #if there are more than 2 channels, only the first 2 will be considered. 2nd will be the alpha channel
    elif(noch >= 2): #with the alpha channel   
        im = Image.new("LA", (s1,s2))
        for i in range(s2):
            for j in range(s1):
                dat1=int(sound[i * s1 + j,0])
                dat2=int(sound[i * s1 + j,1])
                im.putpixel((i, j), (dat1,dat2))
    im.show()
    return im
def any_img_to_wav(image):
    imdata= np.int16(np.asarray(image))
    #will get error for L and BW, since they don't have a  3rd dimension
    #account for that
    full_data=[]
    if(imdata.ndim == 2):
        data=[]
        for x in imdata:
            for y in x:
                data.append(y)
        full_data.append(data)
        full_data= np.transpose(np.array(full_data))
        return full_data
                
    else:
        for l in range(np.size(imdata,2)):
            data=[]
            for x in imdata[:,:,l]:
                for y in x:
                    data.append(y)
            full_data.append(data)
        full_data= np.transpose(np.array(full_data))
        return full_data
def gray_to_wav(image):
    return any_img_to_wav(image)
def wav_to_RGB(sound,old_size):
    size= math.floor(math.sqrt(sound.shape[0]))
    if(old_size==-1):
        s1 = size
        s2 = size
    else:
        s1,s2=old_size
    noch = np.size(sound,1)  
    if(noch==3):
        im = Image.new("RGB",(s1,s2))
        for i in range(s2):
            for j in range(s1):
                dat1=int(sound[i * s1 + j,0]) 
                dat2=int(sound[i * s1 + j,1]) 
                dat3=int(sound[i * s1 + j,2]) 
                im.putpixel((j,i), (dat1,dat2,dat3))
    #if there are more than 4 channels, only the first 4 will be considered. 4th will be the alpha channel
    elif(noch >= 4): #with the alpha channel   
        im = Image.new("RGBA", (s1,s2))
        for i in range(s2):
            for j in range(s1):
                dat1=int(sound[i * s1 + j,0]) 
                dat2=int(sound[i * s1 + j,1]) 
                dat3=int(sound[i * s1 + j,2]) 
                dat4=int(sound[i * s1 + j,3]) 
                im.putpixel((j,i), (dat1,dat2,dat3,dat4))
    elif(noch ==2):
        im = Image.new("RGB",(s1,s2))
        for i in range(s2):
            for j in range(s1):
                dat1=int(sound[i * s1 + j,0]) 
                dat2=int(sound[i * s1 + j,1]) 
                im.putpixel((j,i), (dat1,dat2,0))
    elif(noch ==1):
        im = Image.new("RGB",(s1,s2))
        for i in range(s2):
            for j in range(s1):
                dat1=int(sound[i * s1 + j,0]) 
                im.putpixel((j,i), (dat1,0,0))
    im.show()
    return im
def RGB_to_wav(image):
    return any_img_to_wav(image)
def wav_to_BW(sound,old_size):
    size= math.floor(math.sqrt(sound.shape[0]))
    if(old_size==-1):
        s1 = size
        s2 = size
    else:
        s1,s2=old_size
    noch = np.size(sound,1)  
    if(noch>=1):
        im = Image.new("1",(s1,s2))
        for i in range(s2):
            for j in range(s1):
                dat1=int(sound[i * s1 + j,0]) 
                im.putpixel((i, j), (dat1))
    
    im.show()
    return im
def BW_to_wav(image):
    return any_img_to_wav(image)







list_of_sound_files=[
    'Music//input//Wav//OneWav.wav'
    
    ]

list_of_image_files=[
    #'Image//input//RGB//OneRGB.jpg'
    ]

for path in list_of_sound_files:
    item = path.split('//')[-1].split('.')[0]
    
    samplerate,sound=wavfile.read(path)
    sound=preprocess_sound(sound)
    
    RGB_image = wav_to_RGB(sound,-1)
    RGB_image.save("Image//output//RGB//"+item+".png")
    #recheck
    image = Image.open("Image//output//RGB//"+item+".png")
    wav_sound_from_RGB = RGB_to_wav(image)
    wavfile.write("Music//output//Wav//"+item+"_RGBdoublechecker.wav",samplerate,wav_sound_from_RGB)

    Gray_image=wav_to_gray(sound,-1)
    Gray_image.save("Image//output//Gray//"+item+".png")
    #recheck
    image = Image.open("Image//output//Gray//"+item+".png")
    wav_sound_from_Gray = gray_to_wav(image)
    wavfile.write("Music//output//Wav//"+item+"_Graydoublechecker.wav",samplerate,wav_sound_from_Gray)
    
    BW_image = wav_to_BW(sound,-1)
    BW_image.save("Image//output//BW//"+item+".png")
    #recheck
    image = Image.open("Image//output//BW//"+item+".png")
    wav_sound_from_BW = BW_to_wav(image)
    wavfile.write("Music//output//Wav//"+item+"_BWdoublechecker.wav",samplerate,wav_sound_from_BW)
    
for path in list_of_image_files:
    item = path.split('//')[-1].split('.')[0]
    image=Image.open(path)
    size = image.size
    image = preprocess_image(image)
    if("RGB" in path):
        wav_sound_from_RGB = RGB_to_wav(image)
        wavfile.write("Music//output//Wav//"+item+".wav",8000,wav_sound_from_RGB)
        #recheck
        samplerate, sound = wavfile.read("Music//output//Wav//"+item+".wav")
        RGB_image=wav_to_RGB(sound,size)
        RGB_image.save("Image//output//RGB//"+item+"_doublechecker.png")
    elif("Gray" in path):
        wav_sound_from_Gray = gray_to_wav(image)
        wavfile.write("Music//output//Wav//"+item+".wav",8000,wav_sound_from_Gray)
        #recheck
        samplerate, sound = wavfile.read("Music//output//Wav"+item+".wav")
        Gray_image=wav_to_gray(sound)
        Gray_image.save("Image//output//Gray//"+item+"_doublechecker.png")
    elif("BW" in path):
        wav_sound_from_BW = BW_to_wav(image)
        wavfile.write("Music//output//Wav//"+item+".wav",8000,wav_sound_from_BW)
        #recheck
        samplerate, sound = wavfile.read("Music//output//Wav"+item+".wav")
        BW_image=wav_to_BW(sound)
        BW_image.save("Image//output//BW//"+item+"_doublechecker.png")
    
    
    
    
    
    
    

