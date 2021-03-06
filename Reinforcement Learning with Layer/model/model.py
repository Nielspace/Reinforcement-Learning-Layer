"""New Project Example

This file demonstrates how we can develop and train our model by using the
`features` we've developed earlier. Every ML model project
should have a definition file like this one.

"""
import subprocess
import sys

from typing import Any

from layer import Featureset, Train


from .argparser import parse_args
from .helpers import (compute_td_loss,
                          initialize_models,
                          is_atari,
                          set_device,
                          update_epsilon)
from .replay_buffer import ReplayBuffer
from .train_information import TrainInformation
from .wrappers import wrap_environment

from torch import save
from torch.optim import Adam

import cv2


def update_graph(model, target_model, optimizer, replay_buffer, args, device,
                 info):
    if len(replay_buffer) > args.initial_learning:
        if not info.index % args.target_update_frequency:
            target_model.load_state_dict(model.state_dict())
        optimizer.zero_grad()
        batch = replay_buffer.sample(args.batch_size)
        compute_td_loss(model, target_model, batch, args.gamma, device)
        optimizer.step()


def complete_episode(model, environment, info, episode_reward, episode,
                     epsilon):
    new_best = info.update_rewards(episode_reward)
    if new_best:
        print('New best average reward of %s! Saving model'
              % round(info.best_average, 3))
        save(model.state_dict(), '%s.dat' % environment)
    print('Episode %s - Reward: %s, Best: %s, Average: %s '
          'Epsilon: %s' % (episode, episode_reward, info.best_reward,
                           round(info.average, 3), round(epsilon, 4)))


def run_episode(env, model, target_model, optimizer, replay_buffer, args,
                device, info, episode):
    episode_reward = 0.0
    state = env.reset()

    while True:
        epsilon = update_epsilon(info.index, args)
        action = model.act(state, device, epsilon)
        if args.render:
            env.render()
        next_state, reward, done, _ = env.step(action)
        replay_buffer.push(state, action, reward, next_state, done)
        state = next_state
        episode_reward += reward
        info.update_index()
        update_graph(model, target_model, optimizer, replay_buffer, args,
                     device, info)
        if done:
            complete_episode(model, args.environment, info, episode_reward,
                             episode, epsilon)
            break

def train_model(train: Train, ) -> Any:
    cmd = 'python -m atari_py.import_roms .'

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate() 
    
        
    info = TrainInformation()

    args = parse_args()
    env = wrap_environment(args.environment)
    device = set_device(args.force_cpu)
    model, target_model = initialize_models(env, device, args.checkpoint)
    optimizer = Adam(model.parameters(), lr=args.learning_rate)
    replay_buffer = ReplayBuffer(args.buffer_capacity)

    for episode in range(args.num_episodes):
        run_episode(env, model, target_model, optimizer, replay_buffer, args,
                    device, info, episode)

    env.close()

    return model             
    
   
