#!/bin/sh

#scrot 'Screenshot_%Y-%m-%d_$wx$h.png' -e 'mv $f ~/Pictures/'
scrot 'Screenshot %Y-%m-%d %H.%M.%S.png' -e 'mv "$f" ~/Pictures/'


