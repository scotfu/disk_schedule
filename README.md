Disk scheduling algorightms is used by opearting system to decide the which cylinder should be visited first in the old fashion hard disk, which can reduce the seeking time, try to give each cylinder a fair chance to be visited and get a better performace.

There are many disk scheduling algorithms, in this project, I implemented six algorithms and made compararsions between them.
They are 

Definition
Track number start from 1 to 1024.

SCAN :  SCAN algorithm acts like a elevator, continue to travel in current direction until the end, then go the opposite direction till the other end.

LOOK : LOOK is similar to SCAN,but LOOK will change directions when the head has reached the last request in the current direction, acts as a real elevator, while SCAN change directions at the end of the cylinder.

CSCAN :  In CSCAN algorithm, once the head has arrived at the end of the disk, it returns to the beginning and go through this direction again.

CLOOK :  CLOOK is similar to CSCAN,but CLOOK will go back and restart at the same direction when the head has reached the last request at the current
direction.

SSF : SSF algorithm detects which request is closest to the current position, and then services that request next.

FIFO : First in ,first out(service).

RSS : Select next track randomly.

