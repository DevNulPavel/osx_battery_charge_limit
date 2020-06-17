MacOS / OSX limit maximum battery charge.
========================

Li-ion and polymer batteries (like the one in your MacBook) last the longest when operating between 30 and 80 percent. Keeping your battery at 100% at all times can shorten the lifespan of your notebook significantly. More information can be found here: https://batteryuniversity.com/learn/article/how_to_charge_when_to_charge_table

Script info
------------------------
This is script for changing maximum battery charge value on macbook with set SMC key value. 
It uses *smc-command* binary from smcFanControl project for SMC keys access [smcFanControl](https://github.com/hholtmann/smcFanControl "smcFanControl"). 

Script changes SMC key "BCLM" (Battery control level maximum). Script sets maximum battery charge percent value from 20% to 100%.

You can reset macbook's SMC for rollback script changes in case of some problems.

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

Warning!
------------------------
I do not take any responsibility for any sort of damage in result of using this tool! Alltough this had no negative side effects for me, scripts still taps in some very low level system functions that are not ment to be tampered with. Use it at your own risk!

Alternatives with GUI:
------------------------
- [AlDente](https://github.com/davidwernhart/AlDente)
- [BatteryStatusShow](https://github.com/sicreative/BatteryStatusShow)

Other references:
------------------------
- [coconutbattery](https://www.coconut-flavour.com/coconutbattery/)
- [smcFanControl](https://github.com/hholtmann/smcFanControl)
- [libsmc](https://github.com/beltex/libsmc)
- [VirtualSMC](https://github.com/acidanthera/VirtualSMC)
- [osx-cpu-temp](https://github.com/lavoiesl/osx-cpu-temp)

