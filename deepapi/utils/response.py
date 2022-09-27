from flask import jsonify
from PIL import Image

# Data IO and Encoding-Decoding
from io import BytesIO
import base64

def generate_response(request, model):
    response = {'success': False}

    # If this model is not activated/imported
    if model is None:
        response['error'] = str('Please enable this model on the api server.')
        return jsonify(response)

    if request.json.get('file'): # image is stored as name "file"
        try:
            img = Image.open(BytesIO(base64.b64decode(request.json.get('file'))))
            if img.mode != 'RGB':
                img = img.convert('RGB')

            top = request.args.get('top')
            if top is not None:
                top = int(request.args.get('top'))
            if top not in [1, 3, 5, 10]:
                top = 10

            no_prob = request.args.get('no-prob')
            if no_prob is not None:
                no_prob = True if int(no_prob) > 0 else False
            else:
                no_prob = False

            results = model.predict(img, top=top)

            response['predictions'] = []
            for i in range(0, len(results)):
                if no_prob:
                    row = {'label': results[i][1]} # numpy float is not good for json
                else:
                    row = {'label': results[i][1], 'probability': float(results[i][2])} # numpy float is not good for json
                response['predictions'].append(row)
            response['success'] = True

        except Exception as e:
                response['success'] = False
                response['error'] = str(e)
                print(response)
        finally:        
            return jsonify(response)
    else:
        response['error'] = 'no image file'
        return jsonify(response)
