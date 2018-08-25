import map_env_v3 as map_env
import numpy as np
import pandas as pd
import os
import tensorflow as tf
import random
class QLearningTable:
    def __init__(self,
                 action,
                 learning_rate =.1,
                 reward_decay=0.9,
                 e_greedy=0.99 ):
        self.actions = action
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        if os.path.exists("q_table.txt"):
            # print("-----------------")
            self.q_table = pd.read_csv('./q_table.txt', names=["y", "n"], header=None)
        else:
            # print("111111111111")
            self.q_table = pd.DataFrame(columns=self.actions,dtype=np.float64)

    def choose_action(self, observation):
        observation_str = str(tuple(observation))
        self.check_state_exist(observation_str)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            if int(observation[3]) < 3:
                # print("can not change")
                return "n"
            state_action = self.q_table.loc[observation_str, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            # print(np.random.permutation(state_action.index))
            action = state_action.idxmax()
            # print("change: {}".format(action))
        else:
            # choose random action
            action = np.random.choice(self.actions)
            # print("random: {}".format(action))
        return action

    def learn(self, s, a, r, s_):
        s = str(tuple(s))
        s_ = str(tuple(s_))
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        q_target = r + self.gamma * self.q_table.loc[s_, :].max()
        # print(q_predict,q_target)
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            # print(state)
            self.q_table = self.q_table.append(
                pd.Series(
                    [0.0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )
        # print(self.q_table)
        self.q_table.to_csv("q_table.txt",header=None)

class DeepQNetwork:
    def __init__(self,
                 num_actions,
                 num_features,
                 actions,
                 learning_rate = 0.1,
                 reward_decay = 0.9,
                 e_greedy = 0.9,
                 memory_size = 2000,
                 batch_size = 32,
                 time_to_replace = 300):

        self.num_actions = num_actions
        self.actions = actions
        self.num_features = num_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.replace_time = time_to_replace
        self.epsilon = e_greedy
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.memory = np.zeros((memory_size,self.num_features*2+2))
        self.session = tf.Session()
        self.session.run(tf.initialize_all_variables())
        self.m_index = 0
        self.learn_counter = 0
        self._build_nn()

    def _build_nn(self):
        ### next observation
        self.s_ = tf.placeholder(tf.float32, [None, self.num_features], name= "s_")
        ### current observation
        self.s = tf.placeholder(tf.float32, [None, self.num_features], name= "s")
        ### {y: xxx, n: xxx}
        self.q_target = tf.placeholder(tf.float32, [None, self.num_actions], name= "q_target")

##predit_nn -> q_predict
        with tf.variable_scope('predit_nn'):
            col = ['predit_nn', tf.GraphKeys.GLOBAL_VARIABLES]
            with tf.variable_scope("layer_1"):
                l1 = self._add_layer(col=col,w_name="w1",
                                      b_name="b1",input=self.s,
                                      insize=self.num_features,outsize=15)

            with tf.variable_scope("layer_2"):
                self.q_predict = self._add_layer(col=col,w_name="w2",
                                                  b_name="b2",input=l1,
                                                  insize=15,outsize=self.num_actions)
        self.session.run(tf.global_variables_initializer())

        with tf.variable_scope("count_loss"):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target,self.q_predict))

        with tf.variable_scope("train"):
            self.train = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

##using the separate Target Network to count q_target
        with tf.variable_scope("fix_nn"):
            col = ['fix_nn', tf.GraphKeys.GLOBAL_VARIABLES]
            with tf.variable_scope("layer_1"):
                l1 = self._add_layer(col=col,w_name="w1",b_name="b1",input=self.s_,
                                      insize=self.num_features,outsize=15)

            with tf.variable_scope("layer_2"):
                self.q_next = self._add_layer(col=col,w_name="w2",b_name="b2",input=l1,
                                               insize=15,outsize=self.num_actions)
        self.session.run(tf.global_variables_initializer())


    def _add_layer(self,
                    col,
                    w_name,
                    b_name,
                    input,
                    insize,
                    outsize,
                    activation = False,
                    initializer_w = tf.random_normal_initializer(0., 0.5),
                    initializer_b = tf.constant_initializer(0.1)):
        Weight = tf.get_variable(w_name,
                                 shape=[insize,outsize],
                                 initializer=initializer_w,
                                 collections=col)
        bias = tf.get_variable(b_name,
                               shape=[1,outsize],
                               initializer=initializer_b,
                               collections=col)
        output = tf.matmul(input,Weight) + bias
        if activation:
            return activation(output)
        else:
            return output


    def choose_action(self, observation):

        observation = np.array(observation)[np.newaxis, :]
        if np.random.uniform() < self.epsilon:
            next_action = self.session.run(self.q_predict,
                                           feed_dict={self.s: observation})
            # print(next_action)
            return self.actions[np.argmax(next_action)]
        else:
            return self.actions[np.random.randint(0, self.num_actions-1)]

    def learn(self):
        if self.learn_counter % 50 == 0:
            p_para = tf.get_collection('predit_nn')
            t_para = tf.get_collection('fix_nn')
            self.replace_target_op = [tf.assign(t, e) for t, e in zip(p_para, t_para)]
            self.session.run(self.replace_target_op)
        if self.m_index > self.memory_size:
            sample = random.sample(range(self.memory_size),self.batch_size)
        else:
            sample = random.sample(range(self.memory_size),self.batch_size)
        b_memory = self.memory[sample,:]
        next, predict =self.session.run([self.q_next, self.q_predict],
                         feed_dict={self.s:b_memory[:,:self.num_features],
                                    self.s_:b_memory[:,-self.num_features:]})
        r = b_memory[: , self.num_features+1]
        target = predict.copy()
        action_index = [int(i) for i in b_memory[:,self.num_features]]
        b_index = range(self.batch_size)
        target[b_index,action_index] = r + self.gamma * np.max(next, axis=1)
        self.session.run([self.train, self.loss],
                      feed_dict={self.s: b_memory[:, :self.num_features],
                                 self.q_target: target})
        self.learn_counter += 1

    def save_memory(self, s, a, r, s_):
        a = self.actions.index(a)
        self.memory[self.m_index % self.memory_size, :] = np.hstack((s, [a, r], s_))
        self.m_index += 1

