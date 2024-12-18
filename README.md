# Meta Glass

## How to Run

To run the full pipeline, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```



### Usage 1: Full Pipeline for Facebook Live Video

1. Run the script with your Facebook live video link:
    ```bash
    python Full_pipeline.py
    ```

The script will prompt you to enter a Facebook public live video link. Follow the instructions provided by the script to complete the processing.

Example:
```bash
$ python Full_pipeline.py
Enter the Facebook live video link: https://www.facebook.com/username/live/video_id
```

### Usage 2: Fixed Image upload pipeline

1. Run the script for testing with a fixed image:
    ```bash
    python image_upload_pipeline.py
    ```
2. Modify the `image_path` variable based on requirement. By defautl it is using `detected_faces/nm.jpg` image



Example:
```bash
$ python image_upload_pipeline.py
```



