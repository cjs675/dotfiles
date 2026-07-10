local configs = require("nvim-treesitter")

configs.setup({
    ensure_installed = {
        -- languages 
        "go", "java", "typescript", "tsx",
        "cpp", "json", "bash", "zsh",
        "html", "svelte", "javascript", "css",
        -- essential parsers for nvim 
        "c", "lua", "vim", "vimdoc", "query",
         -- extras 
        "http", "markdown", "markdown_inline",
        "dockerfile"
    },
    sync_install = false,
    highlight = {
        enable = true,
    },
    indent = {
        enable = true,
    },
})
-- create autocmd evertime buffer is set 
vim.api.nvim_create_autocmd("FileType", {
    -- done for all filetypes 
    pattern = "*",
    callback = function(args)
        -- store buffer number of file just opened 
        local buf = args.buf
        -- reads filetype of specific buffer 
        local ft = vim.bo[buf].filetype
        -- get treesitter lang name for current file type 
        local lang = vim.treesitter.language.get_lang(ft)
        -- if no matching parses found, fallback to vim regex highlights 
        if not lang then
            return
        end
        -- load parser 
        local ok_add = pcall(vim.treesitter.language.add, lang)
        -- if parser not installed, fallback 
        if not ok then
            return
        end
        -- start treesitter highlights on buffer 
        pcall(vim.treesitter.start, buf, lang)
    end,
})


