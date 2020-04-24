from app import app

# Not safe, but will work to open the machine up to external traffic. 
if __name__ == "__main__":
  app.run(host='0.0.0.0')
