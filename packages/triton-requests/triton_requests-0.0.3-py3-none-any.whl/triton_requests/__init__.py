# Requirement : 
# pip install tritonclient[http]

import tritonclient.http
import numpy as np
from tritonclient.http import InferInput


class TritonEndPoint:

    def __init__(self, model_name, model_version="1", url="localhost:9000"):
        self.url = url
        self.model_name = model_name
        self.model_version = model_version
        self.triton_client = tritonclient.http.InferenceServerClient(url=self.url, verbose=False)
        assert self.triton_client.is_model_ready(model_name=model_name,
                                                 model_version=model_version), f"model {model_name} not yet ready"
        self.model_metadata = self.triton_client.get_model_metadata(model_name=model_name, model_version=model_version)
        self.model_config = self.triton_client.get_model_config(model_name=model_name, model_version=model_version)
        self.model_score = tritonclient.http.InferRequestedOutput(name="output", binary_data=False)

    def encode(self, text, batch_size=1):
        query: InferInput = tritonclient.http.InferInput(name="TEXT", shape=(batch_size,), datatype="BYTES")
        query.set_data_from_numpy(np.asarray([text] * batch_size, dtype=object))
        response = self.triton_client.infer(model_name=self.model_name,
                                            model_version=self.model_version,
                                            inputs=[query],
                                            outputs=[self.model_score])
        return response.as_numpy("output")

    def qa(self, question, context):
        question = tritonclient.http.InferInput(name="QUESTION", shape=(1,), datatype="BYTES")
        question.set_data_from_numpy(np.asarray([question], dtype=object))
        context = tritonclient.http.InferInput(name="CONTEXT", shape=(1,), datatype="BYTES")
        context.set_data_from_numpy(np.asarray([context], dtype=object))
        response = self.triton_client.infer(model_name=self.model_name,
                                            model_version=self.model_version,
                                            inputs=[question, context],
                                            outputs=[self.model_score])
        return response.as_numpy("output")
