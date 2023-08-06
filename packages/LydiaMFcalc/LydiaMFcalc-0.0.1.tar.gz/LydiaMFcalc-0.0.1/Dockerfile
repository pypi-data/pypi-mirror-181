FROM python:3.8.16-slim

WORKDIR /usr/src/app




# --- Demo environment - BEGIN ---    
#     Execute anywhere ...

RUN python -m pip install \
        -i https://test.pypi.org/simple/ LydiaMFcalc
        
# --- Demo environment - END ---   
  
   
##############################################
    
    
## --- Testing environment - BEGIN ---    
##     Execute in package/app folder !
#   
##RUN apt-get update \
##     && apt-get install -y geany   
##  need to figure out X11 stuff first
#
#RUN python -m pip install \
#        mypy \
#        pyflakes \
#        flake8 \
#        black
#
#COPY . .
#
## --- Testing environment - END ---   

    
    
    
    
        
CMD bash
