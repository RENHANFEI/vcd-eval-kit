# VCD Eval Kit

This is an image quality assessment experiment for <b><i>Vision Correcting Displays</i></b>.

1. Coded with Python3, not sure if it can work well with Python2
2. Install required package: `pip install Image`
3. Enter the eval_kit directory: `cd path/to/eval_kit`
4. Run the test: `python evaluate.py`
5. Compelete the test and you will see a .csv file under eval_kit, named after completion time stamp.
6. The logic of csv entries: a_image_index, a_window_function, a_aperture, a_degree, b_image_index, b_window_function, b_aperture, b_degree, rating. Rating means (b) is `{-3: 'Much worse', -2: 'Worse', -1: 'Slightly worse', 0: 'The same', 1: 'Slightly better', 2: 'Better', 3: 'Much better'}` than (a).