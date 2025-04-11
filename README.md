# ASCII-horses
ASCII horses is a simple python script that generates random virtual horses races in the terminal.

## Usage
```bash
socat TCP-LISTEN:1337,reuseaddr,fork EXEC:python3\ main.py,pty,stderr,setsid,sigint,sane
```

## Notice
Is possible for more than one horse to finish at the same time, in this case, it will print all the horses that won.

## License
[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html)