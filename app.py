from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/single_view')
def single_view():
    return render_template('single_view.html')

@app.route('/comparison_view')
def comparison_view():
    return render_template('comparison_view.html')

# Endpoint to retrieve single model animation based on user selection
@app.route('/get_single_animation', methods=['POST'])
def get_single_animation():
    data = request.json
    initialization = data['initialization']
    feature = data['feature']
    block = data['block']
    epoch_or_batch = data['epoch_or_batch']
    mode = data['mode']
    layer = data['layer']

    # Construct the file path for the requested animation
    if mode == 'all_epochs':
        animation_path = f'static/animations/{initialization}/combined_animations/{feature}_block_{block}_{layer}_combined.gif'
        # animation_path = 'static/animations/output_xavier/combined_animations/activations_heatmap_block_3_attention_combined.gif'
    else:
        animation_path = f'static/animations/{initialization}/{feature}_block_{block}_{layer}_epoch_epoch_{epoch_or_batch}.gif'

    return jsonify({'animation_url': animation_path})

# Endpoint to retrieve comparison animations based on user selection
@app.route('/get_comparison_animation', methods=['GET'])
def get_comparison_animation():

    # print(request.json)
    # data = request.json
    data= request.args
    # print(data)
    initialization_1 = data.get('initialization1')
    initialization_2 = data.get('initialization2')
    feature = data.get('feature')
    block = data.get('block')
    epoch_or_batch = data.get('epoch_or_batch')
    mode = data.get('mode')
    layer = data.get('layer')
    # print("i am here")
    if mode == 'all_epochs':
        animation_url_1 = f'static/animations/{initialization_1}/combined_animations/{feature}_block_{block}_{layer}_combined.gif'
        animation_url_2 = f'static/animations/{initialization_2}/combined_animations/{feature}_block_{block}_{layer}_combined.gif'
        # animation_url_1= "static/animations/output_xavier/combined_animations/activations_heatmap_block_3_attention_combined.gif"
        # animation_url_2= "static/animations/output_xavier/combined_animations/activations_heatmap_block_3_attention_combined.gif"
    else:
        animation_url_1 = f'static/animations/{initialization_1}/{feature}_block_{block}_{layer}_epoch_epoch_{epoch_or_batch}.gif'
        animation_url_2 = f'static/animations/{initialization_2}/{feature}_block_{block}_{layer}_epoch_epoch_{epoch_or_batch}.gif'
    print("finally")
    return jsonify({'animation_url_1': animation_url_1, 'animation_url_2': animation_url_2})

if __name__ == '__main__':
    app.run(debug=True)
