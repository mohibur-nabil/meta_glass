from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import io
import uvicorn
import os
import image_upload_pipeline
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAVE_DIRECTORY = "saved_images"

# Ensure the directory exists
os.makedirs(SAVE_DIRECTORY, exist_ok=True)


def process_image(image: Image.Image) -> str:
    # Generate a unique filename
    filename = "nm.jpg"
    file_path = os.path.join(SAVE_DIRECTORY, filename)
    image.save(file_path)

    summary = image_upload_pipeline.main()

    if summary:
        return summary+'\nthank you for using our service'
    else:
        return "No summary generated." 


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read the image file
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Process the image and generate text output
        result_text = process_image(image)

        return JSONResponse(content={"result": result_text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
