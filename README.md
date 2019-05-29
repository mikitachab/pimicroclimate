# pimicroclimate

## Setup
Create virtual environment after clonning repo
```bash
./prepare_venv.sh
```
Activate virtual environment
```bash
source venv/bin/activate
```
Run Django Dev Server
```bash
python manage.py runserver
```
For testing porpose you can populate local dev server with data from heroku prodaction sever. Remember that local dev server must be running with default django debug host address.
```bash
python put_data.py
```
