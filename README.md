MacOS / OSX limit maximum battery charge.
========================

Info
------------------------
This is script for changing maximum battery charge value on macbook with set SMC key value. 
It uses smc-command binary from smcFanControl for SMC keys access [smcFanControl](https://github.com/hholtmann/smcFanControl "smcFanControl"). 

Script changes SMC key "BCLM" (Battery control level maximum). Script sets maximum battery charge percent value from 20% to 100%.

You can reset macbook SMC for rollback script changes in case of some problems.

Tests 
------------------------
Tested on Macbook Pro 13 (mid 2020, 2 ports).

Usage examples
------------------------
```
# Get current charge limit
python3 main.py
python3 main.py -c

# Set maximum charge level at 65%
sudo python3 main.py -s 65

# Reset maximum charge level to 100%
sudo python3 main.py -r
```

Alternatives with GUI:
------------------------
- [AlDente](https://github.com/davidwernhart/AlDente)
- [BatteryStatusShow](https://github.com/sicreative/BatteryStatusShow)

Other references:
------------------------
- [smcFanControl](https://github.com/hholtmann/smcFanControl)
- [libsmc](https://github.com/beltex/libsmc)
- [VirtualSMC](https://github.com/acidanthera/VirtualSMC)
- [osx-cpu-temp](https://github.com/lavoiesl/osx-cpu-temp)

