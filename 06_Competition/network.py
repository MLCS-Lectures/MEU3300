import redis

class Network:
    '''
    Team name example : team1 (t is in lowercase)
    '''
    def __init__(self,team_name):
        self.r = redis.StrictRedis(host='redis.hwanmoo.kr', port=6379, db=2)
        self.car_name = team_name

    def syncTrigger(self):
        self.r.hset('ready_flag', self.car_name, True)
        # print("Synchronous Triggered")
        while True:
            computed_flag = eval(self.r.hget('computed_flag', 'vrep'))
            if computed_flag == True:
                self.r.hset('ready_flag', self.car_name, False)
                break