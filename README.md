# VideoCC Extractor

A Python-based tool for extracting closed captions from video files. This project allows users to extract subtitles or closed captions embedded in video files using various techniques.

## Features

- Extracts subtitles/closed captions from video files.
- Supports multiple video formats.
- User-friendly interface for selecting video files and extracting captions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/VipulMore11/videocc_extractor.git
    ```
2. Navigate to the project directory:
    ```bash
    cd videocc_extractor
    ```
3. Create a `.env` file in the root directory of the project and add the necessary environment variables:
    ```env
    # .env file

    # Django settings
    SECRET_KEY=your-secret-key
    DEBUG=False

    # AWS settings
    AWS_ACCESS_KEY_ID=your-aws-access-key
    AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
    AWS_STORAGE_BUCKET_NAME=your-bucket-name
    AWS_S3_REGION_NAME=your-region-name

    # Redis and Celery settings
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0

    DYNAMO_TABLE_NAME=your-dynamo-table-name
    ```
   Replace the placeholder values with your actual configuration.

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Redis server** (if not already running):
    ```bash
    redis-server
    ```
    Ensure that Redis is properly installed on your system. You can follow the [official Redis installation guide](https://redis.io/download) if needed.

## Usage

1. Run the application:
    ```bash
    python manage.py runserver
    ```
2. Access the application through your web browser at `http://localhost:8000`.
3. Follow the on-screen instructions to upload video files and extract captions.

## Technologies Used

- Python
- Django
- HTML/CSS (for the interface)

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
