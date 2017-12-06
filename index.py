from flask import Flask, jsonify, request, render_template
from flask import make_response, abort


app = Flask(__name__)

# infos 应该为从数据库读取的json数据，这里暂时先用list代替
infos = [
    {
        "id": 0,
        "title": "flask",
        "content": "flask test content 0"
    },
    {
        "id": 1,
        "title": "flask",
        "content": "flask test content 1"
    },
    {
        "id": 2,
        "title": "flask",
        "content": "flask test content 2"
    }
]

@app.route('/')
def index():
    return render_template("vue.html")

@app.route('/api/v1.0/info/', methods=['GET'])
def getInfos():
    return jsonify({"infos":infos})

# 未发现处理
@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.route('/api/v1.0/info/<int:id>', methods=['GET'])
def getInfo(id):
    info = list(filter(lambda t: t['id'] == id, infos))
    if len(info) == 0:
        abort(404)

    return jsonify({"info": infos[0]})

@app.route('/api/v1.0/info', methods=["POST"])
def ceratInfo():
    if not request.json or not 'title' in request.json:
        abort(400)
    info = {
        "id": infos[-1]['id'] + 1,
        "title": request.json["title"],
        "content": request.json.get("content", "")
    }
    infos.append(info)
    return jsonify({"info": info}), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)