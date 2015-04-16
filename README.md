# spawner
Simple Python/PyQt script that runs multiple instances of a shell command; useful for instance to stress-test a server with multiple clients

![Screenshot](http://i.imgur.com/SIJI0gv.png)

### Notes

The process can be any kind of shell script, and the string `{}` will be replaced by the index of the instance.

For instance, the command:

```
while :; echo {}; sleep {}; done
```

With number of instances set to `5`, transforms into these five shells running in parallel:

```
while :; echo 1; sleep 1; done
while :; echo 2; sleep 2; done
while :; echo 3; sleep 4; done
while :; echo 4; sleep 5; done
```
