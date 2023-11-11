# Apple Silicon Tensorflow Installation + Validation + Notes

I needed to install Tensorflow to start tinkering with it. Never used Python
before (though I've been writing Ruby code for over 10 years, shouldn't be too
hard once I learn the ecosystem). But I have some unique quirks of my own that
aren't often catered to like most:

- I use [PowerShell Core][pwsh] on MacOS. Seriously. [Here's why][pwsh-article].
(Link to Wayback Machine because of acquisition). [pyenv][pyenv] doesn't support
[pwsh][pwsh] out of the box, so I had to [get creative][pyenv-compat] just to get
started.
- I'm also on a Mac Studio with an M2 Max - which of course has an integrated
GPU. Not supported by tensorflow according to the documentation I read as of
this evening (which isn't surprising). So I had to do a little research, which
turned up some interesting [Apple Developer documentation][metal-tensorflow].

So these are my notes after figuring things out on how to set all this up and
verify that it's working.

## Got Apple Silicon? Want Tensorflow to use your GPU via Metal API? Do this!

The following is somewhat inelegant but does seem to work. Keep in mind I'm
fairly new to Python, and there is likely room to optimize this workflow, but
for local developer workstation experimentation, it seems to work.

> Optional - if you're a crazy person like me using PowerShell Core, set up
your environment to take advantage of [pyenv][pyenv] through PowerShell. You may
not get autocompletion this way, but my little [hax][pyenv-compat] for pwsh do, now,
include a compatibility layer for `pyenv` that seems to work. Copied it straight
from my compatibility layer for `rbenv`, which has also worked for a few years
just fine.

Assuming `pyenv` is ready to rock in your shell:

```bash
$ pyenv install 3.11 && pyenv global 3.11 && python --version # sanity check
$ pip install --upgrade pip
$ python -m venv ~/.venv/metal # create a virtual env off pyenv's python 3.11
$ ~/.venv/metal/bin/Activate.ps1 -Verbose # for PowerShell, use 'source ~/.venv/metal/bin/activate' for bash/zsh
$ pip install tensorflow
$ pip install tensorflow-metal # this is the one maintained by Apple as of late 2023
$ cd /path/where/this/silly/little/repo/got/cloned/on/your/disk
$ python metal.py
```

If all that insanity went right (good luck), you'll likely see something similar
to the following hit your terminal:

```
Downloading data from https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz
169001437/169001437 [==============================] - 3s 0us/step
2023-11-10 22:05:58.824656: I metal_plugin/src/device/metal_device.cc:1154] Metal device set to: Apple M2 Max
2023-11-10 22:05:58.824682: I metal_plugin/src/device/metal_device.cc:296] systemMemory: 64.00 GB
2023-11-10 22:05:58.824690: I metal_plugin/src/device/metal_device.cc:313] maxCacheSize: 24.00 GB
Epoch 1/5
2023-11-10 22:06:01.557603: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:117] Plugin optimizer for device_type GPU is enabled.
782/782 [==============================] - 55s 58ms/step - loss: 4.7810 - accuracy: 0.0612
Epoch 2/5
782/782 [==============================] - 45s 58ms/step - loss: 4.1494 - accuracy: 0.1188
Epoch 3/5
782/782 [==============================] - 44s 56ms/step - loss: 4.2114 - accuracy: 0.1039
Epoch 4/5
782/782 [==============================] - 48s 62ms/step - loss: 3.7985 - accuracy: 0.1518
Epoch 5/5
782/782 [==============================] - 45s 58ms/step - loss: 3.6025 - accuracy: 0.1876
```

In my case, I did also see log messages telling me stuff like...

```
Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
```

...and...

```
Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
```

RIGHT after it, depending on your specific model of Apple hardware (I'm trying
this on a Mac Studio M2 Max). My interpretation of this - as I'm not a hardware
expert by any means - is that these are just leftovers of log messages from
libraries of OSS projects that Apple re-used in `tensorflow-metal`, and nothing
to worry about. As you can see elsewhere in the logs, your GPU -is- getting
picked up and used. Non-Uniform Memory Access may not be relevant in these
machines anymore for all I know (again, got better things to do than nerd out
over every little detail, gotta get things done, like ship this repo so someone
can eventually benefit from this - I hope!), at least according to ChatGPT, our
future overlord 🤣

Credit for the script here goes fully to the Apple developers - copied it from
them. Just wanted to include it here for convenience. See the documentation I
linked for the most up to date version, and if that 404's for you at some point
in the future, I advise using archive.org to look that up, as Apple has had a
somewhat..."complex" history (I'm being diplomatic, here) when it comes to the
quality of their developer documentation, public-facing, anyway, so far as I can
tell. (Well, as it pertains to non-iOS related development.)

[updater]: https://github.com/jahio/dawts/blob/main/powershell/hax/util/update-pwsh.ps1
[pwsh-article]: https://web.archive.org/web/20220505012311/https://www.starkandwayne.com/blog/i-switched-from-bash-to-powershell-and-its-going-great/
[pwsh]: https://github.com/powershell/powershell
[pyenv]: https://github.com/pyenv/pyenv
[metal-tensorflow]: https://developer.apple.com/metal/tensorflow-plugin/
[pyenv-compat]: https://github.com/jahio/dawts/blob/main/powershell/hax/lang/python.ps1
