# SMT  
Web based SMT - pt to en  

# Instructions  
Run website:
install pip  
pip install -r requirements.txt  
python manage.py runserver  

Run moses server:  
docker build -t moses .  
docker run -d -p 5000:5000 moses python run_moses.py &  


# Authors  
Ruben Vasconcelos  
Sebastian wankovic  
Daniel Redneck  
