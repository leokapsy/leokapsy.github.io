from email.mime import image
import os
import cv2
from PIL import Image
from flask import Flask, render_template, request, abort, send_from_directory


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["DOWNLOAD_FOLDER"] = "downloads"




@app.route("/")
def homepage():
        
          
        return render_template("index.html")


@app.route('/process', methods=['POST'])
def process():
     if request.method == "POST":
        # Get the uploaded image file
        image = request.files["image"]

        # Save the image to a temporary file
        image_path = "static/uploads/input.png"
        image.save(image_path)

        # Remove the background
        remove_background(image_path)

        # Return the processed image
        return render_template("index.html", image="output.png")
     
def remove_background(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert the image to RGBA mode
    image = image.convert("RGBA")

    # Get the image data
    data = image.getdata()

    new_data = []
    for item in data:
        
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], "output.png")
    image.save(output_path, "PNG")


@app.route("/download")
def download():
    # Serve the processed image for download
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], "output.png")
    return send_from_directory(app.config["UPLOAD_FOLDER"], "output.png", as_attachment=True)

@app.route("/about")
def about():
    return render_template('about.html')


    
    




   
       
      


    
                       
if __name__ == "__main__":
    app.run(debug=True)