# plotlines
Exploring the shapes of stories using indico sentiment analysis APIs. Implements a couple hacks to enable sentiment models to work reasonably well across long context windows
Sentiment analysis is difficult to implement on long stories. This repo implements a couple hacks, to demonstrate how the indico sentiment API can be used to pick up long-range emotional landscape across long stories and movie scripts. We think Kurt Vonnegut would be impressed!

### To install:
Navigate to a good place on your filesystem, then:
`git clone https://github.com/IndicoDataSolutions/plotlines`

If you don't have ipython/Jupyter installed yet, then install it:
`pip install -U ipython`

Launch the notebook server. It will bring up a browser window.
`ipython notebook`

Click on `plotlines.ipynb` and walk through the code. Either use the menu `Cell > Run all` to run everything at once, or use `Shift + Enter` to execute one cell at a time.

Follow the links in the notebook to get an indico API key, install any necessary modules, and find input data (e.g., movie scripts).


