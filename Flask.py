from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api_v1/user/vipState", methods=["POST"])
def vip_state():
  response = {
    "code": 200,
    "message":"success",
    "data":{
      "time": "17256268713585",
      "state": "true",
      "hex": "c7114d9bbe8ed19c1d"
    }
  }
  return jsonify(response)

@app.route("/api_v1/user/getUserId",methods=["GET"])
def get_user_id():
  response = {
    "code": 200,
    "message": "Success",
    "data": {
      "uid": 17,
      "userName": "jiuliaj@qq.com",
      "passWord": None,
      "registrationTime": "2024-08-05T20:19:56"
    }
  }
  return jsonify(response)

if __name__ == "__main__":
  app.run(debug=True,host="0.0.0.0", port=9080)