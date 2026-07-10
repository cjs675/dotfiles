# ============================================================================
# PROMPT INITIALIZATION
# ============================================================================
eval "$(starship init zsh)"
export STARSHIP_CONFIG=~/.config/starship/starship.toml

# ============================================================================
# ENVIRONMENT & PATH SETUP
# ============================================================================
eval "$(/opt/homebrew/bin/brew shellenv)"

export PATH="$HOME/.cargo/bin:$PATH"                                          # Rust
export PATH="/usr/local/go/bin:$PATH"                                         # Go
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"       # Solana
export PATH="/opt/homebrew/opt/emacs/bin:$PATH"                               # Emacs
export PATH="/opt/homebrew/opt/gnu-tar/libexec/gnubin:$PATH"                  # GNU tar
export PATH="/Users/data/.avm/bin:$PATH"                                      # AVM
export PATH="/Applications/Postgres.app/Contents/Versions/18/bin:$PATH"       # Postgres
export PATH="$HOME/.local/bin:$PATH"                                          # Local scripts

# Bun setup
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# ============================================================================
# VERSION MANAGERS
# ============================================================================
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

# ============================================================================
# SHELL COMPLETIONS
# ============================================================================
fpath=($HOME/.docker/completions $fpath)

autoload -Uz compinit
compinit -i
zstyle ':completion:*' menu select

[ -s "/Users/data/.bun/_bun" ] && source "/Users/data/.bun/_bun"

# ============================================================================
# ALIASES
# ============================================================================
alias nv="nvim"
alias py="python3"
alias dev="cd /Users/chrissilva/environment/"
alias config="cd /Users/chrissilva/.config"
alias ls="eza --long --sort=size --icons"
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
alias gp='git push'

# ============================================================================
# TMUX AUTO-ATTACH
# ============================================================================
if [ -z "$TMUX" ]; then
    tmux attach || tmux new
fi
tmux set-option status off 2>/dev/null

export PGPORT=5434
export HOMEBREW_NO_ENV_HINTS=1  

# ========================================================================== 
# function to create & edit file (with boilerplate if cpp) into specified dir using nvim 
#===========================================================================

# create dir and cd 
mkproj() { 

    local dir="$1"
    local file="$2" 

    # 1. create dir & move into it 
    # || return 1 stops script if folder fails to create 
    mkdir -p "$dir" && cd "$dir" || return 1

    # 2. check if file ends in .cpp (if so insert boilerplate)  
    if [[ "$file" == *.cpp ]]; then
        echo "#include <iostream>\n\nint main() {\n    \n    return 0;\n}" > "$file"
    else 
        # if !.cpp, create empty file 
        touch "$file" 
    fi 

    # open in nv
    nv "$file" 
}

# create dir, cd, create file, open in nv 
mkcd() {
    dir="$1"
    file="$2" 
    mkdir -p "$dir" && cd "$dir" && touch "$file" && nv "$file"
} 


# ========================================================================== 
# function to write g++ main.cpp -o main && ./main in one command (run) 
#===========================================================================
run() {
    # default to main.cpp if no filename is given 
    local src="${1:-main.cpp}" 

    # check if file exists before trying to compile 
    if [[ ! -f "$src" ]]; then
        echo "Error: $src not found"
        return 1
    fi

    # strip .cpp extension to get output name (main.cpp -> main) 
    local out="${src%.*}" 

    # compile & run 
    g++ "$src" -o "$out" && ./"$out" 
}




# Added by Antigravity CLI installer
export PATH="/Users/chrissilva/.local/bin:$PATH"

# bun completions
[ -s "/Users/chrissilva/.bun/_bun" ] && source "/Users/chrissilva/.bun/_bun"
