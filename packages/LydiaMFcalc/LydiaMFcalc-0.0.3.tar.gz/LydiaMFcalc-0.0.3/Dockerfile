
# create image by >>> docker build -t dockerpy38 .
# run image by    >>> docker run -it --rm dockerpy38


FROM python:3.8-slim
WORKDIR /usr/src/app




### --- Demo environment - BEGIN --------------------    
#     Execute anywhere ...

RUN python -m pip install LydiaMFcalc
        
### --- Demo environment - END ---   
  
   
    
    
### --- Testing environment - BEGIN -----------------    
#     Execute in package or app folder !
   
#RUN apt-get update \
#     && apt-get install -y geany   
#  need to figure out X11 stuff first

COPY . .
RUN python -m pip install \
        mypy \
        pyflakes \
        flake8 \
        black
        
COPY . .

### --- Testing environment - END ---   

    
    
# should always be executed if nothing specific is needed:  
CMD bash
