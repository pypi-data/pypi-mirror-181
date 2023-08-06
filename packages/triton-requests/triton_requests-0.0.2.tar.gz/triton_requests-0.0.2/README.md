Python package to interact with Nvidia Triton Server


```python

from triton_requests import TritonEndPoint

tep = TritonEndPoint(model_name="emotion-english-distilroberta-base_onnx_inference", url="localhost:9000")

tep.encode("Harry is really happy after his present")
 
```

Will result a numpy array 

	array([[-1.1953125 , -2.4921875 , -2.8964844 ,  4.9921875 ,  0.35498047, 0.70458984,  1.9570312 ]], dtype=float32)

