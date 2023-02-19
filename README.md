# learning-engine

<center><b>If you encounter any problem, please leave a message in the slack channel of learning-engine.</b></center>

# Environment Setup 
Fast API (web framework): https://fastapi.tiangolo.com/tutorial/

Tesseract (pdf read): https://tesseract-ocr.github.io/tessdoc/Installation.html

Questgen AI (ai generation): https://github.com/ramsrigouthamg/Questgen.ai

Leaf (ai generation, not yet implemented):https://github.com/KristiyanVachev/Leaf-Question-Generation

and all the packages/libs that the current files depend on.

## Requirements
Python 3.7+ 

## Running and Accessing The Server

Main Command:
```
uvicorn server.controller.request_handler:app --reload
```

or run ```request_handler.py``` at ```server/controller/request_handler.py```


You can access your server in your browser, by opening: ```http://127.0.0.1:8000```

You can download [Postman](https://www.postman.com/) for easier GET and POST request testing

