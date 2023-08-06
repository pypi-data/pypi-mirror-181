# Fourier Analysis

This works nicely for sine waves. The series output was tested with plotly's line plot but can be used with any plotting library. It should output a new series (in list of floats format) with maximums corresponding to the frequency (highly accurate) and amplitude (usually 90%+ accurate) of the input series.

## Usage

Expected input: a path with a file of csv with one row only of floats.
Output: 

```python3
import fourier_sine
series = fourier_sine.create_random_series()
output = fourier_sine.fourier_analysis(series)
```

For inspection you can also:

```python3
import plotly
plotly.plot(series, kind='line', title='input').show()
plotly.plot(output, kind='line', title='output').show()
```

Input series composed of three sine waves:
frequency 95 amplitude 967, frequency 140 amplitude 731, frequency 170 amplitude 53

![Input wave](wave_to_decompose.png "input wave series")

![Output graph](fourier_output.png "output series")

Notice that the amplitude of the first two waves listed, 967 and 731, respectively reflect the frequency of 95 an 140. Unfortunately, for this example, the amplitude of 53 is too small to detect visually from this graph at the 170 frequency.

Credits: Andrew Matte and Bob Matte, implemented after watching the youtube video [The Algorithm That Transformed The World on the Veritasium channel](https://www.youtube.com/watch?v=nmgFG7PUHfo).