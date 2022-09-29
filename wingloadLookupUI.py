from re import X
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from random import randint
import matplotlib.pyplot as plt

colors = {'Norway':'lightsteelblue', 'Sweden':'olive', 'British':'indianred', 'French':'darkorange', 'Brian_Germain': 'teal'} #https://matplotlib.org/stable/gallery/color/named_colors.html    
alpha_solid = [.5, .2, .2]
alpha_dotted = [.8, .3, .3]


tab_font_css = """
            <style>
            button[data-baseweb="tab"] {
            font-size: 18px;
            }
            </style>
            """
hvar = """  <script>
                    var elements = window.parent.document.querySelectorAll('.streamlit-expanderHeader');
                    var arrayLength = elements.length;
                    for (var i =0 ; i< arrayLength; i++) {
                        elements[i].style.color = 'rgba(183, 56, 68, 1)';
                        elements[i].style.fontSize = 'large';
                        elements[i].style.fontWeight = 'normal'; 
                    }
            </script>"""
font2_css = """
            <style>
            button[data-baseweb="tab"] {
            font-size: 12px;
            }
            </style>
            """

def applyCSS():
    st.markdown("""    
    <style>
    button[data-baseweb="tab"] {
    font-size: 18px;
    }
    </style>
    
    <script>
            var elements = window.parent.document.querySelectorAll('.streamlit-expanderHeader');
            elements[0].style.color = 'rgba(183, 36, 68, 1)';
            /*elements[0].style.fontFamily = 'Didot';*/
            elements[0].style.fontSize = 18px; /*'large';*/
            elements[0].style.fontWeight = 'normal';
    </script>


    <style>
    .stTextInput > label {
    font-size:120%;
    font-weight:bold;
    color:white;
    background:linear-gradient(to bottom, #3399ff 0%,#00ffff 100%);
    border: 2px;
    border-radius: 3px;
    }

    [data-baseweb="base-input"]{
    background:linear-gradient(to bottom, #3399ff 0%,#00ffff 100%);
    border: 2px;
    border-radius: 3px;
    }

    input[class]{
    font-weight: bold;
    font-size:120%;
    color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def renderAdvice(options, loadedTables, loadedIndices, numberOfJumps, exitWeight):
    
    #show_min3 = st.checkbox("Show Minimum Accepted Size", True)
    
    # Make Data Frame
    listOfWL = list()
    for i, option in enumerate(options):
        
        if exitWeight > loadedIndices[i][-1]:
            continue
        if numberOfJumps > int(list(loadedTables[i].keys())[-1]):
            continue

        rowIndex = [x for x in loadedTables[i].keys() if int(x)-numberOfJumps > -1][0]
        columnIndex = [i for i,x in enumerate(loadedIndices[i]) if x-exitWeight > -1][0]

        for reqKey in loadedTables[i][rowIndex].keys():
            canopySize = loadedTables[i][rowIndex][reqKey][columnIndex]
            wingLoad = (exitWeight*2.20462)/int(canopySize)
            wingLoad = float("%.2f" % wingLoad)

            wlEntry = list()
            wlEntry.append(option)
            wlEntry.append(reqKey)
            wlEntry.append(int(canopySize))
            wlEntry.append(wingLoad)
            listOfWL.append(wlEntry) 

    df = pd.DataFrame(listOfWL, columns=['Instance', 'Type', 'CanopySize', 'WL'])
    

    # RegBody | Category | Size | WL
    with st.expander("Lookup", expanded=True):
        df.style.set_properties(subset=['CanopySize'], **{'width': '300px'})
        st.dataframe(data=df)
        
        
    #df.CanopySize = int(df.CanopySize.replace(' ', ''))
    with st.expander("Statistics", expanded=True):
        st.write(df.describe())
    
    with st.expander("Advice from Jørgen Svanholm", expanded=True):
        
        # Add Jorgen
        if True:
            J_SVANHOLM = ["Du har sett på muligheten av påsying av en annen warninglabel, for eksempel en SA2 170, dermed slipper HI alt ansvar og sier du trodde det var en rolig skjerm.",
                    "Du drømmer fortsatt om linesus og søkkvåte småjenter på landingsfeltet som omfavner deg når du går som den skygoden du er mot pakkeområdet!",
                    "Få HI til å signere på et blankt ark.",
                    "Dispsøknader gjør seg best på seddler.",
                    "Søk på grunnlag av at skjermen subber i bakken når du går til hangar og den er litt stor å pakke",
                    "Du treng disp på skjerm, kausjonist på boliglån åsså tenkt du å ta ut I3 i samme slengen."]
                
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
        
        with st.expander(option, expanded=False): #st.subheader(option)
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

def renderCurrency(exitWeight, numberOfJumps):

    canopySize = st.slider("Current CanopySize", 69, 210, 150)
    jumpsOnCurrentSize = st.slider("# Jumps on current Canopy", 0, 500, 50)
    jumpsLast6m = st.slider("#Jumps last 6m", 0, 1000, 50)

    currentWL = exitWeight*2.20462/canopySize

    wlMax = 2.8
    wlExp = currentWL+jumpsLast6m*0.001
    wlWeight = 0.9+(numberOfJumps+jumpsLast6m)*0.0007
    wlWhat = currentWL+0.25 # If you are conservative

    recWL =min(wlMax, wlExp, wlWhat, wlWeight)

    st.write("Recommended SIze for you is:", recWL, "size", int((exitWeight*2.20462)/recWL), "sqft")
    st.write("wlMax", wlMax)
    st.write("wlExp", wlExp)
    st.write("wlWeight", wlWeight)
    st.write("wlWhat", wlWhat)

def main():

    applyCSS()
    # Header
    st.title("Wingload Lookup Tool")
    st.write("What canopy size is recommended for you?")
        

    #st.write(tab_font_css, unsafe_allow_html=True)
    with st.expander("Set Input Data", expanded=True):
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
        exitWeight = st.slider('Select exitWeight [KG]', 40, 150, 100)
        numberOfJumps = st.slider('Select # Jumps', 0, 2001, 200)

    #tab1, tab2, tab3, tab4, tab5 = st.tabs(["Recommendation Lookup", "Wingload By # Jumps", "Wingload By exitWeight", "Data Tables", "Based on Currency"])
    tab1, tab2, tab3, tab4 = st.tabs(["Table Lookups", "Wingload By # Jumps", "Wingload By exitWeight", "Data Tables"])

    with tab1:
        renderAdvice(options, wingSizeTables, wingSizeIndices, numberOfJumps, exitWeight)

    with tab2:
        renderWingloadByWeight(options, wingSizeTables, wingSizeIndices, exitWeight) 

    with tab3:
        renderWingloadByJumps(options, wingSizeTables, wingSizeIndices, numberOfJumps, exitWeight)
    
    with tab4:
        renderDataTables(options, wingSizeTables, wingSizeIndices)
 
    components.html(hvar, height=0, width=0)
    st.write("By Ebbe Smith of Norway 2022")

    return True
if __name__ == "__main__":
    st.set_page_config(
        "Wingload Lookup Tool By Ebbe Smith",
        "📊",
        initial_sidebar_state="expanded",
        #layout="wide",
    )
    main()