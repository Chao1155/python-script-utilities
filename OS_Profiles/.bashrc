
# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi


# personal definitions

alias l='ls -al'
alias ..='cd ..'
alias ...='cd ../..'


# native gem5 configurations 

M5_PATH="$HOME/M5_dependences"
export M5_PATH

# for tmux path
PATH="$HOME/local/bin:$PATH"


