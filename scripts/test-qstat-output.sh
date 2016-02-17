#!/bin/bash
# a prototype qstat -u $USER command for testing
# qstat-del
OPTION=$1
USER_NAME=$2

echo '
sched: 
                                                                         Req'd  Req'd   Elap
Job ID               Username Queue    Jobname          SessID NDS   TSK Memory Time  S Time
-------------------- -------- -------- ---------------- ------ ----- --- ------ ----- - -----
1248127.sched        shbinom  laurent  serial             5504     1   1    --  4800: R 4118:
1248128.sched        shbinom  laurent  serial             5577     1   1    --  4800: R 4118:
1287620.sched        shbinom  laurent  serial            12761     1   1    --  4800: R 3048:
1287640.sched        shbinom  laurent  serial            12900     1   1    --  4800: R 3048:
1287645.sched        shbinom  laurent  serial            12976     1   1    --  4800: R 3048:
1302819.sched        shbinom  laurent  26Sr80             4969     1   1    --  4800: R 2822:
1401747.sched        shbinom  laurent  serial             2651     1   1    --  2400: R 733:2
1401757.sched        shbinom  laurent  serial             3443     1   1    --  2400: R 733:0
1401797.sched        shbinom  laurent  serial             5012     1   1    --  2400: R 731:2
1401798.sched        shbinom  laurent  serial             5166     1   1    --  2400: R 731:1
1404092.sched        shbinom  serial12 28BST80           17062     1   1    --  1008: R 708:5
1404111.sched        shbinom  laurent  serial             9084     1   1    --  2400: R 708:4
1404624.sched        shbinom  laurent  serial            10329     1   1    --  2400: R 700:5
1404634.sched        shbinom  serial12 serial             4414     1   1    --  1008: R 700:5
1404647.sched        shbinom  serial12 serial             4607     1   1    --  1008: R 700:5
1408703.sched        shbinom  serial12 serial            10726     1   1    --  1008: R 591:5
1408720.sched        shbinom  laurent  serial            28904     1   1    --  2400: R 589:4
1408735.sched        shbinom  laurent  serial              999     1   1    --  2400: R 587:2
1420572.sched        shbinom  serial12 abinit            29249     1   6    --  1008: R 356:1
1420699.sched        shbinom  laurent  abinit             9865     1   6    --  1008: R 347:0
1431413.sched        shbinom  laurent  abinit            16981     1   6    --  2400: R 179:1
1439751.sched        shbinom  laurent  abinit              --      1   6    --  2400: Q   -- '

echo $1
echo $2
