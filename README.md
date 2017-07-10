# pso-appdev-appengine-std-python
Google Cloud App Dev PSO - App Engine Standard Python


# Setup

## git
```
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```

```
gcloud source repos clone pso-appdev  
```
## Create Instance
```
gcloud compute --project "pso-appdev-gnp-mex" instances create "pso-appdev-appengine1" --zone "us-west1-c" --machine-type "n1-standard-2" --subnet "default" --maintenance-policy "MIGRATE" --service-account "839154992522-compute@developer.gserviceaccount.com" --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --image "ubuntu-1604-xenial-v20170619a" --image-project "ubuntu-os-cloud" --boot-disk-size "200" --boot-disk-type "pd-standard" --boot-disk-device-name "pso-appdev-appengine1"
```
