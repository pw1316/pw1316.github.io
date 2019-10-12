---
layout: page
title: Tmux Cheat Sheet
date: 2019-10-12 14:27:42 +0800
mdate: 2019-10-12 14:27:42 +0800
---

- [Basic](#basic)
- [Session](#session)
- [Window](#window)
- [Panel](#panel)

### Basic

New session

```
tmux [new -s <sess-name>]
```

Attach session

```
tmux a [-t <sess-name>]
```

List session

```
tmux ls
```

Kill session

```
tmux kill-session -t <sess-name>
```

### Session

```
:new<CR>  # new session
s         # list session
$         # rename session
```

### Window

```
c  # create window
w  # list windows
n  # next window
p  # previous window
f  # find window
,  # name window
&  # kill window
```

### Panel

```
%  # vertical split
"  # horizontal split
o  # swap panes
q  # show pane numbers
x  # kill pane
+  # break pane into window (e.g. to select text by mouse to copy)
-  # restore pane from window
   # toggle between layouts
{  # move the current pane left
}  # move the current pane right
z  # toggle pane zoom
```

Resize panel

```
:resize-pane [-t [<id>]] -D|U|L|R [<value>]
```
