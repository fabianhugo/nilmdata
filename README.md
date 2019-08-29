# nilmdata

## 5 Different Scenarios: 
1. Single Appliances without Switching Events 
2. Single Appliances with Switching Events
3. Multi Appliance Recording  
     3.1 Without Superposition of Loads
          - Order00: Heatbulb, Fan2, Fluorescent Light, Laptopcharger, Kettle  
          - Order01: Fan2, Fluorescent Light, Kettle, Laptopcharger, Heatbulb  
          - Order02: Kettle, Laptopcharger, Heatbulb, Microwave2, Fan2    
     3.2 With Superposition of Loads  
          - Order10: Heatbulb, Fan2, Fluorescent Light, Laptopcharger, Kettle  
          - Order11: Fan2, Fluorescent Light, Heatbulb, Kettle, Laptopcharger  
4. Extended Single Appliance Detection  
5. Switching Event Collection  

## Labels
label dictionary can be found in fileutils.py
0:'no load'  
1:'heatbulb'  
2:'kettle'  
3:'fan1'  
4:'fan2'  
5:'fan3'  
6:'microwaveon'  
7:'microwaveidle'  
8:'microwavestarting'  
9:'laptop'  
10:'monitor'  
11:'fluorescentlight'  
12:'cellphonecharger'  
13:'idlehp'  
14:'1threadhp'  
15:'2threadshp'  
16:'3threadshp'  
17:'idlesamsung'  
18:'1threadsamsung'  
19:'2threadssamsung'  
20:'3threadssamsung'  
21:'4threadssamsung'  
22:'videosamsung' 
