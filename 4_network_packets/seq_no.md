To ensure reliabilty TCP uses

1. Seq no.
  Number that identifies the first byte of the data chunk
  ex:
  bytes: 8   8   8-->how many bytes long each data chunk is
        how | are  | you
      0   7 8  15 16    23
  so the starting number of each data chunk, 0,8,and 16 form the seq no of that chunk

2. Ack no.
  The next starting byte that i want to receive


  A                             B
  |  How(seq=0,8byte)           |
  |---------------------------->|
  |  ack 8                      |
  |<----------------------------|
  |   are(seq=8, 8 bytes)       |
  |---------------------------->|
  |   ack=16                    |
  |<----------------------------| 
  |                             |

  but if all the seq nos start from 0 hackers can probably guess and inject something of their own, so A chooses an arbitrary number but now how will B know that the arbitary number is the first sequence no? This is where the 3 way handshake comes in where A sends a syn packet incluing a seq no that it is planning to start with(lets say1000) and B sends back an packet with ack no 1001 and its own arbitrary seq no.(lets say 5000) and finally A sends back packet with ack no. 5001