import map_env_v3 as map_env
import RL
import random as rnd
import time
import sys
def cars(r1,r2):
    if env.time%(r1.randint(0,10)+5) == 0:
        choose_road = r2.randint(1,13)
        if choose_road == 1:
            env.cars_append1()
        if choose_road == 2:
            env.cars_append1_L()
        if choose_road == 3:
            env.cars_append1_R()
        if choose_road == 4:
            env.cars_append2()
        if choose_road == 5:
            env.cars_append2_L()
        if choose_road == 6:
            env.cars_append2_R()
        if choose_road == 7:
            env.cars_append3()
        if choose_road == 8:
            env.cars_append3_L()
        if choose_road == 9:
            env.cars_append3_R()
        if choose_road == 10:
            env.cars_append4()
        if choose_road == 11:
            env.cars_append4_L()
        if choose_road == 12:
            env.cars_append4_R()

def traffic_baseline():
    observation = env.reset()
    total_reward = 0
    r1 = rnd
    r2 = rnd
    r1.seed(1)
    r2.seed(2)
    # --------------- BASELINE (switch by 10 time-step) -------------------
    while True:
        env.render()

        cars(r1,r2)
        action = 'n'
        # if time step % 10 != 0, we can not switch the lights 
        if env.time%10 == 0:
            action = 'y'
        observation_, reward, done = env.switch_light(action)
        total_reward += reward

        observation = observation_
        if done:
            print('Baseline: the number of cars waiting')
            print(total_reward)
            total_reward = 0
            break

def traffic():
    for i in range(100):
        observation = env.reset()
        t_reward = 0
        step = 0
        r1 = rnd
        r2 = rnd
        r1.seed(1)
        r2.seed(2)
        while True:
            step+=1
            # time.sleep(0.1)
            cars(r1, r2)
            env.render()
            action = RL.choose_action(observation)
            if int(observation[5]) < 6:
                # print("can not change")
                action = "n"
            # print(action)
            observation_, reward, done = env.switch_light(action)
            t_reward += reward
            RL.save_memory(observation,action,reward,observation_)
            if step > 500 and step%5 == 0:
                RL.learn()

            observation = observation_
            if done:
                print(t_reward)
                break


if __name__ == "__main__":
    env = map_env.Map()
    mode = sys.argv[1]
    env.after(100,traffic_baseline())
    env.destroy()
    if mode == 'RL':
        env = map_env.Map()
        RL = RL.QLearningTable(env.action_space)

    elif mode == 'DQN':
        env = map_env.Map()
        RL = RL.DeepQNetwork(num_actions=2, num_features=6,actions=['y','n'])
    env.after(100,traffic())