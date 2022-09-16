from re import X
import streamlit as st
import pandas as pd
import json
from random import randint
import matplotlib.pyplot as plt

colors = {'Norway':'lightsteelblue', 'Sweden':'olive', 'British':'indianred', 'French':'darkorange', 'Brian_Germain': 'teal'} #https://matplotlib.org/stable/gallery/color/named_colors.html    
alpha_solid = [.5, .2, .2]
alpha_dotted = [.8, .3, .3]

def renderAdvice(options, loadedTables, loadedIndices, numberOfJumps, exitWeight):
    
    for i, option in enumerate(options):
        st.subheader("%s" % option)
        
        if exitWeight > loadedIndices[i][-1]:
            st.write("Weight exceeds table.")
            continue
        if numberOfJumps > int(list(loadedTables[i].keys())[-1]):
            st.write("Jumps exceeds table.") 
            continue

        rowIndex = [x for x in loadedTables[i].keys() if int(x)-numberOfJumps > -1][0]
        columnIndex = [i for i,x in enumerate(loadedIndices[i]) if x-exitWeight > -1][0]

        for reqKey in loadedTables[i][rowIndex].keys():
            canopySize = loadedTables[i][rowIndex][reqKey][columnIndex]
            wingLoad = (exitWeight*2.20462)/int(canopySize)
            wingLoad = float("%.2f" % wingLoad)
            st.write("Requirement -", reqKey, "- can fly: " ,canopySize, "sqft @ WL", wingLoad)
        
    # Add Jorgen
    if True:
        J_SVANHOLM = ["Du har sett på muligheten av påsying av en annen warninglabel, for eksempel en SA2 170, dermed slipper HI alt ansvar og sier du trodde det var en rolig skjerm.",
                "Du drømmer fortsatt om linesus og søkkvåte småjenter på landingsfeltet som omfavner deg når du går som den skygoden du er mot pakkeområdet!",
                "Få HI til å signere på et blankt ark.",
                "Dispsøknader gjør seg best på seddler.",
                "Søk på grunnlag av at skjermen subber i bakken når du går til hangar og den er litt stor å pakke",
                "Du treng disp på skjerm, kausjonist på boliglån åsså tenkt du å ta ut I3 i samme slengen."]
        st.subheader("Advice From Joergen Svanholm")
            
        canopySize = randint(67, 92)
        validReason = J_SVANHOLM[randint(0, 5)]
        wingLoad = (exitWeight*2.20462)/int(canopySize)
        wingLoad = float("%.2f" % wingLoad)
        st.write("\tAnbefalt skjermstørrelse:", canopySize, "sqft @ WL", wingLoad)
        st.write("Kommentar: %s" % validReason)

    return True

def renderWingloadByWeight(options, loadedTables, loadedIndices, exitWeight):

    show_min = st.checkbox("Show Minimum Accepted Size", True)
    show_max = st.checkbox("Show Recommended Size", True)
    show_exitWeight = st.checkbox("Show +/- 10kg Effects")

    fig, ax = plt.subplots()  # plt.subplots(figsize=(14, 7))
    weights = [exitWeight]
    if show_exitWeight:
        weights.append(exitWeight+10)
        weights.append(exitWeight-10)

    for k, exitWeight in enumerate(weights):
        for i, option in enumerate(options):
            try:
                columnIndex = [i for i,x in enumerate(loadedIndices[i]) if x-exitWeight > -1][0]
            except:
                continue
            
            xData = list()
            yData = {"max":[], "min":[]}
        
            for jumpKey in loadedTables[i].keys():
                canopySizeMax = max([loadedTables[i][jumpKey][reqKey][columnIndex] for reqKey in loadedTables[i][jumpKey].keys()])
                canopySizeMin = min([loadedTables[i][jumpKey][reqKey][columnIndex] for reqKey in loadedTables[i][jumpKey].keys()])
                yData["max"].append(exitWeight*2.20462/max(50,int(canopySizeMax)))    
                yData["min"].append(exitWeight*2.20462/max(50,int(canopySizeMin))) 
                xData.append(int(jumpKey))            
            
            label_max = option+"_Recommended"
            label_min = option+"_Minimum"
            if k!=0: label_max = label_min = None

            if show_max:
                ax.plot(xData, yData['max'], label=label_max, linewidth=1.2, alpha=alpha_solid[k], color=colors[option])
            if yData['max'] != yData['min'] and show_min:
                ax.plot(xData, yData['min'], label=label_min, linestyle="dotted", linewidth=1.2, alpha=alpha_dotted[k], color=colors[option])
    
    ax.grid(True, alpha=0.2)
    ax.set_title("Allowed Wingload for %d kilos exitWeight and X jumps" % exitWeight)
    ax.set_xlabel("Number of Jumps [#]")
    ax.set_ylabel("WingLoad [lbs/sqft]")
    plt.legend(loc="upper left", fontsize=6)
    st.pyplot(fig)

    return True

