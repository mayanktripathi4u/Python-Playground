from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    print("This function being called.")
    return {
        "status": 1,
        "class": "success",
        "message": "Welcome to Money COntrol APP",
        "payload": {},
    }

# @app.route("/en/<versionNumber>/<topicName>")
# def doc(versionNumber, topicName):
#     return {
#         "status": 1,
#         "class": "success",
#         "message": "Success",
#         "payload": {
#             "versionNumber": versionNumber,
#             "topicName": topicName,
#         },
#     }


@app.route("/en/<versionNumber>/<topicName>", methods=["GET", "POST"])
def doc(versionNumber, topicName):
    if request.method == "POST":
        print("request.method: ", request.method)
        print("request.form: ", request.form)
        print("request.values: ", request.values)
        print("request.json: ", request.json)

        # Access JSON Data
        json_data = request.json
        print("json_data: ", json_data)
        print("json_data -- name: ", json_data["name"])
        print("json_data -- age: ", json_data["age"])

        # if "hobbies" in json_data:
        #     print("Hobbies : ", json_data["hobbies"])
        # else:
        #     print("Hobbies : No Hobbies")

        # Alternate of above if...else..
        print("hobbies : ", json_data.get("hobbies", "No Hobbies") )

        return {
            "status": 1,
            "class": "success",
            "message": "POST Success",
            "payload": {
                "method": request.method
            },
        }
    
    return {
        "status": 1,
        "class": "success",
        "message": "GET Success",
        "payload": {
            "versionNumber": versionNumber,
            "topicName": topicName,
        },
    }


@app.route("/form_doc/en/<versionNumber>/<topicName>", methods=["GET", "POST"])
def form_doc(versionNumber, topicName):
    if request.method == "POST":
        print("request.method: ", request.method)
        print("request.form: ", request.form)
        print("request.values: ", request.values)
        print("request.json: ", request.json)

        formData =request.form
        print("formData : ", formData)
        print(f"Name with Get Method : {formData.get("name")}")
        print(f"Name with square brackets : {formData["name"]}")
        print(f"Age with Get Method : {formData.get("age", "No Age")}")
        print(f"Random with Get Method : {formData.get("random", "No Random")}")

        return {
            "status": 1,
            "class": "success",
            "message": "POST Success",
            "payload": {
                "method": request.method
            },
        }
    
    return {
        "status": 1,
        "class": "success",
        "message": "GET Success",
        "payload": {
            "versionNumber": versionNumber,
            "topicName": topicName,
        },
    }


if __name__ == "__main__":
    # app.run(debug = True)
    app.run(debug=True, port=5001)
    # app.run(debug=True, host='0.0.0.0')

 