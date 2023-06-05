# Chat App

This is a Chat App project built with FastAPI and WebSockets.
The chat application is integrated with the OpenAI API for customizing text based on desired tone

## Features

- Real-time messaging using WebSocket
- User connections management
- Broadcasting messages to connected clients
- Customization of messages based on tone provided.(i.e. modifies the message based on what tone is provided)

## Requirements

- Python 3.7 or above

## Installation

1. Clone the repository:

        git clone https://github.com/your-username/chat-app.git

2. Change into the project directory:
 
        cd chat-app

3. Install the dependencies:
        
        pip install -r requirements.txt

## Usage

Start the FastAPI server:

        uvicorn main:app --reload
        
Open your browser and navigate to http://localhost:8000 to access the application.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License

This project is licensed under the GNU License.
