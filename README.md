# pso-appdev-appengine-std-python
Google Cloud App Dev PSO - App Engine Standard Python


# Setup

## initialize API
```
gcloud service-management enable appengine.googleapis.com
gcloud service-management enable compute-component.googleapis.com
```
## git
```
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
  git remote add upstream https://github.com/joseret/pso-appdev-appengine-std-python
```

```
gcloud source repos clone pso-appdev  
```
## Create Instance
```
gcloud compute --project "pso-appdev-gnp-mex" instances create "pso-appdev-appengine1" --zone "us-west1-c" --machine-type "n1-standard-2" --subnet "default" --maintenance-policy "MIGRATE" --service-account "839154992522-compute@developer.gserviceaccount.com" --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --image "ubuntu-1604-xenial-v20170619a" --image-project "ubuntu-os-cloud" --boot-disk-size "200" --boot-disk-type "pd-standard" --boot-disk-device-name "pso-appdev-appengine1"
```

## Deploy Simplest App
```
gcloud app deploy app.yaml
```

## Add Libraries
```commandline
https://askubuntu.com/questions/244641/how-to-set-up-and-use-a-virtual-python-environment-in-ubuntu
```

```commandline
apt-get install libffi-dev libssl-dev
```

```commandline
pip install -r requirements -t lib
```

# References

https://cs.corp.google.com/piper///depot/google3/experimental/gtech_pssk/crono
https://firebase.google.com/docs/web/setup
https://firebase.google.com/docs/auth/web/start#sign_up_new_users
https://firebase.google.com/docs/auth/web/anonymous-auth
http://google-auth.readthedocs.io/en/latest/
https://cloud.google.com/appengine/docs/standard/python/authenticating-users-firebase-appengine

https://www.spinnaker.io/guides/tutorials/codelabs/appengine-source-to-prod/
https://github.com/roike/SpaTemplate