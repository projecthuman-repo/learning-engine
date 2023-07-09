# learning-engine

<center><b>If you encounter any problem, please leave a message in the slack channel of learning-engine.</b></center>

# Environment Setup 

Flask(web framework): https://flask.palletsprojects.com/en/2.3.x/quickstart/

PyDictionary: https://pypi.org/project/PyDictionary/

language_tool_python: https://github.com/jxmorris12/language_tool_python


Poppler (pdf read): 
  - https://poppler.freedesktop.org/
  - (**Windows**) https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows

Tesseract (pdf read): https://tesseract-ocr.github.io/tessdoc/Installation.html

Academic Paper PDF files: phc google drive or use your own pdf papers.

Questgen AI (ai generation): https://github.com/ramsrigouthamg/Questgen.ai

LeafAI (ai generation, implemented, but see next section for further instruction):https://github.com/KristiyanVachev/Leaf-Question-Generation

and all the packages/libs that the current files depend on.

### Environment Setup issues and tricks
1. ml_models of LeafAI and tar.gz files: 
LeafAI and Questgen models requires the "reddit tar.gz" file and other model related files which were too big and those needed to be placed in .gitignore.

2. server_constants: 
Due to our lack of experience, its currently a mess to align all the PATH variables in a general fashion, try to adjust on your own and place the server_constants.py file in .gitignore as well.

3. RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu! (when checking argument for argument index in method wrapper_CUDA__index_select): 
Go to the distractor_generator.py or question_generator.py, theres a _model_predict function, add _.to('cuda')_ to source_encoding = self.tokenizer(blablabla) and make it source_encoding = self.tokenizer(blablabla).to('cuda')


## Requirements
Python 3.7+ 


## Running and Accessing The Server

Main Command:
```
flask --app YOUR_PREV_PATH'S\srv\controller\main.py run
```

or run ```main.py``` at ```srv/controller/main.py```


You can access your server in your browser, by opening: ```http://127.0.0.1:8080```

You can download [Postman](https://www.postman.com/) for easier GET and POST request testing



