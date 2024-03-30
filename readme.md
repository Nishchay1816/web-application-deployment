# Web Application Deployment Documentation

## 1. Application Development
Developed a Python FastAPI web application to serve as the basis for deployment.
### Create a python environment : 
```bash
python -m venv venv
Activate : venv\Scripts\activate
For creating webpage
pip install fastapi
pip install "uvicorn[standard]"
```


## 2. Minikube Installation and installation of argo cd and argo rollouts on kubernetes cluster

### Minikube :
```powershell
New-Item -Path 'c:\' -Name 'minikube' -ItemType Directory -Force
Invoke-WebRequest -OutFile 'c:\minikube\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing
```

### Setting up env variables :
```powershell
$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
if ($oldPath.Split(';') -inotcontains 'C:\minikube'){
  [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)
}
```
```powershell
minikube start
kubectl get po -A
```

### Installing Argo cd
```bash
kubectl cluster-info
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get pods -n argocd
kubectl -n argocd get all
kubectl edit svc argocd-server -n argocd : Change type to NodePort
kubectl get nodes -o wide : To get Ip of kubernetes node
kubectl get svc : To get port of kubernetes node
kubectl port-forward svc/argocd-server -n argocd --address 0.0.0.0 8080:443
minikube service argocd-server -n argocd
C:\argocd.exe admin initial-password -n argocd  : 2kYqek5jRD6lhZmf
```

### Installing argo rollouts
```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
kubectl argo rollouts version
```

## 3. Local Testing
Tested the web application locally to ensure functionality and correctness.

## 4. Push the code to local repository
### Created new repository on github
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <https://github.com/Nishchay1816/web-application-deployment.git>
git push -u origin master
```

## 5. Dockerization

pip freeze > requirements.txt

Created a Dockerfile to containerize the FastAPI application.
### Dockerfile
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Built the Docker image using the docker build command.
```bash
docker build -t webapp:latest .
docker images
docker run -d -p 8000:8000 webapp:latest
docker ps -a
```

## 6. Docker Hub
Created new repository on docker hub
Tagged the Docker image with the appropriate Docker Hub username and repository name.
```bash
docker tag <image_id> nishchay18/ai-planet-web-app:latest
```

Logged in to Docker Hub using the docker login command.
```bash
docker login
```

Pushed the Docker image to Docker Hub using the docker push commandPython version : 3.9.7
```bash
docker push nishchay18/ai-planet-web-app:latest
```

Created Manifests files and used the docker image Created

## 7. Deploying app on argo cd 
```bash
argocd login <localhost:8080>
argocd app create webapp --repo https://github.com/Nishchay1816/web-application-deployment.git --path manifests --dest-server https://kubernetes.default.svc --dest-namespace argocd
argocd app sync webapp
```
Once the state is healthy 
Access the web app via minikube ip and node port : http://192.168.49.2:31429/

## 8.Define a Rollout Strategy:
```bash
kubectl -n argo-rollouts get pod
```
Replaced the existing Deployment resource with a Rollout resource
Created a new docker file for web app
```bash
kubectl -n argo-rollouts apply -f rollout.yaml
kubectl -n argo-rollouts get rollout webapp-rollout
```

## 9.Cleanly remove all resources created during this assignment from the Kubernetes cluster
```bash
kubectl delete namespace argocd
kubectl delete namespace argorollouts
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
kubectl delete -f rollouts.yaml
kubectl get all --all-namespaces
```
