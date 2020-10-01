from datetime import datetime
import updated_variables as uv


def printer():
    tempo = datetime.today()
    h,m,s = tempo.hour, tempo.minute, tempo.second
    time=f"{h}:{m}:{s}"
    #path=uv.__file__
    #with open(path,"w") as fp:
    #    fp.writelines(['a=5 \n','b="'+time+'" \n'])
    print(time)