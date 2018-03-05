# serverless-bahn-scrapper
Serverless zappa scrapping project running on AWS lambda.

# Usage

Activate your virtual environment:
```
source venv/Scripts/activate
```
Install requirements:
```
pip install -r requirements.txt
```

Add your AWS credential file to the user dir:
https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html

#Deploy:
```
zappa deploy
```

#Update
```
zappa update
```

#Undeploy
```
zappa undeploy
```



