# python-csv-to-firebase

## setup

1. $`cd virtualenv && virtualenv -p python3 env --no-site-packages` to prep all dependencies in project
1. start virtual environment $`cd ../ && source virtualenv/env/bin/activate` (see: http://sourabhbajaj.com/mac-setup/Python/virtualenv.html)
1. If setting up rPi, be ready to get some coffee. This next step takes a bit to install. (~15mins)
1. go fetch all python dependencies $`pip install -r virtualenv/requirements.txt`
1. $`python3 start.py`

## helpful tips with setup

- connect mac to pi file system for editing (see: https://www.raspberrypi.org/documentation/remote-access/ssh/sshfs.md)
- stop virtual environment $`deactivate`
- freeze new dependencies while virtual environment is active (see setup #3) in `virtualenv/env/` folder $`pip freeze --local > ../requirements.txt`