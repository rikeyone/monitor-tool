
## Memory record 

It uses `free` command to record the memory which has been used in the past time.

caculate function: total = used + free + buff/cache

```shell
              total        used        free      shared  buff/cache   available
Mem:       32871328    12632316      281116     1212644    19957896    18493416
Swap:       7999484      152144     7847340

```

## Cpu load record

In this function, `mpstat` command is used to track cpu usage which could represent
system load.

```shell
16时02分08秒  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
16时02分08秒  all    4.97    0.00    5.05    0.51    0.00    0.02    0.00    0.00    0.00   89.45
```

It reads the idle percentage first, then cpu usage could be caculated by : (100% - % idle).

## iowait record

The `iowait` data is also recorded by mpstat command. The value represents the time which cpu waits
for IO operations.
