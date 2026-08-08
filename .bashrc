# ============================================================================
# ALIASES
# ============================================================================ 
alias gp="git push"
alias nv="nvim"
alias py="python3"
alias dev="cd \$HOME/Environment/"
alias config="cd \$HOME/.config"
alias ls="eza --long --sort=size --icons -a" 
alias ..='cd .. && ls'
alias ...='cd ../.. && ls'
alias h='history'
alias ports='netstat -tulanp'
alias uvr='uv run'
# tmux shortcuts
alias ta='tmux attach -t'
alias tn='tmux new-session -s'
alias tl='tmux list-sessions'
alias tk='tmux kill-session -t' 
alias gs='git status' 


# create dir, cd, create file, open in nv 
mkcd() {
    dir="$1"
    file="$2" 
    mkdir -p "$dir" && cd "$dir" && touch "$file" && nv "$file"
}  

# Added by Antigravity CLI installer
export PATH="$HOME/.local/bin:$PATH"

# cmd-one terminal command helper
source "/Users/chrissilva/Environment/projects/command-one/shell_integration.bash"
