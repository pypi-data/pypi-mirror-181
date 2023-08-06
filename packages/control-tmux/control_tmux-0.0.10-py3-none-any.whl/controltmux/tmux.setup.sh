#
# .tmux.setup.sh - called from .bashrc to handle history save and restore for control-tmux
#
# Copyright 2018 Katie Rust (https://ktpanda.org)
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
# of conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# Don't write history if not running inside tmux
_cmd_writehist() { :; }

##########################################################################################
# BEGIN COMMAND_HOOKS

# Enable other scripts to hook commands at specific points
NEWLINE='
'

_add_prompt_command() {
    cmd="${NEWLINE}$1${NEWLINE}"
    if [[ ${PROMPT_COMMAND} != *"$cmd"* ]]; then
        PROMPT_COMMAND="$cmd${PROMPT_COMMAND}"
    fi
}
_add_command_hook() {
    cmd="${NEWLINE}$1${NEWLINE}"
    if [[ ${COMMAND_HOOKS} != *"$cmd"* ]]; then
        COMMAND_HOOKS+="$cmd"
    fi
}

# Set _oncmd as a DEBUG hook. Make this an alias, because we can't change the DEBUG
# hook from within the hook itself.
alias _oncmd=
trap _oncmd DEBUG

# Create a variable called COMMAND_HOOKS which behaves like PROMPT_COMMAND, but runs
# just before other commands are run. This will run from the DEBUG hook, then disable
# the hook by clearing the _oncmd alias.
[[ "${COMMAND_HOOKS@a}" == *x* ]] && COMMAND_HOOKS=
declare +x COMMAND_HOOKS

_run_command_hooks() {
    eval "$COMMAND_HOOKS"
    alias _oncmd=
}

# Set up PROMPT_COMMAND to 'arm' the hook whenever an interactive prompt is
# displayed. Bash supports PROMPT_COMMAND being a string or an array, so support both
# modes.

_add_prompt_command 'alias _oncmd=_run_command_hooks'

# END COMMAND_HOOKS
##########################################################################################

if [ -n "$TMUX" ]; then
    # $TMUX_INSTANCE is set by control-tmux --log-session (or whenever control-tmux is first run)
    if [ -n "$TMUX_INSTANCE" ]; then
        # Determine the current window. It's possible to attach a pane to multiple
        # windows, but if we are just being launched, we are probably in only one.
	    TMUX_WINDOW=`tmux list-panes -t $TMUX_PANE -F '#{session_name}:#{window_index}' | head -n 1`

        # Save our history to the specified instance
	    _tmux_prefix=$HOME/.tmuxsave/tmux-$TMUX_INSTANCE
	    mkdir -p $_tmux_prefix
	    _tmux_prefix=$_tmux_prefix/${TMUX_PANE#%}

        # Override _cmd_writehist to enable saving
	    _cmd_writehist() { pwd > $_tmux_prefix-pwd; history -w $_tmux_prefix-hist; }
        _add_command_hook '_cmd_writehist'
    else
	    echo "warning: \$TMUX set but \$TMUX_INSTANCE is not set"
    fi
fi

unalias _run_tmux_restore_script 2>/dev/null
_run_tmux_restore_script()
{
    # the restore script will delete itself
    [ -n " $SCN_RESTORE_SCRIPT" ] && . $SCN_RESTORE_SCRIPT
    unset SCN_RESTORE_SCRIPT
    unset _run_tmux_restore_script
    PROMPT_COMMAND="${PROMPT_COMMAND/_run_tmux_restore_script/}"
}

# In user mode, pip installs scripts in ~/.local/bin, but that directory is not in $PATH
# by default on some systems. If `control-tmux` is not in the path, but
# ~/.local/bin/control-tmux exists, then add it to the path.
if [[ `type -t control-tmux` == "" && -e $HOME/.local/bin/control-tmux ]]; then
    PATH=$HOME/.local/bin:$PATH
fi

# Bash reads $HISTFILE after running .bashrc, so we have to defer restoring history until
# the first interactive prompt is shown.
if [ -n "$SCN_RESTORE_SCRIPT" ]; then
    _add_prompt_command '_run_tmux_restore_script'
fi
