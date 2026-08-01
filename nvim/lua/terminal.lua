require("toggleterm").setup {
    -- size can be a number or function which is passed the current terminal 
    -- size = 20 | function(term) 
        size = function(term)
            if term.direction == "horizontal" then
                return 15
            elseif term.direction == "vertical" then
                return vim.o.columns * 0.4
            end
        end,
        open_mapping = [[<C-t>]],
        hide_numbers = false,       -- hide number column in toggleterm buffers
        shade_filetypes = {},
        shade_terminals = true,
        start_in_insert = true,
        insert_mappings = true,     -- whether or not open mapping applies in insert mode
        persist_size = true,
        -- direction = "vertical" | "horizontal" | "window" | "float" ,
        direction = "horizontal",
        close_on_exit = true,       -- close the terminal window when the process exits 
        shell = vim.o.shell,                -- change default shell 
        float_opts = {
            border = 'curved',
            winblend = 3,
            highlights = {
                border = "Normal",
                background = "Normal",
            }
        }
}
