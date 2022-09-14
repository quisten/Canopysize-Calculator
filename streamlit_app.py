import streamlit as st
import pandas as pd
import json
from random import randint


# Load Canopy Tables
with open("NLF.json", "r") as fin:
    rec_NLF = json.load(fin)
with open('BrianGermain.json', 'r') as fin:
    rec_Brian = json.load(fin)

J_SVANHOLM = ["Du har sett på muligheten av påsying av en annen warninglabel, for eksempel en SA2 170, dermed slipper HI alt ansvar og sier du trodde det var en rolig skjerm.",
              "Du drømmer fortsatt om linesus og søkkvåte småjenter på landingsfeltet som omfavner deg når du går som den skygoden du er mot pakkeområdet!",
              "Få HI til å signere på et blankt ark.",
              "Dispsøknader gjør seg best på seddler.",
              "Søk på grunnlag av at skjermen subber i bakken når du går til hangar og den er litt stor å pakke",
              "Du treng disp på skjerm, kausjonist på boliglån åsså tenkt du å ta ut I3 i samme slengen."]

def adviceNLF(exitWeightKG, numberOfJumps):
    indexFromWeight = int(max(0, exitWeightKG-60)/5)    # Column 
    rowIndex = [x for x in rec_NLF.keys() if int(x)-numberOfJumps > -1][0]

    # Don't ask for more info, just display requirement for all recommendation
    st.subheader("NLF Part 1 | Appendix 100: Regulation of Canopy sizes:")
    for reqKey in rec_NLF[rowIndex].keys():
        stringStart = ""
        if "2" in reqKey:
            st.write("\tLicence: %s and Completion of the Advanced Canopy Course" % reqKey.replace("2", "")) 
        else:
            st.write("\tLicence: %s" % reqKey)
        
        #print("%s %s %s" % (rowIndex, reqKey, indexFromWeight))
        canopySize = rec_NLF[rowIndex][reqKey][indexFromWeight]
        wingLoad = exitWeightKG*2.20462/canopySize
        wingLoad = float("%.2f" % wingLoad)
        st.write("\tMinimum Allowable Canopysize (NLF):", canopySize, "sqft @ WL", wingLoad)
        #st.write("\tMinimum Allowable Canopysize (NLF): %d sqft @ WL %.2f\n" % (canopySize, wingLoad))

def adviceBG(exitWeightKG, numberOfJumps):
    
    st.subheader("Advice From Brian Germain's Downsizing Chart")
    # Early Out
    if numberOfJumps > 499:
        st.write("\tBeyond 500 jumps: Follow Canopy Manufacturer’s Recommendations and Guidence from Instructors")
        return

    IndexX = [110, 121, 132, 143, 154, 165, 176, 187, 198, 209, 220, 232, 243, 254, 265] # Weight In LBS
    rowIndex = [x for x in rec_Brian.keys() if int(x)-numberOfJumps > -1][0]
    columnIndex = [i for i,x in enumerate(IndexX) if x-exitWeightKG*2.20462 > -1][0]

    for reqKey in rec_Brian[rowIndex].keys(): 
        
        canopySize = rec_Brian[rowIndex][reqKey][columnIndex]
        wingLoad = (exitWeightKG*2.20462)/int(canopySize)
        wingLoad = float("%.2f" % wingLoad)

        if reqKey == "Mid":
            #st.write("\tRecommended size is %s sqft @ WL %.2f\n" % (canopySize, wingLoad))
            st.write("\tRecommended size is:", canopySize, "sqft @ WL", wingLoad)
        else:
            #st.write("\tMinimum size is %s sqft @ WL %.2f\n" % (canopySize, wingLoad))
            st.write("\tMinimum size is:", canopySize, "sqft @ WL", wingLoad)

def adviceJS(exitWeight):

    st.subheader("Advice From Joergen Svanholm")
    
    canopySize = randint(67, 92)
    validReason = J_SVANHOLM[randint(0, 5)]
    wingLoad = (exitWeight*2.20462)/int(canopySize)
    
    st.write("\tAnbefalt skjermstørrelse: %d sqft @ WL %.2f" % (canopySize, wingLoad))
    st.write("%s" % validReason)

###########################################################################################
# GUI 
###########################################################################################
st.title("Canopy Lookup Tool")
st.write("What canopy size is recommended for you?")

exitWeight = st.slider('exitWeight [KG]', 40, 150, 100)
numberOfJumps = st.slider('# Jumps', 0, 1001, 200)

if exitWeight > 125:
    st.write("Exit Weight Exceeds 125kg which is the maximum of recommended tables.")
else: 
    adviceNLF(exitWeight, numberOfJumps)
    adviceBG(exitWeight, numberOfJumps)
    adviceJS(exitWeight)   


    #https://uspa.org/canopy-risk-quotient <- really great! 