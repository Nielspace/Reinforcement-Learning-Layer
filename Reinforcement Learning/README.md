# Reinforcement learning with OpenAI gym and Pytorch

OpenAI gym is one of the best libraries to test your reinforcement learning algorithms. Please refer to the official documentation for this library. 

## Setting up the repository
### Create a virtual environment

To install virtualenv run

``` pip install virtualenv```

Once install run:

```virtualenv env```

```source env/bin/activate```

You should see (env) at the beginning of the terminal prompt, indicating the environment is active. 

To get out of the environment, simply run

```deactivate```

### Installing Dependencies

While the virtual environment is active, install the required dependencies by running

```pip -r requirements.txt```

This will install all of the dependencies.

### Install ROMS

When you are getting started with gym you should know that some of the gym environments need ROM, especially the atari environments. Roms are basically game images. You can download the ROM and then install it in your OS. 

Follow these steps to download and install roms:
1. Visit this [website](http://www.atarimania.com/rom_collection_archive_atari_2600_roms.html) and [download](http://www.atarimania.com/roms/Roms.rar) the roms.rar file in your OS.
2. Unrar it.
3. After you unrar you will get two files: HC ROMS.zip and ROMS.zip. 
4. Unzip ROMS.zip (inside this project folder). 
5. Once you have followed the above mentioned process run ```python -m atari_py.import_roms ROMS``` in your terminal. 

### Training the model
To train a model, use the ```train.py``` script and specify any parameters that need to be changed, such as the environment or epsilon decay factors. A list of the default values for every parameters can be found by running

```python train.py --help```

### Testing the model
To test, use ```test.py --checkpoint``` 


## Things to keep in mind

If you face problems in installing the atari environement then use the following commands:
 
- `pip install gym[atari]`

The above command only bash script If you are in zsh (z shell) script then you can use the following pip commands:
1. ```pip install 'gym[atari]'```
2. ```pip install gym\[atari\]```
3. ```pip install atari-py```



