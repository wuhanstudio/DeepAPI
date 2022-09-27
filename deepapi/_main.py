import argparse
from flask import Flask, request, send_from_directory

from deepapi.utils import generate_response

m_vgg16_cifar10     = None
m_vgg16             = None
m_resnet50          = None
m_inceptionv3       = None

app = Flask(__name__)

# Serve the front-end
@app.route("/")
def index():
    return send_from_directory('static', "index.html")

@app.route('/<path:path>')
def send_website(path):
    print(path)
    return send_from_directory('static', path)

@app.route('/vgg16_cifar10', methods=['GET', 'POST'])
def vgg16cifar10():
    global m_vgg16_cifar10
    response = {'success': False}

    if request.method == 'POST':
        return generate_response(request, m_vgg16_cifar10)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

@app.route('/vgg16', methods=['GET', 'POST'])
def vgg16():
    global m_vgg16
    if request.method == 'POST':
        return generate_response(request, m_vgg16)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

@app.route('/resnet50', methods=['GET', 'POST'])
def resnet50():
    global m_resnet50
    if request.method == 'POST':
        return generate_response(request, m_resnet50)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

@app.route('/inceptionv3', methods=['GET', 'POST'])
def inceptionv3():
    global m_inceptionv3
    if request.method == 'POST':
        return generate_response(request, m_inceptionv3)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

def main_cli():

    parser = argparse.ArgumentParser(description='DeepAPI Application')
    
    # Load each model
    parser.add_argument('--vgg16_cifar10', dest='vgg16_cifar10', action='store_true', help='Enable VGG16 model pre-trained on CIFAR10.')
    parser.add_argument('--vgg16_imagenet', dest='vgg16_imagenet', action='store_true', help='Enable VGG16 model pre-trained on ImageNet.')
    parser.add_argument('--resnet50_imagenet', dest='resnet50_imagenet', action='store_true', help='Enable ResNet50 model pre-trained on ImageNet.')
    parser.add_argument('--inceptionv3_imagenet', dest='inceptionv3_imagenet', action='store_true', help='Enable InceptionV3 model pre-trained on ImageNet.')
    parser.add_argument('--all', dest='all', action='store_true', help='Enable all models.')

    # Only activate VGG16 Cifar10 by default
    parser.set_defaults(vgg16_cifar10=True)
    parser.set_defaults(vgg16_imagenet=False)
    parser.set_defaults(resnet50_imagenet=False)
    parser.set_defaults(inceptionv3_imagenet=False)
    parser.set_defaults(all=True)

    args = parser.parse_args()

    # Import Keras models
    global m_inceptionv3, m_resnet50, m_vgg16, m_vgg16_cifar10

    if args.vgg16_cifar10 or args.all:
        from deepapi.models.vgg16 import VGG16Cifar10, VGG16ImageNet
        m_vgg16_cifar10     = VGG16Cifar10()
    
    if args.vgg16_imagenet or args.all:
        from deepapi.models.vgg16 import VGG16ImageNet
        m_vgg16             = VGG16ImageNet()

    if args.resnet50_imagenet or args.all:
        from deepapi.models.resnet50 import ResNet50ImageNet
        m_resnet50          = ResNet50ImageNet()
        
    if args.inceptionv3_imagenet or args.all:
        from deepapi.models.inceptionv3 import InceptionV3ImageNet
        m_inceptionv3       = InceptionV3ImageNet()

    # no-thread: https://github.com/keras-team/keras/issues/2397#issuecomment-377914683
    # avoid model.predict runs before model initiated
    # To let this run on HEROKU, model.predict should run onece after initialized
    # app.run(host="0.0.0.0", port=8080, threaded=False, debug=True)

    from waitress import serve
    print("Serving on port 8080...")
    serve(app, host="0.0.0.0", port=8080, threads=1)

def main():
    return main_cli()

if __name__ == "__main__":
    main()
