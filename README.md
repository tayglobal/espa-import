# Remote Import


## Introduction

This library allows you to rapidly code and run on distributed clusters.
There are no need to rebuild containers.
The cluster simply imports modules while oblivion to the fact that it's
loading source from a remote source and you control.

The remote source itself is can be anything that is supported by
[KYDB](https://kydb.readthedocs.io/en/latest/)


## Example

### Basic local and remote

Create *hello.py*

```python

def main():
     print("Hello World!")
         
```

Upload it to remote source

```
python -m epimport.uploader --srcdb redis://your.redis.host/my-source --key hello.py hello.py 
```

Or you could just let use the below running to keep your local source in sync with remote.

```
python -m epimport.code_sync --recursive --verbose .
```
    
Now we can import the **hello** module.
You can run this on any machine that has connection to the redis server!!

```python
import epimport as ei
ei.set_srcdb('redis://your.redis.host/my-source')

import hello

hello.main() # prints 'Hello Word!'
```

Or simply use the **main** module

```
# prints 'Hello World!'
python -m epimport.main --srcdb redis://your.redis.host/my-source hello
```

### Docker container

You can also use a docker container to run your script on any host that has access to your remote source.

Try going to a different host with nothing installed and run:

Pull the container from DockerHub.

```
docker pull tayglobal/espa-import:latest
```

Find the image id:

```
docker images
```

Now run it.

```
docker run $IMAGE_ID python -m epimport.main \
    --srcdb redis://your.redis.host/my-source hello
```

There you have it. Now knock yourself out with a cluster of containers in ECS Fargate, Kubenetes or whatever you fancy.
Just try and do more work than just say *Hello World!* Enjoy!