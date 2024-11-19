import pickle
# we are going to use the Flask micro web framework
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_model():
    infile = open("tree.p", "rb")
    header, tree = pickle.load(infile)
    infile.close()
    return header, tree

def tdidt_predict(header, tree, instance):
    info_type = tree[0]
    if info_type == "Leaf":
        return tree[1] # label
    att_index = header.index(tree[1])
    for i in range(2, len(tree)):
        value_list = tree[i]
        if value_list[1] == instance[att_index]:
            return tdidt_predict(header, value_list[2], instance)
        
# we need to add some routes
# a route is a function that handles a request
# ex. for the HTML content for a home page
# ex. for the JSON response for a /predict API endpoint etc.

@app.route("/")
def index():
    # return content and status code
    return "<h1>Welcome to the interview predictor app</h1>", 200

# let's add a route for the predict endpoint
@app.route("/predict")
def predict():
    # let's parse the unseen instance values from the query string they are in the request object
    level = request.args.get("level") # defaults to None
    lang = request.args.get("lang")
    tweets = request.args.get("tweets")
    phd = request.args.get("phd")
    instance = [level, lang, tweets, phd]
    # load pickled tree
    header, model = load_model()
    # make the prediction
    prediction = tdidt_predict(header, model, instance)
    if prediction is not None:
        return jsonify({"prediction": prediction}), 200
    return "Error making a prediction", 400
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
    # TODO: when deploy app to "production" set debug=False and check host and port values
