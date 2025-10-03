"forrunningtheseviakeyboardonecharshortcuts"
#!/usr/bin/env bash
# Usage: ./send-vi-keys.sh hjklddw
# Sends each character as a keypress to the currently focused window.
buffer=""
prompt='>>> '
plen=${#prompt}

# read raw single characters until we detect the full Python prompt ">>> "
while IFS= read -rsn1 ch; do
    # process the character here (e.g. send it to the focused window)
    printf '%s' "$ch"
    buffer+="$ch"
    if (( ${#buffer} >= plen )) && [[ "${buffer: -$plen}" == "$prompt" ]]; then
        break
    fi
done