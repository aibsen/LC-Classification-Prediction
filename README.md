# LC-Classification-Prediction

<p>
This repository contains a pipeline to download, preprocess and classify data from the Catalina-Real Time Transient Survey (http://crts.caltech.edu/)
The code is written using Python3.6.4 
</p>

<p>
In order to locally run the whole pipeline:
</p>

<pre>
  <code>
    virtualenv path/to/virtualenv
    source path/to/virtualenv/bin/activate
    pip install -r requirements.txt
    python classify_crts_data.py ClassifyCRTSData --local-scheduler
  </code>
</pre>
