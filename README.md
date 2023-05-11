#### Install Python3.9

```
wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz
tar -xf Python-3.9.9.tgz
cd Python-3.9.9
./configure --enable-optimizations
sudo make altinstall
```

#### Deploy Backend Service
```
git clone https://github.com/AWS-First-Cloud-Journey/FCJ-DMS-Backend.git
cd FCJ-DMS-Backend
sam build
sam deploy --guided
```
***Note API URL***

#### Deploy Frontend Service
```
git clone https://github.com/AWS-First-Cloud-Journey/FCJ-Serverless-DMS.git
cd FCJ-Serverless-DMS
npm install --force
npm install -g @aws-amplify/cli
```
#### Configuration Amplify
```
amplify init
amplify import auth
amplify import storage
npm install --global yarn
```
#### Build and Copy to S3:
```
yarn build
aws s3 cp build s3://fcjdmswebstore-2000 --recursive
```