def renderWingloadByJumps(options, loadedTables, loadedIndices, numberOfJumps, exitWeight):

    show_min2 = st.checkbox("Show Minimum Accepted Size:", True)
    show_max2 = st.checkbox("Show Recommended Size:", True)
    #show_exitWeight = st.checkbox("Show +/- 10kg Effects")

    fig, ax = plt.subplots()  # plt.subplots(figsize=(14, 7))


    for i, option in enumerate(options):
        try:
            columnIndex = [i for i,x in enumerate(loadedIndices[i]) if x-exitWeight > -1][0]
            jumpKey = [x for x in loadedTables[i].keys() if int(x)-numberOfJumps > -1][0]
        
        except:
            continue
        
        xData = list()
        yData = {"max":[], "min":[]}
    
        #for jumpKey in loadedTables[i].keys():
        #st.write(loadedIndices[i])
        for columnIndex, exitWeight2 in enumerate(loadedIndices[i]):
            
            canopySizeMax = max([loadedTables[i][jumpKey][reqKey][columnIndex] for reqKey in loadedTables[i][jumpKey].keys()])
            canopySizeMin = min([loadedTables[i][jumpKey][reqKey][columnIndex] for reqKey in loadedTables[i][jumpKey].keys()])
            yData["max"].append(exitWeight2*2.20462/max(50,int(canopySizeMax)))    
            yData["min"].append(exitWeight2*2.20462/max(50,int(canopySizeMin))) 
            #xData.append(int(jumpKey))            
            xData.append(exitWeight2)
            #yData[""]

        label_max = option+"_Recommended"
        label_min = option+"_Minimum"


        if show_max2:
            ax.plot(xData, yData['max'], label=label_max, linewidth=1.2, alpha=alpha_solid[0], color=colors[option])
        if yData['max'] != yData['min'] and show_min2:
            ax.plot(xData, yData['min'], label=label_min, linestyle="dotted", linewidth=1.2, alpha=alpha_dotted[0], color=colors[option])

    ax.grid(True, alpha=0.2)
    ax.set_title("Allowed Wingload for %d jumps and X kilos" % numberOfJumps)
    ax.set_xlabel("ExitWeight [kg]")
    ax.set_ylabel("WingLoad [lbs/sqft]")
    plt.legend(loc="upper left", fontsize=6)
    st.pyplot(fig)

    return True

def renderDataTables(options, loadedTables, loadedIndices):

    # Convert To Dataframe | Horrible horrible code! sorry mom!
    dfs = list() 
    for i, option in enumerate(options): 
        st.subheader(option)
        df = pd.DataFrame()#columns=loadedIndices[i])
        
        data = dict()
        df = pd.DataFrame(data, index=loadedTables[i].keys())#columns=loadedIndices[i])
       
        for k, indices in enumerate(loadedIndices[i]):
            data[loadedIndices[i][k]] = list()

        realIndex = list()
        #st.write(len(loadedTables[i]), len(loadedIndices[i]))
        for jumpKey in loadedTables[i].keys():
            for req in loadedTables[i][jumpKey].keys():
                for k, values in enumerate(loadedTables[i][jumpKey][req]):
                    try:
                        data[loadedIndices[i][k]].append(loadedTables[i][jumpKey][req][k])
                    except:
                        pass
                realIndex.append(jumpKey+'  '+req)
                
        df = pd.DataFrame(data, index=realIndex)#, index=loadedTables[i].keys())#columns=loadedIndices[i])
        st.table(df)
        
def main():

    # Header
    st.title("Wingload Lookup Tool")
    st.write("What canopy size is recommended for you?")
    st.write("This app only looks up regulations regarding canopysizes and does not take into account planforms and other regulations.")
    
    # Select Governing Bodies and Load Tables
    options = st.multiselect('Regulations and Recommendation to Look up?',
    ['Norway', 'Sweden', 'French', 'British', 'Brian_Germain'],
    ['Norway', 'Sweden', 'French', 'British', 'Brian_Germain'])

    wingSizeTables, wingSizeIndices = list(), list()
    for option in options:
        with open("Tables/%s_Table.json" % option, "r") as fin:
            wingSizeTables.append(json.load(fin))
        with open("Tables/%s_Index.json" % option, "r") as fin:
                wingSizeIndices.append(json.load(fin))

    # Sliders & Tabs ! 
    exitWeight = st.slider('exitWeight [KG]', 40, 150, 100)
    numberOfJumps = st.slider('# Jumps', 0, 1001, 200)
    tab1, tab2, tab3, tab4 = st.tabs(["Advice", "Wingload By # Jumps", "Wingload By exitWeight", "Data Tables"])

    with tab1:
        renderAdvice(options, wingSizeTables, wingSizeIndices, numberOfJumps, exitWeight)

    with tab2:
        renderWingloadByWeight(options, wingSizeTables, wingSizeIndices, exitWeight) 

    with tab3:
        renderWingloadByJumps(options, wingSizeTables, wingSizeIndices, numberOfJumps, exitWeight)
    
    with tab4:
        renderDataTables(options, wingSizeTables, wingSizeIndices)

    return True
if __name__ == "__main__":
    st.set_page_config(
        "Wingload Analyser By Ebbe Smith",
        "📊",
        initial_sidebar_state="expanded",
        #layout="wide",
    )
    main()