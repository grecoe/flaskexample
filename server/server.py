from app import app

'''
  Running with SSL
    1. flask run --cert=adhoc
    2. Run this file right with python 
'''

# Not safe, but will work to open the machine up to external traffic with adhoc
# SSL certificates (HTTPS). 
if __name__ == "__main__":
  app.run(host='0.0.0.0', ssl_context='adhoc')
