import base64
from io import BytesIO
import json
import requests
import imgcat
from PIL import Image
import numpy as np


URL = "http://localhost:9000/2015-03-31/functions/function/invocations"
URL= "https://nhxz4gljps6hbnkwhx6aegrap40cjxzb.lambda-url.us-east-1.on.aws"

request = {
    "actions": [
        {"command":"navigate","url":"https://erichambro.com"}, 
        {"command":"scroll", "scroll_y":600}
    ]
}

request = {
    "actions": [
        {"command":"navigate","url":"https://example.com"}, 
        {"command":"click", "cursor_x":200, "cursor_y":270}
    ]
}


def main(request):

    response = requests.post(URL, data=json.dumps(request), headers={"Content-Type":"application/json"})
    print(response)
    for r in response.json()['responses']:
        imgcat.imgcat(np.asarray(Image.open(BytesIO(base64.b64decode(r["screen"])))))
        print('----')


if __name__=="__main__":


    main(request)