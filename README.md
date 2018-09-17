# docker-svm-light-api
[SVM light](http://svmlight.joachims.org/) API service on Docker only using docker-compose command.

# How to Start/stop
## Pull from Docker Hub (recommend)
```
docker run -it -d -p 5001:3001 mhirano/svm-light-api
```
If you need change port number, please change 5001 to what you want.

## Clone from Github
After cloning this repository,

UP
```
docker-compose up -d
```

Down
```
docker-compose down
```

# Setting
Initially, this is binded on #5001 port.
So, please access to ```http://localhost:5001/```

If you need, please change the port number from 5001 on ```docker-compose.yml```.

# How to Use
## Learning Mode
Post to ```/svm-light/v1/learn``` with your example file.
Your post file name haa to be "example_file" and its MIME type haa to be "text/plain."
If you need use any option on [SVM light](http://svmlight.joachims.org/), please post "option=option" together. Option details is shown on [SVM light](http://svmlight.joachims.org/).
Some options like "-h" are forbidden because you can not use results showing only on the terminal usually.
After submittion and calaculation on docker, you will get the result of svm model.

### Usage Example:
If you need example file, you can downlod [SVM light official example files.](http://download.joachims.org/svm_light/examples/example1.tar.gz) More example are on [the SVM light official site] (http://svmlight.joachims.org/). 
```
curl -X POST http://localhost:5001/svm-light/v1/learn -F "example_file=@train.dat;type=text/plain" -F "option=-f 0" > model
```

## Classify Mode
Post to ```/svm-light/v1/classify``` with your example file (test data file) and model file.
Your post file names have to be "example_file" and "model_file", and these MIME types have to be "text/plain."
If you need use any option on [SVM light](http://svmlight.joachims.org/), please post "option=option" together. Option details is shown on [SVM light](http://svmlight.joachims.org/).
Some options like "-h" are forbidden because you can not use results showing only on the terminal usually.
After submittion and calaculation on docker, you will get the result of svm predictions.

### Usage Example:
```
curl -X POST http://localhost:5001/svm-light/v1/classify -F "example_file=@test.dat;type=text/plain" -F "model_file=@model;type=text/plain" > predictions
```

# Copyright
Copyright &copy; 2018 · All rights reserved. · [Masanori HIRANO](https://mhirano.jp/)
