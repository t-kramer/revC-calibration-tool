import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


# STREAMLIT PAGE

# define constants for reference function (average of multiple sensors)
beta_0 = 0.626886771
beta_1 = -1.846669496
intercept = 1.603399326

rvs = np.arange(1.000,1.500,0.005)


# introduction container
intro = st.container()

with intro:
    st.title('Welcome to the revC calibration for climateBOX users!')
    st.image('img/desk.png')
    st.markdown('This page aims to guide you through a simplified calibration process for the revC sensor. \
        Quickly read the explainer below, enter your measured values and leave with the one value you need: the \
        custom **zeroWind adjustment** for your sensor.')


# explainer container
explainer = st.container()

with explainer:
    st.header('Quick explanation')

    explainer_markdown = read_markdown_file('explanation.md')
    st.markdown(explainer_markdown)


# input containter
input = st.container()

with input:
    st.text('Please enter your observed values here.')

    sel_col, disp_col = st.columns(2)

    rv_input = sel_col.number_input(label='Enter your RV value here:',format="%.3f")
    tmp_input = sel_col.number_input(label='Enter your TMP value here:',format="%.3f")



# output container
output = st.container()

with output:


    df = pd.DataFrame({'rv': np.arange(0.900,1.800,0.005)})
    df = df.assign(y = lambda x: (round(beta_0 * x['rv']**3 + beta_1 * tmp_input + intercept, ndigits=3)))

    index = df.iloc[(df['rv']-rv_input).abs().argsort()[:1]].index.item()

    zeroWind = df['y'].iloc[index]

    df['sensor'] = df['y'] - zeroWind


if rv_input and tmp_input:

        # build plot
        fig, ax = plt.subplots()

        ax.scatter(rv_input, 0, color='black', zorder=10)
        ax.scatter(rv_input, 0 + zeroWind, color='black', zorder=10)

        ax.plot((rv_input, rv_input),(0, 0 + zeroWind), color='red')
        ax.plot(df['rv'], df['y'], color='silver', linestyle='--')
        ax.plot(df['rv'], df['sensor'], color='black')

        ax.set_ylim(-0.5,1.2)

        ax.set_xlabel('Raw RV value [-]')
        ax.set_ylabel('Air velocity [m/s]')

        labels = ['zeroWind adjustment','Reference function','Sensor (approx.)']

        plt.legend(labels=labels, frameon=False)

        # show plot
        st.pyplot(fig)

        # output zeroWind adjustment
        st.write(f"Your zeroWind adjustment is: {-zeroWind:.2f} m/s")

# conclusion container
goodbye = st.container()

with goodbye:

    if rv_input and tmp_input:

        st.markdown('Now that you have the sensor specific zeroWind adjustment, you need to change  \
            this variable the climateBOX code (see image below).')

        st.image('img/code.png')

        st.markdown('For any questions, feel free to visit the **climateBOX GitHub page** [LINK].\
            Thanks for using this tool!')

        st.markdown('For more context on this tool we would like to refer you to our recent publication:')

        st.markdown('Kramer, T., Garcia-Hansen, V., & Omrani, S. (2023). climateBOX: a low-cost and open-source monitoring device\
                 for personal thermal comfort evaluation. Energy and Buildings, 112830. https://doi.org/https://doi.org/10.1016/j.enbuild.2023.112830')