#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 23:22:40 2019

@author: Shruti & Shantanu
"""


import sys
from tkinter import *
import tkinter
import threading
import numpy as np
from threading import Thread, Lock
import time;
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks, filtfilt
from scipy import signal
import serial

global L5;
global L6;


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    #y = lfilter(b, a, data)
    y = filtfilt(b, a, data)

    return y

#order = 6
#fs = 100.0       # sample rate, Hz
#cutoff = 5  # desired cutoff frequency of the filter, Hz

#root = tkinter.Tk()
#root.geometry('500x500')
#counter=0;
#A=[1,2,3,4,5];
#m=10;

buttons = ['a','b','c','d','e','f','g','h','i','j','k','l','Space','BackSpace','1/2','1/3']
buttons2 = ['A','B','C','D','E','F','G','H','I','J','K','L','Space','BackSpace','2/1','2/3']
buttons3=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', ',', 'Space', 'BackSpace','3/1','3/2']
#global var_add
#var_add = ''

class keyboard_switch(tkinter.Tk):
    
    def __init__(self,*arg,**kwargs):
        
        tkinter.Tk.__init__(self,*arg,**kwargs)
        container = tkinter.Frame(self)
        
        container.pack(side="top", fill='both',expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (kb_page1, kb_page2, kb_page3):
                
            frame  = F(container, self)
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(kb_page1)
        
    def show_frame(self, cont):
        
        cont.refill()
        frame = self.frames[cont]
        frame.tkraise()

class kb:
    activePage = 1
    var_add = ''
    var_add1= '';
        
class kb_page1(tkinter.Frame, threading.Thread, kb):
    txtDisplay = None
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        
        #print('hiiii')
        self.controller=controller
        print("Page1 Init Called")
        threading.Thread.__init__(self)
        
#        global txtDisplay
        kb_page1.txtDisplay1 = tkinter.Entry(self, font='Helvetica 25 bold', width=35, bd=15)
        kb_page1.txtDisplay1.grid(row=1,column = 0,columnspan = 4,padx=5,pady=10,ipady=3)
        kb_page1.txtDisplay2 = tkinter.Entry(self, font='Helvetica 25 bold', width=7, bd=15)
        kb_page1.txtDisplay2.grid(row=2,column = 0,columnspan = 1,padx=5,pady=10,ipady=3)
        kb_page1.txtDisplay3 = tkinter.Entry(self, font='Helvetica 25 bold', width=7, bd=15)
        kb_page1.txtDisplay3.grid(row=2,column = 3,columnspan = 1,padx=5,pady=10,ipady=3)
        
        kb_page1.txtDisplay1.delete(0,tkinter.END)
        kb_page1.txtDisplay1.insert(tkinter.END,kb.var_add)
        print("1")
        #txtDisplay.bind("<Button-1>", lambda e: Key_buttons())
        #controller
        var_row = 3
        var_col = 0
        
        
        for button in buttons:
        #print(button)
            command = lambda x=button: self.select(x)
        
            tkinter.Button(self, text=button, height=3, width=10, font="Times 20 bold", bg="#3c4987", fg="#ffffff", command = command).grid(row = var_row,column = var_col)

            var_col = var_col + 1
    
            if var_col >= 4:
                var_col = 0
                var_row = var_row + 1
                #print(var_row,var_col)
                
        
        self.start()
        
    def run(self):
        print("Page1 Run Called", kb.activePage)
        
        arduino = serial.Serial('COM14',9600,timeout=0.1)

        #if(kb.activePage != 1): return 
        order = 6
        fs = 100.0       # sample rate, Hz
        cutoff = 5  # desired cutoff frequency of the filter, Hz

        L1=[0];
        L2=[0];

        flag=0;
        flag2a=0;
        flag2b=0;
        flag2c=0;
        flag3=0;
        flag4=0;
        flag5=0;
        flag6a=0
        flag6b=0;
        flag7=0;
        T=[0]
        p_time1=[0];
        t_time1=[0];
        p_height1=[0];
        t_height1=[0];
        p_time2=[0];
        t_time2=[0];
        p_height2=[0];
        t_height2=[0];
        t_len=0;

        i_p1=0;
        i_t1=0;
        i_p2=0;
        i_t2=0;
        
        # tf= final time, vf=final values
        t_f=[];
        v_f=[];

        i_sig=0;
        sig=[];

        #sos = signal.butter(1,10,'lp', fs=1000, output='sos')



        counter=0;
        #sig=[1,1,2,3,5,5,5,4,4,5,5];
        m=1;
        r=0;
        c=0;
        flag1_g=0;
        flag2_g=0;
        flag3_g=0;# flag 3 such that the blink code doesn't get executed in the same counter interation as getting the c value code
        user_input='';
        loop_active = True
        while loop_active:
            
            try:
                
                data=arduino.readline();
                t=datetime.datetime.now();
                
                if data:
            
            
                    #print (data)
                    x=(data[0:len(data)-2].decode('utf-8'));
                    index=x.find('p');
                    if(x!='\n'):
                        #L.append(float(x))
                        L1.append(int(x[0:index]));
                        L2.append(int(x[index+1:len(x)]));                
                        t3M=t.minute;
                        t3s=t.second;
                        t3m=t.microsecond;
            
                    if (flag==0 and x!='\n'):
                        t1M=t.minute;
                        t1s=t.second;
                        t1m=t.microsecond;
                        t2s=t1s+5;
                        t2m=t1m;
                        flag=1;
                    T1=t1M*60*1000000 + t1s*1000000 + t1m;    
                    T.append(((t3M*60*1000000)+(t3s*1000000)+(t3m)) - T1);
                
                if(T[-1]%2000000 > 300000 and T[-1]%2000000 < 700000):
                    flag3=0;
                    
                if (flag2a==0 and T[-1]>2000000):
                    n1=int (len(T));
                    flag2a=1;
                    n3=int (len(T));
        
                if (flag2b==0 and T[-1]>4000000):
                    n2=int (len(T));
                    flag2b=1;
                if(flag2c==0 and flag2a==1 and flag2b==1):
                    n=n2-n1;
                    flag2c=1;
            
                if(flag5==0 and T[-1]>8000000):
                    n4=int(len(T));
                    flag5=1;
                    Z1=L1[n3:n4];
                    Z2=L2[n3:n4];
                    Z2a = butter_lowpass_filter(Z2, cutoff, fs, order)
                    Z1a = butter_lowpass_filter(Z1, cutoff, fs, order)
                    avg1=sum(Z1a)/(n4-n3);
                    avg2=sum(Z2a)/(n4-n3);
                
                if(flag3==0 and T[-1]>10000000 and T[-1]%2000000 < 200000  ):
                    
                    #L5=L1;
                    #L6=L2;
                    print (len(L1));
                    print(len(L2));
                    flag3=1;
                    flag4=0; 
                    
                    T_u1 = avg1+110;
                    T_d1 = avg1-100;     
            
                    T_u2=avg2+100;
                    T_d2=avg2-100;
                    
                    if(flag7==0):
                        flag7=1;
                        c_data1a = L1[-n:-1];
                        c_data2a = L2[-n:-1];
                        c_time  = T[-n:-1];
                        t_len=len(T);
                    else:
                        c_data1a = L1[t_len:-1];
                        c_data2a = L2[t_len:-1];
                        c_time  = T[t_len:-1];
                        t_len=len(T);
                        
                    c_data1 = butter_lowpass_filter(c_data1a, cutoff, fs, order) ;   
                    c_data2 = butter_lowpass_filter(c_data2a, cutoff, fs, order) ;
            
                    c_data3=[];
                    c_data4=[];
                    c_data3=np.dot(c_data1,-1);
                    c_data4=np.dot(c_data2,-1);
            
                    peaks1, height1 = find_peaks(c_data1, height=T_u1, distance=20);
            
            
                    troughs1, depth1 = find_peaks(c_data3, height=(-T_d1), distance=20);
                    height1_list=list(height1.values());
                    depth1_list=list(depth1.values());
                    depth1_list=np.dot(depth1_list,-1);

            
                    i_p1=len(p_time1);
                    i_t1=len(t_time1);    
                    i_p2=len(p_time2);
                    i_t2=len(t_time2);
                    
                    for i in range(len(peaks1)):
                        p_height1.append(height1_list[0][i]);
                        p_time1.append(c_time[peaks1[i]]);
            
            
                    for i in range(len(troughs1)):
                        t_height1.append(depth1_list[0][i]);
                        t_time1.append(c_time[troughs1[i]]);
                        
                    peaks2, height2 = find_peaks(c_data2, height=T_u2, distance=20);
                    troughs2, depth2 = find_peaks(c_data4, height=-T_d2, distance=20);
            
                    height2_list=list(height2.values());
                    depth2_list=list(depth2.values());
                    depth2_list=np.dot(depth2_list,-1);
                    
                    for i in range(len(peaks2)):
                        p_height2.append(height2_list[0][i]);
                        p_time2.append(c_time[peaks2[i]]);
            
                    for i in range(len(troughs2)):
                        t_height2.append(depth2_list[0][i]);
                        t_time2.append(c_time[troughs2[i]]);
            
            
                    j_p1=i_p1;
                    j_t1=i_t1;
                    j_p2=i_p2;
                    j_t2=i_t2;
                    
                    p_time3=p_time1[0:len(p_time1)];
                    t_time3=t_time1[0:len(t_time1)];
                    p_time4=p_time2[0:len(p_time2)];
                    t_time4=t_time2[0:len(t_time2)];
            
                    try:
                        M=max(p_time3[-1], t_time3[-1], p_time4[-1], t_time4[-1])+1000;
                    except IndexError:
                        M=150000000;
                        #continue;
                    while(flag4==0):
                
                        if(j_p1==len(p_time3) and j_t1==len(t_time3) and j_p2==len(p_time4) and j_t2==len(t_time4)):
                            flag4=1;
                        
                        else:
                            k_p1=j_p1;
                            k_t1=j_t1;
                            k_p2=j_p2;
                            k_t2=j_t2;
                            
                            if(j_p1==len(p_time3)):
                                p_time3[-1]=M;
                                k_p1=j_p1-1;
                            if(j_t1==len(t_time3)):
                                t_time3[-1]=M;
                                k_t1=j_t1-1;
                            if(j_p2==len(p_time4)):
                                p_time4[-1]=M;
                                k_p2=j_p2-1;
                            if(j_t2==len(t_time4)):
                                t_time4[-1]=M;  
                                k_t2=j_t2-1;
                                
                                
                            mini=min(p_time3[k_p1],t_time3[k_t1], p_time4[k_p2], t_time4[k_t2]);
                            t_f.append(mini);
                    
                            if(mini==p_time3[k_p1]):
                                j_p1=j_p1+1;
                                v_f.append(1);
                            elif (mini==t_time3[k_t1]):
                                j_t1=j_t1+1;
                                v_f.append(2);
                            elif(mini==p_time4[k_p2]):
                                j_p2=j_p2+1;
                                v_f.append(3);
                            elif(mini==t_time4[k_t2]):
                                j_t2=j_t2+1;
                                v_f.append(4);
                        
                        
                        j_sig=i_sig;
                        
                        while(j_sig<len(v_f)-1):
                            if(v_f[j_sig]==3 or v_f[j_sig]==4):
                                if(v_f[j_sig+1]==1 or v_f[j_sig+1]==2):
                                    if(t_f[j_sig+1]-t_f[j_sig]<100000):
                                        v_f[j_sig+1]=0;
                            j_sig=j_sig+1;
                            
                        
                        while(i_sig<len(v_f)-1):
                            if(v_f[i_sig]==1):
                                if(v_f[i_sig+1]==2):
                                    if(t_f[i_sig+1]-t_f[i_sig]<500000):
                                        sig.append(5);
                                        print('Blink');
                                        i_sig=i_sig+1;
                                    elif(t_f[i_sig+1]-t_f[i_sig]<1500000):
                                        sig.append(1);
                                        print('Up');
                                        i_sig=i_sig+1;
                            elif(v_f[i_sig]==2):
                                if(v_f[i_sig+1]==1 and t_f[i_sig+1]-t_f[i_sig]<1500000):
                                    sig.append(2);
                                    print('Down');
                                    i_sig=i_sig+1;
                            elif(v_f[i_sig]==3):
                                if(flag6b==1):
                                    flag6b=0;
                                elif(flag6b==0):
                                    if(v_f[i_sig+1]==0 and t_f[i_sig+1]-t_f[i_sig]<1500000):
                                        sig.append(3);
                                        print('Left');
                                        i_sig=i_sig+1;
                                        flag6a=1;
                                    elif(v_f[i_sig+1]==4 and t_f[i_sig+1]-t_f[i_sig]<1500000):
                                        sig.append(3);
                                        print('Left');
                                        i_sig=i_sig+1;
                            elif(v_f[i_sig]==4):
                                print(flag6a);
                                print(i_sig);
                                if(flag6a==1):
                                    flag6a=0;
                                elif(flag6a==0):
                                    if(v_f[i_sig+1]==3 and t_f[i_sig+1]-t_f[i_sig]<1500000):
                                        sig.append(4);
                                        print('Right');
                                        i_sig=i_sig+1;
                                    elif(v_f[i_sig+1]==0 and t_f[i_sig+1]-t_f[i_sig]<1500000):
                                        sig.append(4);
                                        print('Right');
                                        i_sig=i_sig+1;
                                        flag6b=1;
                                        
                                        
                            i_sig=i_sig+1;
                    
#                       for i in range(1):
#                           sig.append(m);
#                           m=m+1;
#                           if(m==6):
#                                sig.append(5);
#                                m=1;
#                        
#                       time.sleep(1);
            
                
                        print(sig);
                        #time.sleep(3);    
                        while(counter<len(sig)):
                            
                            if(len(kb.var_add)>=35):
                                kb.var_add1=kb.var_add1 + kb.var_add[0];
                                kb.var_add=kb.var_add[1:len(kb.var_add)]
                            
                            if(flag3_g==1):
                                flag3_g=0;
                            if(r==0):
                                if(sig[counter]==5):
                                    counter=counter+1;
                                    continue;
                                r=sig[counter];
                                counter=counter+1;
                                kb_page1.txtDisplay2.delete(0,tkinter.END)
                                kb_page1.txtDisplay2.insert(tkinter.END,str(r))
                                kb_page2.txtDisplay2.delete(0,tkinter.END)
                                kb_page2.txtDisplay2.insert(tkinter.END,str(r))
                                kb_page3.txtDisplay2.delete(0,tkinter.END)
                                kb_page3.txtDisplay2.insert(tkinter.END,str(r))
                                #kb_page1.txtDisplay3.delete(0,tkinter.END)
                                #kb_page1.txtDisplay3.insert(tkinter.END,str(c))
                                #print(r);
                                #continue;
                                
                            elif(r!=0 and c==0):
                                if(sig[counter]==5):
                                    counter=counter+1;
                                    continue;
                                c=sig[counter];
                                counter=counter+1;
                                flag3_g=1;
                                #kb_page1.txtDisplay2.delete(0,tkinter.END)
                                #kb_page1.txtDisplay2.insert(tkinter.END,str(r))
                                kb_page1.txtDisplay3.delete(0,tkinter.END)
                                kb_page1.txtDisplay3.insert(tkinter.END,str(c))
                                kb_page2.txtDisplay3.delete(0,tkinter.END)
                                kb_page2.txtDisplay3.insert(tkinter.END,str(c))
                                kb_page3.txtDisplay3.delete(0,tkinter.END)
                                kb_page3.txtDisplay3.insert(tkinter.END,str(c)) 
                                #print(c);
                                #continue;
                            #print(r); 
                            #kb_page1.txtDisplay2.delete(0,tkinter.END)
                            #kb_page1.txtDisplay2.insert(tkinter.END,str(r))
                            #print(c);
                            #kb_page1.txtDisplay3.delete(0,tkinter.END)
                            #kb_page1.txtDisplay3.insert(tkinter.END,str(c))
                
                            if(r!=0 and c!=0 and flag3_g==0):
                                if (sig[counter]==5 and flag1_g==0):
                                    flag1_g=1;
                                    counter=counter+1;
                                elif(flag1_g==1 and sig[counter]==5):# for r-c-blink-blink
                                    flag2_g=1;
                                    counter=counter+1;
                                elif(flag1_g==1 and sig[counter]!=5): #for r-c-blink-r
                                    flag1_g=0;
                                    flag2_g=0;
                                    c=0;
                                    r=sig[counter];
                                    counter=counter+1;
                                    kb_page1.txtDisplay2.delete(0,tkinter.END)
                                    kb_page1.txtDisplay2.insert(tkinter.END,str(r))
                                    kb_page1.txtDisplay3.delete(0,tkinter.END)
                                    kb_page1.txtDisplay3.insert(tkinter.END,str(c))
                                    kb_page2.txtDisplay2.delete(0,tkinter.END)
                                    kb_page2.txtDisplay2.insert(tkinter.END,str(r))
                                    kb_page2.txtDisplay3.delete(0,tkinter.END)
                                    kb_page2.txtDisplay3.insert(tkinter.END,str(c))
                                    kb_page3.txtDisplay2.delete(0,tkinter.END)
                                    kb_page3.txtDisplay2.insert(tkinter.END,str(r))
                                    kb_page3.txtDisplay3.delete(0,tkinter.END)
                                    kb_page3.txtDisplay3.insert(tkinter.END,str(c))
                                    #time.sleep(0.1);
                                elif(sig[counter]!=5): # For r-c-r
                                    r=sig[counter];
                                    c=0;
                                    counter=counter+1;
                                    kb_page1.txtDisplay2.delete(0,tkinter.END)
                                    kb_page1.txtDisplay2.insert(tkinter.END,str(r))
                                    kb_page1.txtDisplay3.delete(0,tkinter.END)
                                    kb_page1.txtDisplay3.insert(tkinter.END,str(c))
                                    kb_page2.txtDisplay2.delete(0,tkinter.END)
                                    kb_page2.txtDisplay2.insert(tkinter.END,str(r))
                                    kb_page2.txtDisplay3.delete(0,tkinter.END)
                                    kb_page2.txtDisplay3.insert(tkinter.END,str(c))
                                    kb_page3.txtDisplay2.delete(0,tkinter.END)
                                    kb_page3.txtDisplay2.insert(tkinter.END,str(r))
                                    kb_page3.txtDisplay3.delete(0,tkinter.END)
                                    kb_page3.txtDisplay3.insert(tkinter.END,str(c))
                                    
                                    
                                if(flag1_g==1 and flag2_g==1):
                                    if(kb.activePage==1):
                                        if(r==1 and c==1):
                                            print('u_a');
                                            user_input='a';
                                        elif(r==1 and c==2):
                                            print('u_b');
                                            user_input='b';
                                        elif(r==1 and c==3):
                                            print('u_c');
                                            user_input='c';
                                        elif(r==1 and c==4):
                                            print('u_d');
                                            user_input='d';
                                        elif(r==2 and c==1):
                                            print('u_e');
                                            user_input='e';
                                        elif(r==2 and c==2):
                                            print('u_f');
                                            user_input='f';
                                        elif(r==2 and c==3):
                                            print('u_g');
                                            user_input='g';
                                        elif(r==2 and c==4):
                                            print('u_h');
                                            user_input='h';
                                        elif(r==3 and c==1):
                                            print('u_i');
                                            user_input='i';
                                        elif(r==3 and c==2):
                                            print('u_j');
                                            user_input='j';
                                        elif(r==3 and c==3):
                                            print('u_k');
                                            user_input='k';
                                        elif(r==3 and c==4):
                                            print('u_l');
                                            user_input='l';
                                        elif(r==4 and c==1):
                                            print('Space');
                                            user_input=' ';
                                        elif(r==4 and c==2):
                                            print('Backspace');
                                            user_input='clc';                            
                                        elif(r==4 and c==3):
                                            user_input='1/2';
                                        elif(r==4 and c==4):
                                            user_input='1/3';
                                
                                    elif(kb.activePage==2):
                                        if(r==1 and c==1):
                                            print('u_A');
                                            user_input='A';
                                        elif(r==1 and c==2):
                                            print('u_B');
                                            user_input='B';
                                        elif(r==1 and c==3):
                                            print('u_C');
                                            user_input='C';
                                        elif(r==1 and c==4):
                                            print('u_D');
                                            user_input='D';
                                        elif(r==2 and c==1):
                                            print('u_E');
                                            user_input='E';
                                        elif(r==2 and c==2):
                                            print('u_F');
                                            user_input='F';
                                        elif(r==2 and c==3):
                                            print('u_G');
                                            user_input='G';
                                        elif(r==2 and c==4):
                                            print('u_H');
                                            user_input='H';
                                        elif(r==3 and c==1):
                                            print('u_I');
                                            user_input='I';
                                        elif(r==3 and c==2):
                                            print('u_J');
                                            user_input='J';
                                        elif(r==3 and c==3):
                                            print('u_K');
                                            user_input='K';
                                        elif(r==3 and c==4):
                                            print('u_L');
                                            user_input='L';
                                        elif(r==4 and c==1):
                                            print('Space');
                                            user_input=' ';
                                        elif(r==4 and c==2):
                                            print('Backspace');
                                            user_input='clc';                            
                                        elif(r==4 and c==3):
                                            user_input='2/1';
                                        elif(r==4 and c==4):
                                            user_input='2/3';
                                        
                                        
                                    elif(kb.activePage==3):
                                        if(r==1 and c==1):
                                            print('1');
                                            user_input='1';
                                        elif(r==1 and c==2):
                                            print('2');
                                            user_input='2';
                                        elif(r==1 and c==3):
                                            print('3');
                                            user_input='3';
                                        elif(r==1 and c==4):
                                            print('4');
                                            user_input='4';
                                        elif(r==2 and c==1):
                                            print('5');
                                            user_input='5';
                                        elif(r==2 and c==2):
                                            print('6');
                                            user_input='6';
                                        elif(r==2 and c==3):
                                            print('7');
                                            user_input='7';
                                        elif(r==2 and c==4):
                                            print('8');
                                            user_input='8';
                                        elif(r==3 and c==1):
                                            print('9');
                                            user_input='9';
                                        elif(r==3 and c==2):
                                            print('0');
                                            user_input='0';
                                        elif(r==3 and c==3):
                                            print('.');
                                            user_input='.';
                                        elif(r==3 and c==4):
                                            print(',');
                                            user_input=',';
                                        elif(r==4 and c==1):
                                            print('Space');
                                            user_input=' ';
                                        elif(r==4 and c==2):
                                            print('Backspace');
                                            user_input='clc';                            
                                        elif(r==4 and c==3):
                                            user_input='3/1';
                                        elif(r==4 and c==4):
                                            user_input='3/2';
                                        
                                    #time.sleep(1);
                                    #user_input=str(sig[counter]);
                                    #user_input = input("Page1: Give me your command! Just type \"exit\" to close: ")
                                    if(user_input=='1/2'):
                                        kb.activePage=2;
                                        self.select('1/2');
                                    elif(user_input=='1/3'):
                                        kb.activePage=3;
                                        #print("Change it2")
                                        self.select('1/3');
                                    elif(user_input=='2/1'):
                                        kb.activePage=1;
                                        self.controller.show_frame(kb_page1)
                                    elif(user_input=='2/3'):
                                        kb.activePage=3;
                                        self.controller.show_frame(kb_page3) 
                                    elif(user_input=='3/1'):
                                        kb.activePage=1;
                                        self.controller.show_frame(kb_page1) 
                                    elif(user_input=='3/2'):
                                        kb.activePage=2;
                                        self.controller.show_frame(kb_page2)
                                    elif(user_input=='clc'):
                                        print('pressed backspace')
                                        kb.var_add = kb.var_add[:len(kb.var_add)-1]
                                        kb_page1.txtDisplay1.delete(0,tkinter.END)
                                        kb_page1.txtDisplay1.insert(tkinter.END,kb.var_add)
                                        kb_page2.txtDisplay1.delete(0,tkinter.END)
                                        kb_page2.txtDisplay1.insert(tkinter.END,kb.var_add)
                                        kb_page3.txtDisplay1.delete(0,tkinter.END)
                                        kb_page3.txtDisplay1.insert(tkinter.END,kb.var_add)
                                        
                                        
                                    elif user_input == "exit":
                                        loop_active = False
                                        self.controller.destroy()
                                        self.controller.update()
                                    else:
                                        kb.var_add = kb.var_add + user_input
                                        if kb.activePage == 1:  
                                            kb_page1.txtDisplay1.delete(0,tkinter.END)
                                            kb_page1.txtDisplay1.insert(tkinter.END,kb.var_add)
                                        elif kb.activePage == 2:
                                            kb_page2.txtDisplay1.delete(0,tkinter.END)
                                            kb_page2.txtDisplay1.insert(tkinter.END,kb.var_add)  
                                            #counter=counter+1;
                                            #time.sleep(1);
                                        elif kb.activePage == 3:
                                            kb_page3.txtDisplay1.delete(0,tkinter.END)
                                            kb_page3.txtDisplay1.insert(tkinter.END,kb.var_add)
                                            #time.sleep(1);
                
                            print(flag1_g);
                            print(flag2_g);
                            print('next iteration');
                            if(c!=0 and r!=0 and flag1_g==1 and flag2_g==1):
                                r=0;
                                c=0;
                                flag1_g=0;
                                flag2_g=0;
                                kb_page1.txtDisplay2.delete(0,tkinter.END)
                                kb_page1.txtDisplay2.insert(tkinter.END,str(r))
                                kb_page1.txtDisplay3.delete(0,tkinter.END)
                                kb_page1.txtDisplay3.insert(tkinter.END,str(c))
                                kb_page2.txtDisplay2.delete(0,tkinter.END)
                                kb_page2.txtDisplay2.insert(tkinter.END,str(r))
                                kb_page2.txtDisplay3.delete(0,tkinter.END)
                                kb_page2.txtDisplay3.insert(tkinter.END,str(c))
                                kb_page3.txtDisplay2.delete(0,tkinter.END)
                                kb_page3.txtDisplay2.insert(tkinter.END,str(r))
                                kb_page3.txtDisplay3.delete(0,tkinter.END)
                                kb_page3.txtDisplay3.insert(tkinter.END,str(c))
                                #time.sleep(1);
                
                
                
            except KeyboardInterrupt:
                print('A');
                break;        
    
            except ValueError:
                continue;                
            
                                        
    def select(self, var_button):
        #kb_page2.run(var_button)
        if  var_button == '1/2':
            kb.activePage = 2
            #print("Change it1")
            self.controller.show_frame(kb_page2)
            #self.txtDisplay.insert(tkinter.END,kb.var_add)
            #global buttons
            #buttons = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','1/2']
        elif  var_button == '1/3':
            kb.activePage = 3
            #print("Change it1")
            self.controller.show_frame(kb_page3)                
        else:
            #print("page1 select else")
            #print(var_button)
            kb.var_add = kb.var_add + var_button
            kb_page1.txtDisplay1.delete(0,tkinter.END)
            kb_page1.txtDisplay1.insert(tkinter.END,kb.var_add)
            

            
    @classmethod
    def refill(cls):
        cls.txtDisplay1.delete(0,tkinter.END)
        cls.txtDisplay1.insert(tkinter.END,kb.var_add) 

class kb_page2(tkinter.Frame, threading.Thread, kb):
    txtDisplay = None
    def __init__(self, parent, controller):
        
        tkinter.Frame.__init__(self, parent)
        #print('hiiii')
        self.controller = controller
        threading.Thread.__init__(self)
        print("Page2 Init Called")
        
        #global txtDisplay
        kb_page2.txtDisplay1 = tkinter.Entry(self, font='Helvetica 25 bold', width=35, bd=15)
        kb_page2.txtDisplay1.grid(row=1,column = 0,columnspan = 4,padx=5,pady=10,ipady=3)
        kb_page2.txtDisplay2 = tkinter.Entry(self, font='Helvetica 25 bold', width=7, bd=15)
        kb_page2.txtDisplay2.grid(row=2,column = 0,columnspan = 1,padx=5,pady=10,ipady=3)
        kb_page2.txtDisplay3 = tkinter.Entry(self, font='Helvetica 25 bold', width=7, bd=15)
        kb_page2.txtDisplay3.grid(row=2,column = 3,columnspan = 1,padx=5,pady=10,ipady=3)
        
        kb_page2.txtDisplay1.delete(0,tkinter.END)
        kb_page2.txtDisplay1.insert(tkinter.END,kb.var_add)
        #txtDisplay.bind("<Button-1>", lambda e: Key_buttons())
        
        
        
        var_row = 3
        var_col = 0
        
        
        for button in buttons2:
        #print(button)
            command = lambda x=button: self.select(x)
        
            tkinter.Button(self, text=button, height=3, width=10, font="Times 20 bold", bg="#3c4987", fg="#ffffff", command = command).grid(row = var_row,column = var_col)

            var_col = var_col + 1
    
            if var_col >= 4:
                var_col = 0
                var_row = var_row + 1
                #print(var_row,var_col)
        self.start()

                    
    def select(self, var_button):
    
        if  var_button == '2/1':
            kb.activePage = 1
            #print("Change it2")
            self.controller.show_frame(kb_page1)
            #self.txtDisplay.insert(tkinter.END,kb.var_add)
            
        elif  var_button == '2/3':
            kb.activePage = 3
            #print("Change it2")
            self.controller.show_frame(kb_page3)
            #self.txtDisplay.insert(tkinter.END,kb.var_add)
            
        elif var_button == 'Clc':
            print('pressed backspace')
            kb.var_add = kb.var_add[:len(kb.var_add)-1]
            kb_page2.txtDisplay1.delete(0,tkinter.END)
            kb_page2.txtDisplay1.insert(tkinter.END,kb.var_add)
            
               
        else:
            #print("page2 select else")
            kb.var_add = kb.var_add + var_button
            kb_page2.txtDisplay1.delete(0,tkinter.END)
            kb_page2.txtDisplay1.insert(tkinter.END,kb.var_add)  
    
    @classmethod
    def refill(cls):
        cls.txtDisplay1.delete(0,tkinter.END)
        cls.txtDisplay1.insert(tkinter.END,kb.var_add) 
        
class kb_page3(tkinter.Frame, threading.Thread, kb):
    txtDisplay = None
    def __init__(self, parent, controller):
        
        tkinter.Frame.__init__(self, parent)
        #print('hiiii')
        self.controller = controller
        threading.Thread.__init__(self)
        print("Page3 Init Called")
        
        #global txtDisplay
        kb_page3.txtDisplay1 = tkinter.Entry(self, font='Helvetica 25 bold', width=35, bd=15)
        kb_page3.txtDisplay1.grid(row=1,column = 0,columnspan = 4,padx=5,pady=10,ipady=3)
        kb_page3.txtDisplay2 = tkinter.Entry(self, font='Helvetica 25 bold', width=7, bd=15)
        kb_page3.txtDisplay2.grid(row=2,column = 0,columnspan = 1,padx=5,pady=10,ipady=3)
        kb_page3.txtDisplay3 = tkinter.Entry(self, font='Helvetica 25 bold', width=7, bd=15)
        kb_page3.txtDisplay3.grid(row=2,column = 3,columnspan = 1,padx=5,pady=10,ipady=3)
        
        kb_page3.txtDisplay1.delete(0,tkinter.END)
        kb_page3.txtDisplay1.insert(tkinter.END,kb.var_add)
        #txtDisplay.bind("<Button-1>", lambda e: Key_buttons())
        
        
        
        var_row = 3
        var_col = 0
        
        
        for button in buttons3:
        #print(button)
            command = lambda x=button: self.select(x)
        
            tkinter.Button(self, text=button, height=3, width=10, font="Times 20 bold", bg="#3c4987", fg="#ffffff", command = command).grid(row = var_row,column = var_col)

            var_col = var_col + 1
    
            if var_col >= 4:
                var_col = 0
                var_row = var_row + 1
                #print(var_row,var_col)
        self.start()

                    
    def select(self, var_button):
    
        if  var_button == '3/1':
            kb.activePage = 1
            #print("Change it2")
            self.controller.show_frame(kb_page1)
            #self.txtDisplay.insert(tkinter.END,kb.var_add)
            
        
        if  var_button == '3/2':
            kb.activePage = 2
            #print("Change it2")
            self.controller.show_frame(kb_page2)
            #self.txtDisplay.insert(tkinter.END,kb.var_add)
        
        elif var_button == 'Clc':
            print('pressed backspace')
            kb.var_add = kb.var_add[:len(kb.var_add)-1]
            kb_page2.txtDisplay1.delete(0,tkinter.END)
            kb_page2.txtDisplay1.insert(tkinter.END,kb.var_add)
            
               
        else:
            #print("page2 select else")
            kb.var_add = kb.var_add + var_button
            kb_page2.txtDisplay1.delete(0,tkinter.END)
            kb_page2.txtDisplay1.insert(tkinter.END,kb.var_add)  
    
    @classmethod
    def refill(cls):
        cls.txtDisplay1.delete(0,tkinter.END)
        cls.txtDisplay1.insert(tkinter.END,kb.var_add) 

app = keyboard_switch()
app.title("Keyboard")
app.mainloop()
print('The text printed is :-\n',kb.var_add)
